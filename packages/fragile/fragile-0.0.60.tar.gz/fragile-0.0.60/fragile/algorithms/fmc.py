import copy
from typing import Iterable, Optional, Tuple, Union

import einops
import judo
import numpy

from fragile.callbacks.data_tracking import StoreInitAction
from fragile.core.api_classes import Callback, EnvironmentAPI, PolicyAPI, WalkersAPI
from fragile.core.swarm import Swarm
from fragile.core.typing import InputDict, StateData, StateDict, Tensor


class BoundaryInitAction(Callback):
    name = "boundary_action"
    default_outputs = ("actions",)

    def __init__(self, only_first_epoch: bool = True, **kwargs):
        self.only_first_epoch = only_first_epoch
        super(BoundaryInitAction, self).__init__(**kwargs)

    def after_policy(self):
        assert hasattr(self.swarm.policy, "bounds")
        if self.only_first_epoch and self.swarm.epoch > 0:
            return
        low_val = einops.repeat(self.swarm.policy.bounds.low, "n -> b n", b=self.swarm.n_walkers)
        high_val = einops.repeat(self.swarm.policy.bounds.high, "n -> b n", b=self.swarm.n_walkers)
        condition = judo.random_state.random(low_val.shape) < 0.5
        actions = numpy.where(condition, low_val, high_val)
        self.update(actions=actions)


class FMCPolicy(PolicyAPI):

    default_inputs = {"init_actions": {}, "oobs": {}}

    def __init__(self, inner_swarm, follow_best: bool = False, **kwargs):
        self.inner_swarm = inner_swarm
        self._follow_best_flag = follow_best
        super(FMCPolicy, self).__init__(**kwargs)

    @property
    def param_dict(self) -> StateDict:
        pdict = self.inner_swarm.env.param_dict
        return {**{"init_actions": dict(pdict["actions"])}, **pdict}

    def select_actions(self, **kwargs) -> Union[Tensor, StateData]:
        if self._follow_best_flag:
            return self._follow_best()
        if hasattr(self.inner_swarm.env, "action_space") and hasattr(
            self.inner_swarm.env.action_space,
            "n",
        ):
            return self._choose_majority()
        init_actions = self.inner_swarm.get("init_actions")
        selected_action = judo.copy(init_actions.mean(0)[None])
        return selected_action

    def _choose_majority(self):
        init_actions = judo.to_numpy(self.inner_swarm.get("init_actions"))
        y = numpy.bincount(init_actions, minlength=self.inner_swarm.env.action_space.n)
        most_used_action = judo.tensor([y.argmax()])
        return most_used_action

    def _follow_best(self):
        return self.inner_swarm.root.data["init_actions"].unsqueeze(0)
        # init_actions = judo.to_numpy(self.inner_swarm.get("init_actions"))
        # y = judo.to_numpy(self.inner_swarm.get("scores"))
        # oobs, terminals = self.inner_swarm.get("oobs"), self.inner_swarm.get("terminals")
        # index = judo.arange(len(y))
        # valid_ix = judo.logical_or(~oobs, terminals)
        # best_ix = y[valid_ix].argmin() if self.inner_swarm.minimize else y[valid_ix].argmax()
        # best_ix_orig = index[valid_ix][best_ix]
        # best_action = init_actions[best_ix_orig][np.newaxis, :]
        # return best_action


class EnvSwarm(EnvironmentAPI):
    def __init__(self, swarm):
        self.inner_swarm = swarm
        super(EnvSwarm, self).__init__(
            swarm=None,
            action_shape=swarm.env.action_shape,
            action_dtype=swarm.env.action_dtype,
            observs_shape=swarm.env.observs_shape,
            observs_dtype=swarm.env.observs_dtype,
        )

    def __getattr__(self, item):
        return getattr(self.inner_swarm.env, item)

    @property
    def inputs(self) -> InputDict:
        return self.inner_swarm.env.inputs

    @property
    def outputs(self) -> Tuple[str, ...]:
        return self.inner_swarm.env.outputs + ("scores",)

    @property
    def param_dict(self) -> StateDict:
        pdict = self.inner_swarm.env.param_dict
        return {**{"scores": pdict["rewards"]}, **pdict}

    def make_transitions(self, inplace: bool = True, **kwargs) -> Union[None, StateData]:
        env_data = self.swarm.inputs_from_swarm("env")
        # old_pos = env_data["observs"].clone()
        env_data = self.inner_swarm.env.make_transitions(
            inplace=False,
            **{
                k: copy.deepcopy(v) if k in self.swarm.state.list_names else judo.copy(v)
                for k, v in env_data.items()
            },
        )
        env_data["scores"] = judo.copy(env_data["rewards"])
        if self.inner_swarm.walkers.accumulate_reward:
            env_data["scores"] += judo.copy(self.get("scores"))
        if inplace:
            self.swarm.state.update(
                {
                    k: copy.deepcopy(v) if k in self.swarm.state.list_names else judo.copy(v)
                    for k, v in env_data.items()
                },
            )
        else:
            return env_data


class WalkersSwarm(WalkersAPI):
    def __init__(self, inner_swarm, **kwargs):
        self.inner_swarm = inner_swarm
        self.accumulate_reward = self.inner_swarm.walkers.accumulate_reward
        super(WalkersSwarm, self).__init__(**kwargs)

    @property
    def param_dict(self) -> StateDict:
        return self.inner_swarm.param_dict

    def __getattr__(self, item):
        return getattr(self.inner_swarm, item)

    def run_epoch(self, inplace: bool = True, **kwargs) -> StateData:
        self.inner_swarm.run(root_walker=dict(self.swarm.state))
        return {}

    def reset(self, inplace: bool = True, **kwargs):
        super(WalkersSwarm, self).reset(inplace=inplace, **kwargs)
        self.inner_swarm.reset()
        walker = self.inner_swarm.state.export_walker(0)
        self.swarm.state.update(**walker)


class FMCSwarm(Swarm):
    walkers_last = False

    def __init__(
        self,
        swarm: Swarm,
        policy: PolicyAPI = None,
        env: EnvironmentAPI = None,
        callbacks: Optional[Iterable[Callback]] = None,
        minimize: bool = False,
        max_epochs: int = 1e100,
        store_init_action: Callback = None,
    ):
        store_init_action = StoreInitAction() if store_init_action is None else store_init_action
        swarm.register_callback(store_init_action)
        # if hasattr(swarm.policy, "bounds"):
        #    swarm.register_callback(BoundaryInitAction())
        self._swarm = swarm
        policy = FMCPolicy(swarm) if policy is None else policy
        env = EnvSwarm(swarm) if env is None else env
        super(FMCSwarm, self).__init__(
            n_walkers=swarm.n_walkers,
            policy=policy,
            env=env,
            callbacks=callbacks,
            minimize=minimize,
            max_epochs=int(max_epochs),
            walkers=WalkersSwarm(swarm),
        )

    @property
    def swarm(self) -> Swarm:
        return self._swarm

    @property
    def n_walkers(self) -> int:
        return 1

    def inputs_from_swarm(self, name):
        def get_names():
            names = []
            inputs = getattr(self.swarm, name).inputs
            for k, v in inputs.items():
                is_optional = v.get("optional", False)
                if not is_optional or (is_optional and k in self.swarm.param_dict.keys()):
                    names.append(k)
            return names

        return {name: self.state[name] for name in get_names()}
