import copy

import einops
import judo
from judo.data_types import dtype

from fragile.core.api_classes import Callback
from fragile.core.typing import StateDict


class StoreInitAction(Callback):
    name = "store_init_action"
    default_inputs = {"init_actions": {"clone": True}}
    default_outputs = ("init_actions",)

    @property
    def param_dict(self) -> StateDict:
        return {"init_actions": dict(self.swarm.param_dict["actions"])}

    def before_env(self):
        if self.swarm.epoch == 0:
            self.update(init_actions=judo.copy(self.get("actions")))


class TrackWalkersId(Callback):
    default_inputs = {"id_walkers": {"clone": True}, "parent_ids": {"clone": True}}
    default_param_dict = {
        "id_walkers": {"dtype": dtype.hash_type},
        "parent_ids": {"dtype": dtype.hash_type},
    }

    def update_ids(self, inactives: bool = True):
        with judo.Backend.use_backend("numpy"):
            name = "states" if "states" in self.swarm.state.names else "observs"
            actives = judo.to_numpy(self.swarm.state.actives)
            new_ids_all = self.swarm.state.hash_batch(name)
            parent_ids = judo.copy(judo.to_numpy(self.get("parent_ids", inactives=inactives)))
            new_ids = judo.copy(judo.to_numpy(self.get("id_walkers", inactives=True)))
            parent_ids[actives] = judo.copy(new_ids[actives])
            new_ids[actives] = new_ids_all[actives]
        self.update(
            parent_ids=judo.to_backend(parent_ids),
            id_walkers=judo.to_backend(new_ids),
            inactives=inactives,
        )

    def after_env(self):
        self.update_ids()


class KeepBestN(Callback):
    name = "keep_best_n"

    def __init__(
        self,
        n_keep: int,
        always_update: bool = False,
        fix_walkers: bool = True,
        **kwargs,
    ):
        super(KeepBestN, self).__init__(**kwargs)
        self.minimize = None
        self.always_update = always_update
        self.n_keep = n_keep
        self.fix_walkers = fix_walkers
        self.top_walkers = []
        self.top_scores = []

    def setup(self, swarm):
        super(KeepBestN, self).setup(swarm)
        self.minimize = swarm.minimize

    def reset(self, *args, **kwargs):
        self.top_walkers = []
        self.top_scores = []

    def before_walkers(self):
        self.update_top_walkers()

    def get_topk_walkers(self):
        scores, oobs, terminals = self.get("scores"), self.get("oobs"), self.get("terminals")
        index = judo.arange(len(scores))
        bool_ix = ~oobs if terminals is None else judo.logical_or(~oobs, terminals)
        alive_scores = judo.copy(scores[bool_ix])
        if len(alive_scores) == 0:
            return None, None
        # print(alive_scores)
        _, topk = judo.topk(alive_scores, k=self.n_keep, largest=not self.minimize)
        # topk = judo.astype(judo.clip(topk, 0, judo.inf), judo.int)
        top_indexes = judo.copy(index[bool_ix][topk])
        top_scores = judo.copy(scores[bool_ix][topk])
        top_walkers = [self.swarm.state.export_walker(i, copy=True) for i in top_indexes]
        try:
            return top_walkers, top_scores
        except Exception as e:
            print(topk, bool_ix)
            raise e

    def update_top_walkers(self):
        last_top_walkers, last_top_scores = self.get_topk_walkers()
        if last_top_walkers is None:
            return
        elif self.always_update:
            new_top_walkers = last_top_walkers
            new_top_scores = last_top_scores
        else:
            all_top_walkers = self.top_walkers + last_top_walkers
            if judo.is_tensor(self.top_scores):
                curr_top_list = einops.asnumpy(self.top_scores).tolist()
            else:
                curr_top_list = self.top_scores
            last_top_list = einops.asnumpy(last_top_scores).tolist()
            top_scores = judo.tensor(curr_top_list + last_top_list)
            new_top_scores, topk = judo.topk(top_scores, k=self.n_keep, largest=not self.minimize)
            new_top_walkers = [all_top_walkers[i] for i in einops.asnumpy(topk).astype(int)]

        self.top_walkers = new_top_walkers
        self.top_scores = new_top_scores
        return

        # if not judo.Backend.is_numpy():# and judo.dtype.is_tensor(self.score):
        #    scores = self._data["scores"]
        #    score = scores[0] if isinstance(scores, list) else scores.item()
        # else:
        score = self.score
        score_improves = (best_score < score) if self.minimize else (best_score > score)
        if self.always_update or score_improves:  # or numpy.isinf(score):
            # new_best = {k: copy.deepcopy(v) for k, v in best.items()}
            self._data = copy.deepcopy(best)

    def fix_topk_walkers(self):
        if self.fix_walkers:
            terminals = self.swarm.get("terminals")
            for i, walker in enumerate(self.top_walkers):
                self.swarm.state.import_walker(copy.deepcopy(walker), index=i)
                if not self.swarm.state.actives[i] and terminals is not None and not terminals[i]:
                    self.swarm.state.actives[i] = True
                    self.swarm.state._n_actives += 1

    def after_walkers(self):
        self.fix_topk_walkers()
