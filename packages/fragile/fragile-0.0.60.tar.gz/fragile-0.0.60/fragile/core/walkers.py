from collections import defaultdict
from typing import Any, Dict, Optional, Tuple, Union

import judo
from judo import dtype, random_state, tensor

from fragile.core.api_classes import WalkersAPI, WalkersMetric
from fragile.core.fractalai import fai_iteration, relativize
from fragile.core.typing import InputDict, StateData, StateDict, Tensor


class SimpleWalkers(WalkersAPI):
    default_inputs = {
        "observs": {},
        "oobs": {"optional": True},
        "is_won": {"optional": True},
        "rewards": {},
        "scores": {"clone": True},
    }
    default_param_dict = {"scores": {"dtype": dtype.float32}}
    default_outputs = tuple(["scores"])

    def __init__(
        self,
        accumulate_reward: bool = True,
        score_scale: float = 1.0,
        diversity_scale: float = 1.0,
        minimize: bool = False,
        **kwargs,
    ):
        self.score_scale = score_scale
        self.diversity_scale = diversity_scale
        self.accumulate_reward = accumulate_reward
        self.minimize = minimize
        super(SimpleWalkers, self).__init__(**kwargs)

    def run_epoch(
        self,
        observs,
        rewards,
        scores,
        oobs=None,
        inplace: bool = True,
        **kwargs,
    ) -> StateData:
        scores = rewards + scores if self.accumulate_reward else rewards
        sign_scores = -1.0 * scores if self.minimize else scores
        compas_ix, will_clone = fai_iteration(
            observs=observs,
            rewards=sign_scores,
            oobs=oobs,
            dist_coef=self.diversity_scale,
            reward_coef=self.score_scale,
        )
        if inplace:
            self.clone_walkers(compas_clone=compas_ix, will_clone=will_clone)
        return {"scores": scores}


def l2_norm(x: Tensor, y: Tensor) -> Tensor:
    """
    Compute the L2 norm between two tensors.

    Args:
        x (Tensor): The first tensor.
        y (Tensor): The second tensor.

    Returns:
        Tensor: The L2 norm between the two input tensors.
    """
    return judo.sqrt(judo.sum((x - y) ** 2, 1))


class ScoreMetric(WalkersMetric):
    """
    A base class for score metrics in a swarm of walkers.

    Attributes:
        default_param_dict (dict): Default parameters dictionary for the score metric.
        default_outputs (tuple): Tuple containing the default output keys.
    """

    default_param_dict = {"scores": {"dtype": dtype.float32}}
    default_outputs = tuple(["scores"])


class RewardScore(ScoreMetric):
    """
    A class representing the reward score metric for a swarm of walkers.

    Attributes:
        default_inputs (dict): Default inputs dictionary for the reward score metric.
    """

    default_inputs = {"rewards": {}}

    def __init__(self, accumulate_reward: bool = True, keep_max_reward: bool = False, **kwargs):
        self.accumulate_reward = accumulate_reward
        self.keep_max_reward = keep_max_reward
        super(RewardScore, self).__init__(**kwargs)

    @property
    def inputs(self) -> InputDict:
        inputs = super(RewardScore, self).inputs
        if self.accumulate_reward:
            inputs["scores"] = {"clone": True}
        return inputs

    def calculate(
        self,
        rewards: Optional[Tensor] = None,
        scores=None,
        **kwargs,
    ) -> Dict[str, Tensor]:
        """
        Calculate the scores for the walkers based on rewards.

        Args:
            rewards (array): Array of walkers' rewards.
            scores (array, optional): Array of walkers' scores.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the scores.
        """
        rewards = self.get("rewards", inactives=True) if rewards is None else rewards
        actives = self.swarm.state.actives
        if self.accumulate_reward:
            values = self.get("scores", inactives=True)
            values[actives] = values[actives] + rewards[actives]
        else:
            values = rewards
        if self.keep_max_reward and scores is not None:
            values = (
                judo.minimum(values, scores)
                if self.swarm.minimize
                else judo.maximum(values, scores)
            )
        return {"scores": values}

    def reset(
        self,
        inplace: bool = True,
        root_walker: Optional[StateData] = None,
        states: Optional[StateData] = None,
        **kwargs,
    ) -> None:
        """
        Reset the reward score metric.

        Args:
            inplace (bool, optional): Whether to reset in-place. Defaults to True.
            root_walker (StateData, optional): The root walker to reset. Defaults to None.
            states (Optional[StateData], optional): The state data to reset. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        if root_walker is None and not self.accumulate_reward:
            rewards = self.get("rewards", inactives=True)
            # _default_reward = numpy.inf if self.swarm.minimize else numpy.ninf
            # rewards = rewards * _default_reward
            self.update(scores=rewards, inactives=True)


class SonicScore(ScoreMetric):
    accumulate_reward = False
    default_inputs = {
        "rewards": {"clone": True},
        "infos": {"clone": True},
        "scores": {"clone": True},
    }

    @staticmethod
    def score_from_info(info):
        not_in_bonus_level = not (info.get("in_bonus_level") or info.get("in_transition_screen"))
        if info.get("in_boss_fight", False):
            score_x = 1010
        elif info.get("in_bonus_level"):
            score_x = 1002
        elif info.get("in_transition_screen"):
            score_x = 1008
        else:
            score_x = 1000 * min(info.get("x", 0) / max(info.get("screen_x_end", 1), 1), 1)
        score = (
            info.get("score", 0)
            + score_x
            + 10 * info.get("rings", 0)
            + 1001
            * (
                info.get("act", 0)
                if (not_in_bonus_level and not info.get("in_transition_screen"))
                else info.get("act", 0) - 1
            )
            + 5000 * info.get("zone", 0)
            + 1000 * info.get("lives", 0)
        )
        return int(score)

    def calculate(self, rewards, scores=None, **kwargs):
        scores = tensor([self.score_from_info(info) for info in self.get("infos", inactives=True)])
        scores = judo.maximum(scores, self.get("scores", inactives=True))
        return {"scores": scores}


class MarioScore(ScoreMetric):
    name = "MarioScore"
    accumulate_reward = False
    default_inputs = {"rewards": {}, "infos": {}}

    @staticmethod
    def score_from_info(info):
        score = (
            (info.get("world", 0) * 25000)
            + (info.get("stage", 0) * 5000)
            + info.get("x_pos", 0)
            + 10 * int(bool(info.get("in_pipe", 0)))
            + 100 * int(bool(info.get("flag_get", 0)))
            + 10 * info.get("coins", 0)
            + info["life"] * 1000
            # + (abs(info["x_pos"] - info["x_position_last"]))
        )

        return score

    def calculate(self, rewards=None, scores=None, **kwargs):
        scores = tensor([self.score_from_info(info) for info in self.get("infos")])
        self.update(scores=scores)
        scores = self.get("scores", inactives=True)
        return {"scores": scores}


class DiversityMetric(WalkersMetric):
    """
    A base class for diversity metrics in a swarm of walkers.

    Attributes:
        default_param_dict (dict): Default parameters dictionary for the diversity metric.
        default_outputs (tuple): Tuple containing the default output keys.
    """

    default_param_dict = {"diversities": {"dtype": dtype.float32}}
    default_outputs = tuple(["diversities"])


class RandomDistance(DiversityMetric):
    """
    A class representing the random distance diversity metric for a swarm of walkers.

    Attributes:
        default_inputs (dict): Default inputs dictionary for the random distance diversity metric.
    """

    use_pbc = False
    default_inputs = {"observs": {}, "oobs": {}}

    def calculate(self, observs, oobs, **kwargs):
        """
        Calculate the diversities for the walkers based on the L2 distance to another \
        walker chosen at random.

        Args:
            observs (array): Array of walkers' observations.
            oobs (array): Array of out-of-bounds flags for walkers.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the diversities.
        """
        compas = self.swarm.walkers.get_in_bounds_compas(oobs=oobs)
        obs = judo.astype(observs.reshape(observs.shape[0], -1), dtype.float32)
        if self.use_pbc and hasattr(self.swarm.env, "bounds"):
            deltas = self.swarm.env.bounds.pbc_distance(obs, obs[compas])
            # return {"diversities": numpy.linalg.norm(deltas, axis=1).flatten()}
            return {"diversities": l2_norm(deltas, 0).flatten()}
        return {"diversities": l2_norm(obs, obs[compas]).flatten()}


class Walkers(WalkersAPI):
    """
    Walkers class handles the walkers' dynamics, including scoring, diversity, cloning, \
    and resetting.

    Inherits from WalkersAPI.
    """

    default_param_dict = {
        "compas_clone": {"dtype": dtype.int64},
        "virtual_rewards": {"dtype": dtype.float32},
        "clone_probs": {"dtype": dtype.float32},
        "will_clone": {"dtype": dtype.bool},
        # "actives": {"dtype": dtype.bool},
    }
    default_outputs = (
        "compas_clone",
        "virtual_rewards",
        "clone_probs",
        "will_clone",
    )  # , "actives")

    default_inputs = {"oobs": {}, "terminals": {"optional": True}}

    def __init__(
        self,
        score: ScoreMetric = None,
        diversity: DiversityMetric = None,
        minimize: bool = False,
        score_scale: float = 1.0,
        diversity_scale: float = 1.0,
        track_data=None,
        accumulate_reward: bool = True,
        keep_max_reward: bool = False,
        clone_period: int = 1,
        freeze_walkers=True,
        **kwargs,
    ):
        """
        Initialize a Walkers object.

        Args:
            score (ScoreMetric, optional): Scoring metric. Defaults to None.
            diversity (DiversityMetric, optional): Diversity metric. Defaults to None.
            minimize (bool, optional): Whether to minimize the score. Defaults to False.
            score_scale (float, optional): Scaling factor for score. Defaults to 1.0.
            diversity_scale (float, optional): Scaling factor for diversity. Defaults to 1.0.
            track_data (iterable, optional): Data to track. Defaults to None.
            accumulate_reward (bool, optional): Whether to accumulate rewards. Defaults to True.
            keep_max_reward (bool, optional): Whether to keep maximum reward. Defaults to False.
            clone_period (int, optional): Clone period. Defaults to 1.
            freeze_walkers (bool, optional): Whether to freeze walkers. Defaults to True.
            **kwargs: Additional keyword arguments.
        """

        self.minimize = minimize
        self.score_scale = score_scale
        self.diversity_scale = diversity_scale
        self.clone_period = clone_period
        self.score = (
            score
            if score is not None
            else RewardScore(accumulate_reward=accumulate_reward, keep_max_reward=keep_max_reward)
        )
        self.accumulate_reward = self.score.accumulate_reward
        self.diversity = diversity if diversity is not None else RandomDistance()
        self.track_data = set(track_data) if track_data is not None else set()
        self.freeze_walkers = freeze_walkers
        super(WalkersAPI, self).__init__(**kwargs)

    @property
    def param_dict(self) -> StateDict:
        return {
            **super(WalkersAPI, self).param_dict,
            **self.diversity.param_dict,
            **self.score.param_dict,
        }

    @property
    def inputs(self) -> InputDict:
        return {**super(WalkersAPI, self).inputs, **self.diversity.inputs, **self.score.inputs}

    @property
    def outputs(self) -> Tuple[str, ...]:
        return super(WalkersAPI, self).outputs + self.score.outputs + self.diversity.outputs

    def setup(self, swarm):
        """
        Set up the Walkers object by initializing its swarm.

        Args:
            swarm: Swarm object to be initialized.
        """
        super(Walkers, self).setup(swarm)
        self.diversity.setup(swarm)
        self.score.setup(swarm)
        self.minimize = swarm.minimize

    def balance(self, inplace: bool = True, **kwargs) -> Union[None, StateData]:
        """
        Balance the walkers.

        Args:
            inplace (bool, optional): Whether to perform the operation inplace. Defaults to True.
            **kwargs: Additional keyword arguments.

        Returns:
            Union[None, StateData]: None if inplace=True, otherwise a StateData object.
        """
        if self.swarm.epoch % self.clone_period == 0 or self.swarm.epoch == 0:
            return super(Walkers, self).balance(inplace=inplace, **kwargs)

    def run_epoch(self, inplace: bool = True, oobs=None, **kwargs) -> Dict[str, Tensor]:
        """
        Execute an epoch in the walkers' dynamics.

        Args:
            inplace (bool, optional): Whether to perform the operation inplace. Defaults to True.
            oobs: Out of bounds flags.
            **kwargs: Additional keyword arguments.

        Returns:
            StateData: State data after the epoch execution.
        """
        scores = self.score(**kwargs)
        diversities = self.diversity(oobs=oobs, **kwargs)
        virtual_rewards = self.calculate_virtual_reward(**{**scores, **diversities})
        clone_data = self.calculate_clones(oobs=oobs, **virtual_rewards)
        actives = clone_data.get("actives")
        if actives is not None and self.freeze_walkers:
            self.swarm.state.update_actives(actives)
        if inplace:
            self.clone_walkers(**clone_data)
        return {**scores, **diversities, **virtual_rewards, **clone_data}

    def calculate_virtual_reward(self, scores, diversities, **kwargs):
        """
        Calculate the virtual rewards for walkers based on scores and diversities.

        Args:
            scores (array): Array of walkers' scores.
            diversities (array): Array of walkers' diversities.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the virtual rewards.
        """
        scores = -1.0 * scores if self.minimize else scores
        norm_scores = relativize(scores)
        norm_diver = relativize(diversities)
        virtual_rewards = norm_scores**self.score_scale * norm_diver**self.diversity_scale
        return {"virtual_rewards": virtual_rewards}

    def calculate_clones(self, virtual_rewards, oobs=None) -> Dict[str, Tensor]:
        """
        Calculate the walkers that will clone and their target companions.

        Args:
            virtual_rewards (array): Array of walkers' virtual rewards.
            oobs (array, optional): Array of out-of-bounds flags for walkers. Defaults to None.

        Returns:
            dict: A dictionary containing clone probabilities, will_clone flags, \
            companion clones, and active flags.
        """
        n_walkers = len(virtual_rewards)
        all_virtual_rewards_are_equal = (virtual_rewards == virtual_rewards[0]).all()
        terminals = self.swarm.get("terminals")
        if all_virtual_rewards_are_equal:
            clone_probs = judo.zeros(n_walkers, dtype=dtype.float)
            compas_clone = judo.arange(n_walkers)
        else:
            compas_clone = self.get_in_bounds_compas(oobs)
            # This value can be negative!!
            clone_probs = (virtual_rewards[compas_clone] - virtual_rewards) / virtual_rewards
        prob_trigger = judo.abs(clone_probs) > random_state.random_sample(n_walkers)
        will_clone = judo.logical_and(prob_trigger, clone_probs > 0)
        actives = judo.logical_not(judo.logical_and(prob_trigger, clone_probs < 0))
        if oobs is not None:
            will_clone[oobs] = True  # Out of bounds walkers always clone
        if terminals is not None:
            will_clone[terminals] = False  # Terminal walkers do not clone
            actives[terminals] = False
        return dict(
            clone_probs=clone_probs,
            will_clone=will_clone,
            compas_clone=compas_clone,
            actives=actives,
        )

    def reset(self, inplace: bool = True, **kwargs) -> None:
        """
        Reset the Walkers object and its score and diversity components.

        Args:
            inplace (bool, optional): Whether to perform the operation inplace. Defaults to True.
            **kwargs: Additional keyword arguments.
        """
        super(Walkers, self).reset(inplace=inplace, **kwargs)
        self.score.reset(**kwargs)
        self.diversity.reset(**kwargs)


class ExplorationWalkers(Walkers):
    def __init__(self, exploration_scale: float = 1.0, **kwargs):
        super(ExplorationWalkers, self).__init__(**kwargs)
        self._explore_counts = defaultdict(0)
        self.exploration_scale = exploration_scale

    @property
    def explore_counts(self) -> Dict[Any, int]:
        return self._explore_counts

    def calculate_virtual_reward(self, scores, diversities, **kwargs):
        """Apply the virtual reward formula to account for all the different goal scores."""
        vr_dict = super(ExplorationWalkers, self).calculate_virtual_reward(
            scores,
            diversities,
            **kwargs,
        )
        explore_reward = relativize(self.get_explore_rewards())
        virtual_rewards = vr_dict["virtual_rewards"] * explore_reward**self.exploration_scale
        return {"virtual_rewards": virtual_rewards}

    def get_explore_rewards(self):
        coords_keys = self.get_coords_keys()
        for key in coords_keys:
            self._explore_counts[key] += 1
        return 1 / judo.tensor([self.explore_counts[k] for k in coords_keys])

    def get_coords_keys(self):
        keys = []
        for info in self.get("infos"):
            in_bonus_level = info.get("screen_x_end", 1) == 0 and info.get("x", -1) != 0
            act = info.get("act") if not in_bonus_level else 0.5
            key = (info.get("zone"), act, int(info.get("x", 0) / 100), int(info.get("y", 0) / 100))
            keys.append(key)
        return keys


class NoBalance(Walkers):
    """
    A class representing walkers with no balancing behavior in a swarm.

    Inherits from the Walkers class and modifies the properties and methods to disable balancing.
    """

    @property
    def param_dict(self) -> StateDict:
        return self.score.param_dict

    @property
    def inputs(self) -> InputDict:
        return self.score.inputs

    @property
    def outputs(self) -> Tuple[str, ...]:
        return self.score.outputs

    def run_epoch(self, inplace: bool = True, oobs=None, **kwargs) -> Dict[str, Tensor]:
        """
        Run an epoch for the walkers without balancing.

        Args:
            inplace (bool, optional): Whether to run the epoch in-place. Defaults to True.
            oobs (array, optional): Array of out-of-bounds walkers. Defaults to None.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the scores.
        """
        scores = self.score(**kwargs)
        return scores
