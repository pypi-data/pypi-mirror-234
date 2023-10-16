"""This modes implements an interfacing with the `evotorch` library."""
from typing import Optional, Union

from evotorch.algorithms.searchalgorithm import SearchAlgorithm
from evotorch.core import Problem, SolutionBatch
import judo
from judo import Bounds, dtype

from fragile.core.env import Function
from fragile.core.typing import StateData


class EvotorchEnv(Function):
    """
    This environment implements an interface with the `evotorch` library.

    When providing an instance of an evotorch :class:`Searcher` it will \
    wrap it and allow to use all the fragile features on top of evotorch, such as \
    plotting, custom policies, etc.
    """

    default_inputs = {
        "actions": {},
        "observs": {"clone": True},
        "rewards": {"clone": True},
    }
    default_outputs = ("observs", "rewards", "oobs")

    def __init__(
        self,
        algorithm: SearchAlgorithm,
        function: Optional[callable] = None,
        bounds: Optional[Bounds] = None,
        **kwargs,
    ):
        """
        Initialize an :class:`EvotorchEnv` instance.

        Args:
            searcher (SearchAlgorithm): An instance of an evotorch :class:`SearchAlgorithm`.
            kwargs: Additional keyword arguments to pass to the :class:`Function`.
        """
        self._algorithm = algorithm
        reward_function = self._get_function() if function is None else function
        bounds = self._get_bounds() if bounds is None else bounds
        super().__init__(function=reward_function, bounds=bounds, **kwargs)

    @property
    def algorithm(self) -> SearchAlgorithm:
        """Return the evotorch :class:`SearchAlgorithm` instance used by this environment."""
        return self._algorithm

    @property
    def population(self) -> SolutionBatch:
        """
        Access the :class:`SolutionBatch` instance used by the evotorch :class:`SearchAlgorithm`.
        """
        return self._algorithm.population

    @property
    def problem(self) -> Problem:
        """Access the :class:`Problem` instance used by the evotorch :class:`SearchAlgorithm`."""
        return self._algorithm.problem

    @property
    def dtype(self):
        """
        Access the dtype used by the evotorch :class:`SearchAlgorithm` for the solution values.
        """
        return self._algorithm.population.dtype

    @property
    def eval_dtype(self):
        """Access the dtype used by the :class:`SearchAlgorithm` for the solution evaluations."""
        return self._algorithm.population.eval_dtype

    @property
    def solution_length(self) -> int:
        """Access the length of the solution used by the evotorch :class:`SearchAlgorithm`."""
        return self._algorithm.population.solution_length

    def _get_bounds(self) -> Bounds:
        """
        Initialize the :class:`Bounds` instance used by this environment.

        Extract all the information about the dimensionality and data type of the solutions
        from the problem instance used by the evotorch :class:`SearchAlgorithm`.
        """
        if self.problem.lower_bounds is not None:
            low = self.problem.lower_bounds
        else:
            low = self.problem.initial_lower_bounds
        if self.problem.upper_bounds is not None:
            high = self.problem.upper_bounds
        else:
            high = self.problem.initial_upper_bounds
        _dtype = self.dtype if judo.Backend.is_torch() else dtype.float32
        low = judo.to_backend(low)
        high = judo.to_backend(high)
        if len(low.shape) == 0:
            low = low * judo.ones(self.solution_length)
        if len(high.shape) == 0:
            high = high * judo.ones(self.solution_length)
        return Bounds(
            low=low,
            high=high,
            dtype=low.dtype if hasattr(low, "dtype") else _dtype,
            shape=self.solution_length,
        )

    def _get_function(self):
        """
        Return a function that sets the values of the evotorch :class:`SolutionBatch` \
        with the provided points and iterates the evotorch :class:`SearchAlgorithm` \
        to obtain new solutions.
        """

        def step_searcher(observs, rewards):
            self.algorithm.population.access_values()[:] = judo.to_torch(observs)
            self.algorithm.population.access_evals()[:] = judo.to_torch(rewards)
            self.algorithm.step()
            population = self.algorithm.population  # .clone()
            observs = judo.to_backend(population.access_values(keep_evals=True))
            rewards = judo.to_backend(population.access_evals())
            return observs, rewards

        return step_searcher

    def step(self, actions, observs, **kwargs):
        """
        Sum the target action to the observations to obtain the new points, and \
        evaluate the reward and boundary conditions.

        Returns:
            Dictionary containing the information of the new points evaluated.

             ``{"observs": new_points, "rewards": scalar array, \
             "oobs": boolean array}``

        """
        new_points_in = actions + observs if self._actions_as_perturbations else actions
        curr_reward = self.get("rewards").reshape(-1, 1)
        new_points, rewards = self.function(new_points_in, curr_reward)
        rewards = rewards.flatten()
        oobs = self.calculate_oobs(points=new_points, rewards=rewards)
        return dict(
            observs=new_points,
            rewards=rewards,
            oobs=oobs,
        )

    def reset(
        self,
        inplace: bool = True,
        root_walker: Optional[StateData] = None,
        states: Optional[StateData] = None,
        **kwargs,
    ) -> Union[None, StateData]:
        """
        Reset the :class:`Function` to the start of a new episode and updates its internal data.
        """
        if root_walker is None:
            new_points = self.sample_action(batch_size=self.swarm.n_actives)
            if self._x0 is not None:
                new_points[:] = self._x0
            elif self.start_same_pos:
                new_points[:] = new_points[0]
            actions = judo.zeros_like(new_points) if self._actions_as_perturbations else new_points
            curr_reward = self.get("rewards").reshape(-1, 1)
            new_points, rewards = self.function(new_points, curr_reward)
            rewards = rewards.flatten()
        else:
            new_points = self.get("observs")
            rewards = self.get("rewards")
            actions = (
                self.get("actions") if self._actions_as_perturbations else self.get("observs")
            )
        data = dict(
            actions=actions,
            observs=new_points,
            rewards=rewards,
        )
        if inplace:
            self.update(**data)
        else:
            return data
