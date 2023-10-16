from typing import Optional, Union

import judo
from judo import Backend, Bounds, dtype, random_state, tensor
import numpy.linalg

from fragile.core.api_classes import PolicyAPI, SwarmAPI
from fragile.core.typing import StateData, Tensor


class DummyPolicy(PolicyAPI):
    def select_actions(self, **kwargs) -> Tensor:
        return judo.zeros((self.swarm.n_actives), dtype=dtype.int64)


class RandomPlangym(PolicyAPI):
    """Policy that selects random actions from the environment action space."""

    def setup(self, swarm: SwarmAPI):
        """
        Setup the policy.

        Args:
            swarm (SwarmAPI): Swarm that will use this policy.

        Raises:
            TypeError: If the environment does not have a sample_action method or an action_space.
        """
        super(RandomPlangym, self).setup(swarm)
        if hasattr(self.swarm.env, "sample_action"):
            sample = self.swarm.env.sample_action
        elif hasattr(self.swarm.env, "action_space"):
            if hasattr(self.swarm.env.action_space, "select_dt"):
                sample = self.swarm.env.action_space.select_dt
            elif hasattr(self.swarm.env.action_space, "sample"):
                sample = self.swarm.env.action_space.sample
        elif hasattr(self.swarm.env, "plangym_env"):
            penv = self.swarm.env.plangym_env
            if hasattr(penv, "sample_action"):
                sample = penv.sample_action
            elif hasattr(penv, "action_space") and hasattr(penv.action_space, "select_dt"):
                sample = penv.action_space.select_dt
        else:
            raise TypeError("Environment does not have a sample_action method or an action_space")
        self._sample_func = sample

    def select_actions(self, **kwargs) -> list:
        """Sample a random action from the environment action space."""
        a = [self._sample_func() for _ in range(len(self.swarm))]
        return a


class Discrete(PolicyAPI):
    """A policy that selects discrete actions according to some probability distribution."""

    def __init__(self, actions: Optional[Tensor] = None, probs: Optional[Tensor] = None, **kwargs):
        """
        Initialize a :class:`Discrete` policy.

        Args:
            actions (Optional[Tensor], optional): The possible actions that can be
                taken by this policy. Defaults to None.. Defaults to None.
            probs (Optional[Tensor], optional): The probabilities of selecting each action.
                Not needed for uniform distributions. Defaults to None.. Defaults to None.
            **kwargs: Any other values that should be set for the policy.
        """
        super(Discrete, self).__init__(**kwargs)
        # TODO: parse all possible ways to infer actions, probs, and n_actions
        self.probs = probs
        self._n_actions = None
        self._actions = actions
        self._setup_params(actions)

    @property
    def n_actions(self) -> int:
        """The number of possible actions."""
        return self._n_actions

    @property
    def actions(self) -> Tensor:
        """The possible actions that can be taken by this policy."""
        return self._actions

    def select_actions(self, **kwargs) -> Tensor:
        """
        Select a random action from the possible actions.

        Returns:
           An array of shape (swarm.n_walkers,) containing the selected actions.
        """
        return random_state.choice(self.actions, p=self.probs, size=self.swarm.n_actives)

    def setup(self, swarm: SwarmAPI) -> None:
        """
        Sets up the policy, inferring any missing parameters.

        Args:
            swarm (SwarmAPI): The swarm that is using this policy.

        Raises:
            TypeError: If n_actions cannot be inferred.
        """
        self._swarm = swarm
        if self.n_actions is None:
            if hasattr(self.swarm.env, "n_actions"):
                self._n_actions = self.swarm.env.n_actions
            elif hasattr(self.swarm.env, "action_space"):
                self._n_actions = self.swarm.env.action_space.n
            else:
                raise TypeError("n_actions cannot be inferred.")
        self._setup_params(self.actions)

    def _setup_params(self, actions: Optional[Tensor] = None):
        """Setup the parameters of the policy."""
        if actions is None and self.n_actions is None and self.actions is not None:
            self._n_actions = len(self.actions)  # Try to set up n_actions using actions
        elif actions is None and self.n_actions is not None:  # setup actions with n_actions
            self._actions = judo.arange(self.n_actions) if self.actions is None else self.actions
        elif isinstance(actions, (list, tuple)) or judo.is_tensor(actions):
            self._actions = tensor(actions)
            self._n_actions = len(self.actions)
        elif actions is not None:  # Actions is an integer-like value
            self._n_actions = self.n_actions if self.n_actions is not None else int(actions)
            self._actions = judo.arange(self._n_actions)
        elif self.probs is not None:  # Try to infer values from probs
            self._n_actions = len(self.probs)
            self._actions = judo.arange(self._n_actions)


class BinarySwap(PolicyAPI):
    def __init__(self, n_swaps: int, n_actions: int = None, **kwargs):
        self._n_actions = n_actions
        self._n_swaps = n_swaps
        super(BinarySwap, self).__init__(**kwargs)

    @property
    def n_actions(self):
        return self._n_actions

    @property
    def n_swaps(self):
        return self._n_swaps

    def select_actions(self, **kwargs):
        from numba import jit
        import numpy

        @jit(nopython=True)
        def flip_values(actions: numpy.ndarray, flips: numpy.ndarray):
            for i in range(flips.shape[0]):
                for j in range(flips.shape[1]):
                    actions[i, flips[i, j]] = numpy.logical_not(actions[i, flips[i, j]])
            return actions

        observs = judo.to_numpy(self.get("observs"))
        with Backend.use_backend("numpy"):
            actions = judo.astype(observs, dtype.bool)
            flips = random_state.randint(0, self.n_actions, size=(observs.shape[0], self.n_swaps))
            actions = judo.astype(flip_values(actions, flips), dtype.int64)
        actions = tensor(actions)
        return actions

    def setup(self, swarm: SwarmAPI):
        self._swarm = swarm
        if self.n_actions is None:
            if hasattr(self.swarm.env, "n_actions"):
                self._n_actions = self.swarm.env.n_actions
            elif hasattr(self.swarm.env, "action_space"):
                self._n_actions = self.swarm.env.action_space.n
            else:
                raise TypeError("n_actions cannot be inferred.")


class ContinuousPolicy(PolicyAPI):
    """
    ContinuousPolicy implements a continuous action space policy for interacting \
    with the environment.

    Args:
        bounds (Bounds, optional): Action space bounds. If not provided, the bounds are obtained
            from the environment. Defaults to `None`.
        second_order (bool, optional): If `True`, the policy is considered second-order, and the \
            action sampled will be added to the last value. Defaults to `False`.
        step (float, optional): The step size for updating the actions. Defaults to 1.0.
        **kwargs: Additional keyword arguments for the base PolicyAPI class.

    Attributes:
        second_order (bool): If `True`, the policy is considered second-order.
        step (float): The step size for updating the actions.
        bounds (Bounds): Action space bounds.
        _env_bounds (Bounds): Environment action space bounds.
    """

    def __init__(self, bounds=None, second_order: bool = False, step: float = 1.0, **kwargs):
        """Initialize a :class:`ContinuousPolicy`."""
        self.second_order = second_order
        self.step = step
        self.bounds = bounds
        self._env_bounds = None
        if second_order:
            kwargs["inputs"] = {"actions": {"clone": True}, **kwargs.get("inputs", {})}
        super(ContinuousPolicy, self).__init__(**kwargs)

    @property
    def env_bounds(self) -> Bounds:
        """Returns the environment action space bounds."""
        return self._env_bounds

    def select_actions(self, **kwargs):
        """
        Implement the functionality for selecting actions in the derived class. This method is
        called during the act operation.

        Args:
            **kwargs: Additional keyword arguments required for selecting actions.
        """
        raise NotImplementedError()

    def act(self, inplace: bool = True, **kwargs) -> Union[None, StateData]:
        """
        Calculate the data needed to interact with the :class:`Environment`.

        Args:
            inplace (bool, optional): If `True`, updates the swarm state with the selected actions.
                                      If `False`, returns the selected actions. Defaults to `True`.
            **kwargs: Additional keyword arguments required for acting.

        Returns:
            Union[None, StateData]: A dictionary containing the selected actions if inplace is
                                    `False. Otherwise, returns `None`.
        """
        action_input = self._prepare_tensors(**kwargs)
        actions_data = self.select_actions(**action_input)
        if not isinstance(actions_data, dict):
            actions_data = {"actions": actions_data}
        actions = actions_data["actions"]
        if self.second_order:
            prev_actions = action_input["actions"]
            actions = prev_actions + actions * self.step
        actions_data["actions"] = self.env_bounds.clip(actions)
        if inplace:
            self.update(**actions_data)
        else:
            return actions_data

    def setup(self, swarm: SwarmAPI) -> None:
        """
        Set up the policy with the provided swarm object.

        Args:
            swarm (SwarmAPI): The swarm object to set up the policy with.

        Returns:
            None
        """
        super(ContinuousPolicy, self).setup(swarm)
        if self.bounds is None:
            if hasattr(self.swarm.env, "bounds"):
                self.bounds = self.swarm.env.bounds
            elif hasattr(self.swarm.env, "action_space"):
                self.bounds = Bounds.from_space(self.swarm.env.action_space)
            else:
                raise ValueError("Bounds is not defined and not present in the Environment.")
        if hasattr(self.swarm.env, "bounds"):
            self._env_bounds = self.swarm.env.bounds
        elif hasattr(self.swarm.env, "action_space"):
            self._env_bounds = Bounds.from_space(self.swarm.env.action_space)
        else:
            self._env_bounds = self.bounds


class ZeroContinuous(ContinuousPolicy):
    """
    Uniform policy samples actions equal to zero.

    Inherits from :class:`ContinuousPolicy`.
    """

    def select_actions(self, **kwargs) -> Tensor:
        """
        Select a vector of zeros.

        Args:
            **kwargs: Additional keyword arguments required for selecting actions.

        Returns:
            Tensor: Selected actions as a tensor.
        """
        shape = tuple([self.swarm.n_actives]) + self.bounds.shape
        return judo.zeros(shape, dtype=self.bounds.dtype)


class Uniform(ContinuousPolicy):
    """
    Uniform policy samples actions uniformly from the bounds of the action space.

    Inherits from :class:`ContinuousPolicy`.
    """

    def select_actions(self, **kwargs) -> Tensor:
        """
        Select actions by sampling uniformly from the action space bounds.

        Args:
            **kwargs: Additional keyword arguments required for selecting actions.

        Returns:
            Tensor: Selected actions as a tensor.
        """
        shape = tuple([self.swarm.n_actives]) + self.bounds.shape
        new_points = random_state.uniform(
            low=self.bounds.low,
            high=self.bounds.high,
            size=shape,
        )
        return new_points


class Gaussian(ContinuousPolicy):
    """
    The Gaussian policy samples actions from a Gaussian distribution.

    Inherits from :class:`ContinuousPolicy`.
    """

    def __init__(self, loc: float = 0.0, scale: float = 1.0, **kwargs):
        """
        Initialize a :class:`Gaussian` policy.

        Args:
            loc (float, optional): Mean of the policy. Defaults to 0.0.
            scale (float, optional): Standard deviation of the policy. Defaults to 1.0.
            **kwargs: Additional arguments.
        """
        super(Gaussian, self).__init__(**kwargs)
        self.loc = loc
        self.scale = scale

    def select_actions(self, **kwargs) -> Tensor:
        """
        Select actions by sampling from a Gaussian distribution.

        Args:
            **kwargs: Additional keyword arguments required for selecting actions.

        Returns:
            Tensor: Selected actions as a tensor.
        """
        shape = tuple([self.swarm.n_actives]) + self.bounds.shape
        new_points = random_state.normal(
            loc=self.loc,
            scale=self.scale,
            size=shape,
        )
        return new_points


class GaussianModulus(ContinuousPolicy):
    def __init__(self, loc: float = 0.0, scale: float = 1.0, **kwargs):
        super(GaussianModulus, self).__init__(**kwargs)
        self.loc = loc
        self.scale = scale

    def select_actions(self, **kwargs) -> Tensor:
        shape = tuple([self.swarm.n_actives]) + self.bounds.shape
        new_points = random_state.uniform(
            low=-1.0,
            high=1.0,
            size=shape,
        )
        new_points = new_points / numpy.linalg.norm(new_points, axis=1).reshape(-1, 1)

        modulus = random_state.normal(
            loc=self.loc,
            scale=self.scale,
            size=(self.swarm.n_actives, 1),
        )

        return new_points * modulus
