"""This module contains the :class:`PlangymEnv` class."""
import copy
from typing import Any, Callable, Optional, Tuple, Union

import judo
from judo import Bounds, dtype, random_state, typing
import numpy


try:
    from plangym.core import PlangymEnv as _PlangymEnv
except ImportError:
    _PlangymEnv = Any

from fragile.core.api_classes import EnvironmentAPI, SwarmAPI
from fragile.core.typing import InputDict, StateData, StateDict, Tensor


class PlangymEnv(EnvironmentAPI):
    r"""
    Wrapper class for running a Swarm to solve planning tasks in a Plangym environment.

    This class allows running gymnasium simulations compatible with the plangym API.
    It can be used as an interface for passing states and actions, and receiving
    observation and reward information from the environment.

    Attributes:
        plangym_env (Env): The Plangym environment this instance is wrapped around.
        _has_terminals (bool): `True` if the environment has terminal signals, `False` otherwise.
        _has_rgb (bool): `True` if the environment includes RGB color data, `False` otherwise.

    Examples:
        >>> import plangym
        >>> plangym_env = plangym.make("CartPole-v0")
        >>> env = PlangymEnv(plangym_env)
    """

    def __init__(
        self,
        plangym_env: _PlangymEnv,
        swarm: Optional[SwarmAPI] = None,
    ):
        r"""
        Initialize a new instance of the PlangymEnv class.

        Args:
            plangym_env (_PlangymEnv): The underlying Plangym environment.
            swarm (Optional[SwarmAPI], optional): The swarm to use in this environment.
                Defaults to None.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
        """
        self._plangym_env = plangym_env
        state, obs = plangym_env.reset()
        *_, infos = plangym_env.step(plangym_env.sample_action())
        self._has_rgb = "rgb" in infos
        self.rgb_shape = infos["rgb"].shape if self.has_rgb else None
        states_shape = None if not plangym_env.STATE_IS_ARRAY else state.shape
        states_dtype = type(state) if not plangym_env.STATE_IS_ARRAY else state.dtype
        self._has_terminals = (
            hasattr(self.plangym_env, "possible_to_win") and self.plangym_env.possible_to_win
        )

        self._states_shape = states_shape
        self._states_dtype = states_dtype
        super(PlangymEnv, self).__init__(
            swarm=swarm,
            observs_dtype=obs.dtype,
            observs_shape=obs.shape,
            action_shape=plangym_env.action_space.shape,
            action_dtype=plangym_env.action_space.dtype,
        )

    @property
    def states_shape(self) -> tuple:
        """
        Returns the shape of the states tensor.

        Returns:
            tuple: The shape of the states tensor.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> env.states_shape
            (4,)
        """
        return self._states_shape

    @property
    def states_dtype(self):
        """
        Returns the data type of the states tensor.

        Returns:
            judo.dtype: The data type of the states tensor.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> env.states_dtype
            dtype('float64')
        """
        return self._states_dtype

    @property
    def plangym_env(self) -> _PlangymEnv:
        """
        Returns the underlying Plangym environment.

        Returns:
            plangym.PlangymEnv: The underlying :class:`plangym.Plangym` environment.
        """
        return self._plangym_env

    @property
    def inputs(self) -> InputDict:
        """
        Returns a dictionary of input data for the environment.

        Returns:
            InputDict: A dictionary of input data for the environment.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> env.inputs  # doctest: +NORMALIZE_WHITESPACE
            {'actions': {},
             'states': {'clone': True},
             'dt': {'optional': True, 'default': 1}}
        """
        plangym_inputs = {"states": {"clone": True}, "dt": {"optional": True, "default": 1}}
        return {**super(PlangymEnv, self).inputs, **plangym_inputs}

    @property
    def outputs(self) -> Tuple[str, ...]:
        """
        Returns a tuple of output variables for the environment.

        Returns:
            Tuple[str, ...]: A tuple of output variables for the environment.
        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> tuple(sorted(env.outputs))
            ('infos', 'n_steps', 'observs', 'oobs', 'rewards', 'states')
        """
        outputs = ("n_steps", "infos", "states")
        if self._has_terminals:
            outputs = outputs + ("terminals",)
        if self.has_rgb:
            outputs = outputs + ("rgb",)
        return super(PlangymEnv, self).outputs + outputs

    @property
    def param_dict(self) -> StateDict:
        """
        Returns a dictionary of parameters for the environment.

        Returns:
            StateDict: A dictionary of parameters for the environment.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> print(env.param_dict)  # doctest: +NORMALIZE_WHITESPACE
            {'observs': {'shape': (4,), 'dtype': dtype('float32')},
             'rewards': {'dtype': <class 'numpy.float32'>},
             'oobs': {'dtype': <class 'numpy.bool_'>},
             'actions': {'shape': (), 'dtype': dtype('int64')},
             'n_steps': {'dtype': <class 'numpy.int32'>},
             'infos': {'shape': None, 'dtype': <class 'dict'>},
             'states': {'shape': (4,), 'dtype': dtype('float64')}}
        """
        plangym_params = {
            "n_steps": {"dtype": dtype.int32},
            "infos": {"shape": None, "dtype": dict},
            "states": {"shape": self.states_shape, "dtype": self.states_dtype},
        }
        if self._has_terminals:
            plangym_params["terminals"] = {"dtype": dtype.bool}
        if self.has_rgb:
            plangym_params["rgb"] = {"shape": self.rgb_shape, "dtype": dtype.uint8}
        return {**super(PlangymEnv, self).param_dict, **plangym_params}

    @property
    def has_rgb(self) -> bool:
        """
        Return whether the environment includes RGB color data or not.

        Returns:
            bool: `True` if the environment includes RGB color data, `False` otherwise.
        """
        return self._has_rgb

    def __getattr__(self, item):
        return getattr(self.plangym_env, item)

    def step(self, actions: Tensor, states: Tensor, dt: int = 1) -> StateDict:
        """
        Takes an action in the environment and returns information about the new state.

        Args:
            actions (Tensor): The actions to take. Shape should be (n_walkers,) + actions_shape.
            states (Tensor): The states to act on. Shape should be (n_walkers,) + state_shape.
            dt (int, optional): The number of simulation steps to take per gym step. Defaults to 1.

        Returns:
            Dict[str, Any]: A dictionary containing the following keys:
                - observs (Tensor): The observatons from the last step.
                    Has shape (n_walkers,) + observation_shape.
                - rewards (Tensor): The rewards received from the last step.
                    Has shape (n_walkers,).
                - oobs (List[Any]): List of episode endings from the last step.
                    Length is n_walkers.
                - infos (List[Dict[str, Any]]): Additional information about the last step.
                    Length is n_walkers.
                - n_steps (List[int]): The number of simulation steps taken in the last step.
                    Length is n_walkers.
                - states (Tensor): The new states after taking the given actions.
                    Has shape (n_walkers,) + state_shape.
                - terminals (List[bool], optional): List of raw terminal values if available.
                    Length is n_walkers. Only returned if the environment has terminal signals.
                - rgb (Tensor, optional): The rendered RGB output of the last step. Only returned
                    by some environments. Has shape (n_walkers, h, w, c).

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> env = PlangymEnv(plangym_env)
            >>> n_walkers = 3
            >>> actions = np.array([plangym_env.sample_action() for i in range(n_walkers)])
            >>> state_dict = env.reset(n_walkers=n_walkers, inplace=False)
            >>> result = env.step(actions, state_dict["states"])
            >>> type(result)
            <class 'dict'>
            >>> tuple(sorted(result.keys()))
            ('infos', 'n_steps', 'observs', 'oobs', 'rewards', 'states')
        """
        step_data = self.plangym_env.step_batch(actions=actions, states=states, dt=dt)
        new_states, observs, rewards, oobs, infos = step_data
        n_steps = [info.get("n_steps", 1) for info in infos]
        states_data = dict(
            observs=observs,
            rewards=rewards,
            oobs=oobs,
            infos=infos,
            n_steps=n_steps,
            states=new_states,
        )
        if self._has_terminals:
            terminals = [info["terminal"] for info in infos] if "terminal" in infos[0] else oobs
            states_data["terminals"] = terminals
        if self.has_rgb:
            rgbs = [info["rgb"] for info in infos]
            states_data["rgb"] = rgbs
        return states_data

    def reset(
        self,
        inplace: bool = True,
        root_walker: Optional[StateData] = None,
        states: Optional[StateData] = None,
        n_walkers: Optional[int] = None,
        **kwargs,
    ):
        """
        Resets the environment(s) to its initial state.

        This method resets the states and observables of the environment(s)
        stored in the object's `swarm.state` attribute to their initial values.

        Args:
            inplace (bool): If True, updates the current instance state with
                the reset values. If False, returns a new dictionary with
                the states, observables and info dicts.
            root_walker (Optional[StateData]): The state information to reset from,
                if not using default initial state.
                Defaults to None.
            states (Optional[StateData]): The states to use as initial values, if
                provided, it will ignore `root_walker`. Defaults to None.
            n_walkers (Optional[int]): The number of walkers to reset. Defaults to None.
            **kwargs: Other parameters that might be necessary
                depending on the specific implementation of the class.

        Returns:
            Optional[StateDict]: A StateDict containing the states,
            observables, and info dict after the reset. Only returned
            when `inplace` is False.

        Examples:
            >>> import plangym
            >>> plangym_env = plangym.make("CartPole-v0")
            >>> n_walkers = 3
            >>> # Reset environment and update the state of the swarm:
            >>> env = PlangymEnv(plangym_env, swarm=None)
            >>> env.reset(n_walkers=n_walkers)  # Fails because there is no swarm
            Traceback (most recent call last):
            ...
            AttributeError: 'NoneType' object has no attribute 'state'

            >>> # Get reset data without modifying current instance:
            >>> env = PlangymEnv(plangym_env)
            >>> reset_data = env.reset(n_walkers=n_walkers, inplace=False)
            >>> tuple(sorted(reset_data.keys()))
            ('infos', 'observs', 'rewards', 'states')
        """
        n_walkers = len(self.swarm) if n_walkers is None else n_walkers
        # TODO: add support for defaults in param_dict to avoid this mess.
        default_value = -numpy.inf
        if self.swarm is not None:
            default_value = numpy.inf if self.swarm.minimize else -numpy.inf
        if root_walker is None:
            state, observs = self.plangym_env.reset()
            new_states = [copy.deepcopy(state) for _ in range(n_walkers)]
            new_observs = [copy.deepcopy(observs) for _ in range(n_walkers)]
        else:  # TODO: test this
            new_states = self.get("states")
            new_observs = self.get("observs")
        infos = [{} for _ in range(n_walkers)]
        rewards = judo.ones(n_walkers) * default_value
        if inplace:
            self.update(
                states=new_states,
                observs=new_observs,
                infos=infos,
                rewards=rewards,
                inactives=True,
            )
        else:
            return dict(states=new_states, observs=new_observs, rewards=rewards, infos=infos)


class Function(EnvironmentAPI):
    """
    Environment that represents an arbitrary mathematical function bounded in a \
    given interval.
    """

    default_inputs = {"actions": {}, "observs": {"clone": True}}

    def __init__(
        self,
        function: Callable[[typing.Tensor], typing.Tensor],
        bounds: Union[Bounds, "gym.spaces.box.Box"],
        custom_domain_check: Callable[[typing.Tensor, typing.Tensor, int], typing.Tensor] = None,
        actions_as_perturbations: bool = True,
        start_same_pos: bool = False,
        x0: Tensor = None,
    ):
        """
        Initialize a :class:`Function`.

        Args:
            function: Callable that takes a batch of vectors (batched across \
                      the first dimension of the array) and returns a vector of \
                      typing.Scalar. This function is applied to a batch of walker \
                      observations.
            bounds: :class:`Bounds` that defines the domain of the function.
            custom_domain_check: Callable that checks points inside the bounds \
                    to know if they are in a custom domain when it is not just \
                    a set of rectangular bounds. It takes a batch of points as \
                    input and returns an array of booleans. Each ``True`` value \
                    indicates that the corresponding point is **outside**  the \
                    ``custom_domain_check``.
            actions_as_perturbations: If ``True`` the actions are interpreted as \
                    perturbations that will be applied to the past states. \
                    If ``False`` the actions are interpreted as the new states to \
                    be evaluated.

        """
        if not isinstance(bounds, Bounds) and bounds.__class__.__name__ != "Box":
            raise TypeError(f"Bounds needs to be an instance of Bounds or Box, found {bounds}")
        self.function = function
        self.bounds = bounds if isinstance(bounds, Bounds) else Bounds.from_space(bounds)
        self._action_space = self.bounds.to_space()
        self.custom_domain_check = custom_domain_check
        self._actions_as_perturbations = actions_as_perturbations
        self._x0 = x0
        self.start_same_pos = start_same_pos
        super(Function, self).__init__(
            observs_shape=self.shape,
            observs_dtype=dtype.float32,
            action_dtype=dtype.float32,
            action_shape=self.shape,
        )

    @property
    def n_dims(self) -> int:
        """Return the number of dimensions of the function to be optimized."""
        return len(self.bounds)

    @property
    def shape(self) -> Tuple[int, ...]:
        """Return the shape of the environment."""
        return self.bounds.shape

    @property
    def action_space(self) -> "gym.spaces.box.Box":
        """Action space with the same characteristics as self.bounds."""
        return self._action_space

    @classmethod
    def from_bounds_params(
        cls,
        function: Callable,
        shape: tuple = None,
        high: Union[int, float, typing.Tensor] = numpy.inf,
        low: Union[int, float, typing.Tensor] = numpy.NINF,
        custom_domain_check: Callable[[typing.Tensor], typing.Tensor] = None,
    ) -> "Function":
        """
        Initialize a function defining its shape and bounds without using a :class:`Bounds`.

        Args:
            function: Callable that takes a batch of vectors (batched across \
                      the first dimension of the array) and returns a vector of \
                      typing.Scalar. This function is applied to a batch of walker \
                      observations.
            shape: Input shape of the solution vector without taking into account \
                    the batch dimension. For example, a two-dimensional function \
                    applied to a batch of 5 walkers will have shape=(2,), even though
                    the observations will have shape (5, 2)
            high: Upper bound of the function domain. If it's a typing.Scalar it will \
                  be the same for all dimensions. If it's a numpy array it will \
                  be the upper bound for each dimension.
            low: Lower bound of the function domain. If it's a typing.Scalar it will \
                  be the same for all dimensions. If it's a numpy array it will \
                  be the lower bound for each dimension.
            custom_domain_check: Callable that checks points inside the bounds \
                    to know if they are in a custom domain when it is not just \
                    a set of rectangular bounds.

        Returns:
            :class:`Function` with its :class:`Bounds` created from the provided arguments.

        """
        if (
            not (judo.is_tensor(high) or isinstance(high, (list, tuple)))
            and not (judo.is_tensor(low) or isinstance(low, (list, tuple)))
            and shape is None
        ):
            raise TypeError("Need to specify shape or high or low must be an array.")
        bounds = Bounds(high=high, low=low, shape=shape)
        return Function(function=function, bounds=bounds, custom_domain_check=custom_domain_check)

    def __repr__(self):
        text = "{} with function {}, obs shape {},".format(
            self.__class__.__name__,
            self.function.__name__,
            self.shape,
        )
        return text

    def step(self, actions, observs, **kwargs) -> StateData:
        """

        Sum the target action to the observations to obtain the new points, and \
        evaluate the reward and boundary conditions.

        Returns:
            Dictionary containing the information of the new points evaluated.

             ``{"states": new_points, "observs": new_points, "rewards": typing.Scalar array, \
             "oobs": boolean array}``

        """
        new_points = actions + observs if self._actions_as_perturbations else actions
        rewards = self.function(new_points).flatten()
        oobs = self.calculate_oobs(points=new_points, rewards=rewards)
        return dict(observs=new_points, rewards=rewards, oobs=oobs)

    def reset(
        self,
        inplace: bool = True,
        root_walker: Optional[StateData] = None,
        states: Optional[StateData] = None,
        **kwargs,
    ) -> Union[None, StateData]:
        """
        Reset the :class:`Function` to the start of a new episode and returns \
        an :class:`StatesEnv` instance describing its internal state.
        """
        if root_walker is None:
            new_points = self.sample_action(batch_size=self.swarm.n_actives)
            if self._x0 is not None:
                new_points[:] = self._x0
            elif self.start_same_pos:
                new_points[:] = new_points[0]
            actions = judo.zeros_like(new_points) if self._actions_as_perturbations else new_points
            rewards = self.function(new_points).flatten()
        else:
            new_points = self.get("observs")
            rewards = self.get("rewards")
            actions = (
                self.get("actions") if self._actions_as_perturbations else self.get("observs")
            )
        if inplace:
            self.update(observs=new_points, rewards=rewards, actions=actions)
        else:
            return dict(observs=new_points, rewards=rewards, actions=actions)

    def calculate_oobs(self, points: typing.Tensor, rewards: typing.Tensor) -> typing.Tensor:
        """
        Determine if a given batch of vectors lie inside the function domain.

        Args:
            points: Array of batched vectors that will be checked to lie inside \
                    the :class:`Function` bounds.
            rewards: Array containing the rewards of the current walkers.

        Returns:
            Array of booleans of length batch_size (points.shape[0]) that will \
            be ``True`` if a given point of the batch lies outside the bounds, \
            and ``False`` otherwise.

        """
        oobs = judo.logical_not(self.bounds.contains(points)).flatten()
        if self.custom_domain_check is not None:
            points_in_bounds = judo.logical_not(oobs)
            oobs[points_in_bounds] = self.custom_domain_check(
                points[points_in_bounds],
                rewards[points_in_bounds],
                len(rewards),
            )
        return oobs

    def sample_action(self, batch_size: int) -> typing.Tensor:
        """
        Return a matrix of points sampled uniformly from the :class:`Function` \
        domain.

        Args:
            batch_size: Number of points that will be sampled.

        Returns:
            Array containing ``batch_size`` points that lie inside the \
            :class:`Function` domain, stacked across the first dimension.

        """
        shape = tuple([batch_size])
        if judo.Backend.is_numpy():
            shape = shape + self.shape
        new_points = random_state.uniform(
            low=judo.astype(self.bounds.low, judo.float),
            high=judo.astype(self.bounds.high, judo.float32),
            size=shape,
        )
        return new_points
