from copy import deepcopy
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

import judo
from judo import tensor
from judo.functions.api import API
from judo.functions.hashing import hasher

from fragile.core.typing import StateDict, Tensor


class State:
    """
    Data structure that handles the data defining a population of walkers.

    Each population attribute will be stored as a tensor with its first dimension
    (batch size) representing each walker.

    In order to define a tensor attribute, a `param_dict` dictionary needs to be
    specified using the following structure:

    Example:
        >>> attr_dict = {'name': {'shape': Optional[tuple|None], 'dtype': dtype},  # doctest: +SKIP
        ...             'biases': {'shape': (10,), 'dtype': float},
        ...             'vector': {'dtype': 'float32'},
        ...             'sequence': {'shape': None, 'dtype': 'float32'}
        ...             }

    Where tuple is a tuple indicating the shape of the desired tensor. The created
    arrays will be accessible through the `name_1` attribute of the class, or by
    indexing the class with `states["name_1"]`.

    If `size` is not defined, the attribute will be considered a vector of length
    `n_walkers`.


    Args:
        n_walkers (int): The number of items in the first dimension of the tensors.
        param_dict (StateDict): Dictionary defining the attributes of the tensors.

    Attributes:
        n_walkers (int): The number of walkers that this instance represents.
        param_dict (StateDict): A dictionary containing the shape and type of each
            walker's attribute.
        names (Tuple[str]): The name of the walker's attributes tracked by this
            instance.
        tensor_names (Set[str]): The name of the walker's attributes that correspond
            to tensors.
        list_names (Set[str]): The name of the walker's attributes that correspond
            to lists of objects.
        vector_names (Set[str]): The name of the walker's attributes that correspond
            to vectors of scalars.
    """

    def __init__(self, n_walkers: int, param_dict: StateDict):
        """
        Initialize a :class:`SwarmState`.

        Args:
             n_walkers: The number of items in the first dimension of the tensors.
             param_dict: Dictionary defining the attributes of the tensors.

        """

        def shape_is_vector(v):
            shape = v.get("shape", ())
            return not (shape is None or (isinstance(shape, tuple) and len(shape) > 0))

        self._param_dict = param_dict
        self._n_walkers = n_walkers
        self._names = tuple(param_dict.keys())
        self._list_names = set(k for k, v in param_dict.items() if v.get("shape", 1) is None)
        self._tensor_names = set(k for k in self.names if k not in self._list_names)
        self._vector_names = set(k for k, v in param_dict.items() if shape_is_vector(v))

    @property
    def n_walkers(self) -> int:
        """Return the number of walkers that this instance represents."""
        return self._n_walkers

    @property
    def param_dict(self) -> StateDict:
        """Return a dictionary containing the shape and type of each walker's attribute."""
        return self._param_dict

    @property
    def names(self) -> Tuple[str]:
        """Return the name of the walker's attributes tracked by this instance."""
        return self._names

    @property
    def tensor_names(self) -> Set[str]:
        """Return the name of the walker's attributes that correspond to tensors."""
        return self._tensor_names

    @property
    def list_names(self) -> Set[str]:
        """Return the name of the walker's attributes that correspond to lists of objects."""
        return self._list_names

    @property
    def vector_names(self) -> Set[str]:
        """Return the name of the walker's attributes that correspond to vectors of scalars."""
        return self._vector_names

    def __len__(self) -> int:
        """Length is equal to n_walkers."""
        return self._n_walkers

    def __setitem__(self, key, value: Union[Tuple, List, Tensor]):
        """
        Allow the class to set its attributes as if it was a dict.

        Args:
            key: Attribute to be set.
            value: Value of the target attribute.

        Returns:
            None.

        """
        setattr(self, key, value)

    def __getitem__(self, item: str) -> Union[Tensor, List[Tensor], "SwarmState"]:
        """
        Query an attribute of the class as if it was a dictionary.

        Args:
            item: Name of the attribute to be selected.

        Returns:
            The corresponding item.

        """
        return getattr(self, item)

    def __repr__(self) -> str:
        """Return a string that provides a nice representation of this instance attributes."""
        string = f"{self.__class__.__name__} with {self._n_walkers} walkers\n"
        for k, v in self.items():
            shape = v.shape if hasattr(v, "shape") else None
            new_str = "{}: {} {}\n".format(k, v.__class__.__name__, shape)
            string += new_str
        return string

    def __hash__(self) -> int:
        """Return an integer that represents the hash of the current instance."""
        return hasher.hash_state(self)

    def hash_attribute(self, name: str) -> int:
        """Return a unique id for a given attribute."""
        return hasher.hash_tensor(self[name])

    def hash_batch(self, name: str) -> List[int]:
        """Return a unique id for each walker attribute."""
        return hasher.hash_iterable(self[name])

    def get(self, name: str, default=None, raise_error: bool = True):
        """
        Get an attribute by key and return the default value if it does not exist.

        Args:
            name: Attribute to be recovered.
            default: Value returned in case the attribute is not part of state.
            raise_error: If True, raise AttributeError if name is not present in states.

        Returns:
            Target attribute if found in the instance, otherwise returns the
            default value.

        """
        if name not in self.names:
            if raise_error:
                raise AttributeError(f"{name} not present in states.")
            return default
        return self[name]

    def keys(self) -> "_dict_keys[str, Dict[str, Any]]":  # pyflakes: disable=F821
        """Return a generator for the values of the stored data."""
        return self.param_dict.keys()

    def values(self) -> Generator:
        """Return a generator for the values of the stored data."""
        return (self[name] for name in self.keys())

    def items(self) -> Generator:
        """Return a generator for the attribute names and the values of the stored data."""
        return ((name, self[name]) for name in self.keys())

    def itervals(self):
        """
        Iterate the states attributes by walker.

        Returns:
            Tuple containing all the names of the attributes, and the values that
            correspond to a given walker.

        """
        if len(self) <= 1:
            yield self.values()
            raise StopIteration
        for i in range(self.n_walkers):
            yield tuple(v[i] for v in self.values())

    def iteritems(self):
        """
        Iterate the states attributes by walker.

        Returns:
            Tuple containing all the names of the attributes, and the values that
            correspond to a given walker.

        """
        if self.n_walkers < 1:
            return self.values()
        for i in range(self.n_walkers):
            yield tuple(self.names), tuple(v[i] for v in self.values())

    def update(self, other: Union["SwarmState", Dict[str, Tensor]] = None, **kwargs) -> None:
        """
        Modify the data stored in this instance.

        Existing attributes will be updated, and no new attributes can be created.

        Args:
            other (Union[SwarmState, Dict[str, Tensor]], optional): Other SwarmState
                instance to copy upon update. Defaults to None.
            **kwargs: Extra key-value pairs of attributes to add to or modify the current state.

        Example:
            >>> s = State(2, {'name': {'shape': (3, 4), "dtype": bool}})
            >>> s.update({'name': np.ones((3, 4))})
            >>> len(s.names)
            1
            >>> s['name']
            array([[ True,  True,  True,  True],
                   [ True,  True,  True,  True],
                   [ True,  True,  True,  True]])
        """
        new_values = other.to_dict() if isinstance(other, SwarmState) else (other or {})
        new_values.update(kwargs)
        for name, val in new_values.items():
            val = self._parse_value(name, val)
            setattr(self, name, val)

    def to_dict(self) -> Dict[str, Union[Tensor, list]]:
        """Return the stored data as a dictionary of arrays."""
        return {name: value for name, value in self.items()}

    def copy(self) -> "SwarmState":
        """Crete a copy of the current instance."""
        new_states = self.__class__(n_walkers=self.n_walkers, param_dict=self.param_dict)
        new_states.update(**deepcopy(dict(self)))
        return new_states

    def reset(self) -> None:
        """Reset the values of the class"""
        try:
            data = self.params_to_arrays(self.param_dict, self.n_walkers)
        except Exception as e:
            print(self.param_dict)
            raise e
        self.update(data)

    def params_to_arrays(self, param_dict: StateDict, n_walkers: int) -> Dict[str, Tensor]:
        """
        Create a dictionary containing arrays specified by ``param_dict``, \
        the attribute dictionary.

        This method creates a dictionary containing arrays specified by the attribute dictionary.
        The attribute dictionary defines the attributes of the tensors, and ``n_walkers`` is
        the number of items in the first dimension of the data tensors.

        The method returns a dictionary with the same keys as ``param_dict``, containing
        arrays specified by the values in the attribute dictionary. The method achieves this by
        iterating through each item in the attribute dictionary, creating a copy of the value, and
        checking if the shape of the value is specified.

        If the shape is specified, the method initializes the tensor to zeros using the
        shape and dtype specified in the attribute dictionary. If the shape is not specified
        or if the key is in ``self.list_names``, the method initializes the value as a list of
        `None` with ``n_walkers`` items. If the key is ``'label'``, the method initializes
        the value as a list of empty strings with ``n_walkers`` items.

        Args:
            param_dict: Dictionary defining the attributes of the tensors.
            n_walkers: Number of items in the first dimension of the data tensors.

        Returns:
            Dictionary with the same names as the attribute dictionary, containing arrays specified
            by the values in the attribute dictionary.

        Example:
            >>> attr_dict = {'weights': {'shape': (10, 5), 'dtype': 'float32'},
            ...              'biases': {'shape': (10,), 'dtype': 'float32'},
            ...              'label': {'shape': None, 'dtype': 'str'},
            ...              'vector': {'dtype': 'float32'}}
            >>> n_walkers = 3
            >>> state = State(param_dict=attr_dict, n_walkers=n_walkers)
            >>> tensor_dict = state.params_to_arrays(attr_dict, n_walkers)
            >>> tensor_dict.keys()
            dict_keys(['weights', 'biases', 'label', 'vector'])
            >>> tensor_dict['weights'].shape
            (3, 10, 5)
            >>> tensor_dict['biases'].shape
            (3, 10)
            >>> tensor_dict['label']
            [None, None, None]
            >>> tensor_dict['vector'].shape
            (3,)
        """
        tensor_dict = {}
        for key, val in param_dict.items():
            val = deepcopy(val)
            shape = val.pop("shape", -1)  # If shape is not specified, assume it's a scalar vector.
            if shape is None or key in self.list_names:
                # If shape is None, assume it's not a tensor but a list.
                value = [None] * n_walkers
            else:  # Initialize the tensor to zeros. Assumes dtype is a valid argument.
                if shape == -1:
                    shape = (n_walkers,)
                else:
                    shape = (
                        (n_walkers, shape) if isinstance(shape, int) else ((n_walkers,) + shape)
                    )
                try:
                    value = API.zeros(shape, **val)
                except TypeError as e:
                    print("FAIL", key)
                    raise TypeError(f"Invalid dtype for {key}: {val['dtype']}") from e

            tensor_dict[key] = value
        return tensor_dict

    def _parse_value(self, name: str, value: Any) -> Any:
        """
        Ensure that the input value has correct dimensions and shape for a given attribute.

        Args:
            name (str): Name of the attribute.
            value (Any): New value to set to the attribute.

        Returns:
            Any: Parsed and validated value of the new state element.

        Example:
            >>> s = State(2, {'name': {'shape': (3, 4), "dtype": int}})
            >>> parsed_val = s._parse_value('name', [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
            >>> parsed_val
            array([[ 1,  2,  3,  4],
                   [ 5,  6,  7,  8],
                   [ 9, 10, 11, 12]])
        """
        if name in self.list_names:
            assert isinstance(value, list), (name, value)
            return value
        dtype = type(value[0])
        if name in self.names:
            dtype = self._param_dict[name].get("dtype", dtype)
        else:
            raise NotImplementedError(f"Name {name} must be present in self.names")
        try:
            tensor_val = tensor(value, dtype=dtype)
        except ValueError as e:
            raise ValueError(f"Name {name} failed conversion to tensor:") from e
        except TypeError as e:
            raise TypeError(
                (f"Name {name} with type {dtype} and value {value} failed conversion to tensor:"),
            ) from e
        return tensor_val


class SwarmState(State):
    """
    A dictionary-style container for storing the current state of the swarm. It allows you
    to update the status and metadata of the walkers in the swarm.

    The keys of the instance must be its attributes. The attribute value can be of \
    any type (tensor, list or any python object). Lists and Tensors can have different \
    len than ``n_walkers`` if necessary, but tensors should have the same number of \
    rows as walkers (whether active or not).

    Args:
        n_walkers (int): Number of walkers
        param_dict (StateDict): Dictionary defining the attributes of the tensors.

    Example:
        >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
        >>> s = SwarmState(n_walkers=100, param_dict=param_dict)
    """

    def __init__(self, n_walkers: int, param_dict: StateDict):
        """
        Initialize a :class:`SwarmState`.

        Args:
             n_walkers: The number of items in the first dimension of the tensors.
             param_dict: Dictionary defining the attributes of the tensors.

        """
        self._clone_names = set(k for k, v in param_dict.items() if v.get("clone"))
        super(SwarmState, self).__init__(n_walkers=n_walkers, param_dict=param_dict)
        self._actives = judo.ones(self.n_walkers, dtype=judo.dtype.bool)
        self._n_actives = int(self.n_walkers)

    @property
    def clone_names(self) -> Set[str]:
        """Return the name of the attributes that will be copied when a walker clones."""
        return self._clone_names

    @property
    def actives(self) -> Tensor:
        """Get the active walkers indices."""
        return self._actives

    @property
    def n_actives(self) -> int:
        """Get the number of active walkers."""
        return self._n_actives

    def clone(self, will_clone, compas_clone, clone_names):
        """Clone all the stored data according to the provided index."""
        for name in clone_names:
            values = self[name]
            if name in self.tensor_names:
                self[name][will_clone] = values[compas_clone][will_clone]
            else:
                self[name] = [
                    deepcopy(values[comp]) if wc else deepcopy(val)
                    for val, comp, wc in zip(values, compas_clone, will_clone)
                ]

    def export_walker(self, index: int, names: Optional[List[str]] = None, copy: bool = False):
        """
        Export the data of a walker at index `index` as a dictionary.

        Args:
            index (int): The index of the target walker.
            names (Optional[List[str]], optional): The list of attribute names
                to be included in the output. If None,
                all attributes will be included. Defaults to None.
            copy (bool, optional): If True, the returned dictionary will be a copy of the
                original data. Defaults to False.

        Returns:
            Dict[str, Union[Tensor, numpy.ndarray]]: A dictionary containing the \
            requested attributes and their corresponding values for the specified walker.

        Examples:
            >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
            >>> s = SwarmState(n_walkers=10, param_dict=param_dict)
            >>> s.reset()
            >>> walker_dict = s.export_walker(0, names=["x"])
            >>> print(walker_dict)  # doctest: +NORMALIZE_WHITESPACE
            {'x': array([[[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]])}
        """

        def _get_value(v, k):
            val = v[[index]] if k in self.tensor_names else [v[index]]
            if copy:
                val = deepcopy(val)
            return val

        names = names if names is not None else self.keys()
        return {k: _get_value(v, k) for k, v in self.items() if k in names}

    def import_walker(self, data: Dict[str, Tensor], index: int = 0) -> None:
        """Takes data dictionary and imports it into state at indice `index`.

        Args:
            data (Dict): Dictionary containing the data to be imported.
            index (int, optional): Walker index to receive the data. Defaults to 0.

        Examples:
            >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
            >>> s = SwarmState(n_walkers=10, param_dict=param_dict)
            >>> s.reset()
            >>> data = {"x": judo.ones((3, 4), dtype=int)}
            >>> s.import_walker(data, index=0)
            >>> s.get("x")[0, 0, :3]
            array([1, 1, 1])
        """
        for name, tensor_ in data.items():
            if name in self.tensor_names:
                self[name][[index]] = judo.copy(tensor_)
            else:
                self[name][index] = deepcopy(tensor_[0])

    def reset(self, root_walker: Optional[Dict[str, Tensor]] = None) -> None:
        """
        Completely resets both current and history data that have been held in state.

        Optionally can take a root value to reset individual attributes.

        Args:
            root_walker (Optional[Dict[str, Tensor]], optional): The initial state when resetting.

        Examples:
            >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
            >>> s = SwarmState(n_walkers=10, param_dict=param_dict)
            >>> s.reset()
            >>> walker_dict = s.export_walker(0, names=["x"])
            >>> print(walker_dict["x"].shape)  # doctest: +NORMALIZE_WHITESPACE
            (1, 3, 4)
        """
        self._actives = judo.ones(self.n_walkers, dtype=judo.dtype.bool)
        self._n_actives = int(self.n_walkers)
        super(SwarmState, self).reset()
        if root_walker:
            for name, array in root_walker.items():
                if name in self.tensor_names:
                    self[name][:] = judo.copy(array)
                else:
                    self[name] = deepcopy([array[0] for _ in range(self.n_walkers)])

    def get(self, name: str, default=None, raise_error: bool = True, inactives: bool = False):
        """
        Get an attribute by key and return the default value if it does not exist.

        Args:
            name: Attribute to be recovered.
            default: Value returned in case the attribute is not part of state.
            raise_error: If True, raise AttributeError if name is not present in states.
            inactives: Whether to update the walkers marked as inactive.

        Returns:
            Target attribute if found in the instance, otherwise returns the
            default value.

        Examples:
            >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
            >>> s = SwarmState(n_walkers=10, param_dict=param_dict)
            >>> s.reset()
            >>> print(s.get("x").shape)
            (10, 3, 4)


        """
        value = super(SwarmState, self).get(name=name, default=default, raise_error=raise_error)
        if inactives or name not in self.names:
            return value
        try:
            return (
                value[self.actives]
                if name not in self.list_names
                else [x for x, active in zip(value, self.actives) if active]
            )
        except Exception as e:
            print("NAME", name, self.actives.shape, value.shape)
            raise e

    def _update_active_list(self, current_vals, new_vals):
        """Update the list of active walkers."""
        new_ix = 0
        updated_vals = []
        for active, curr in zip(self.actives, current_vals):
            if active:
                updated_vals.append(new_vals[new_ix])
                new_ix += 1
            else:
                updated_vals.append(curr)
        return updated_vals

    def update(
        self,
        other: Union["SwarmState", Dict[str, Tensor]] = None,
        inactives: bool = False,
        **kwargs,
    ) -> None:
        """
        Modify the data stored in the SwarmState instance.

        Existing attributes will be updated, and new attributes will be created if needed.

        Args:
            other: State class that will be copied upon update.
            inactives: Whether to update the walkers marked as inactive.
            **kwargs: It is possible to specify the update as name value attributes,
                where name is the name of the attribute to be updated, and value
                is the new value for the attribute.
        Returns:
            None.

        Examples:
            >>> param_dict = {"x": {"shape": (3, 4), "dtype": int}}
            >>> s = SwarmState(n_walkers=10, param_dict=param_dict)
            >>> s.reset()
            >>> s.update(x=judo.ones((10, 3, 4), dtype=int))
            >>> print(s.get("x")[0,0,0])
            1
        """
        if other is not None:
            return super(SwarmState, self).update(other=other, **kwargs)
        # FIXME (guillemdb): This does not make sense because it executes only if other is None.
        new_values = other.to_dict() if isinstance(other, SwarmState) else (other or {})
        new_values.update(kwargs)
        for name, val in new_values.items():
            try:
                if name == "actives":
                    continue
                val = self._parse_value(name, val)
                is_actives_vector = (len(val) == self._n_actives) or (
                    judo.is_tensor(val) and val.shape[0] == self._n_actives
                )
                if is_actives_vector and hasattr(self, name) and not inactives:
                    all_vals = getattr(self, name)
                    if isinstance(all_vals, list):
                        new_vals = self._update_active_list(all_vals, val)
                        assert len(new_vals) == self.n_walkers
                        setattr(self, name, new_vals)
                    else:
                        try:
                            all_vals[self.actives] = val
                        except RuntimeError:
                            all_vals[self.actives] = judo.copy(val)
                        setattr(self, name, all_vals)

                elif inactives or self.n_actives == self.n_walkers or len(val) == self.n_walkers:
                    setattr(self, name, val)
                else:
                    raise ValueError(f"failed to setup data {name} {val.shape}")
            except Exception as e:
                raise ValueError(f"failed to setup data {name} {val.shape}") from e

    def update_actives(self, actives) -> None:
        """
        Set the walkers marked as active.

        Example:
            To set the first 10 walkers as active, call the function with a tensor of size
            equal to the number of walkers, where the first ten elements are `True`
            and the remaining elements are `False`:

            >>> param_dict = {"vector":{"dtype":int}}
            >>> s = SwarmState(n_walkers=20, param_dict=param_dict)
            >>> active_walkers = np.concatenate([np.ones(10), np.zeros(10)]).astype(bool)
            >>> s.update_actives(active_walkers)

            This will mark those walkers as active, and any attribute updated with inactives=False
            (this is the default) will only modify the data from those walkers.
        """
        self._actives = actives
        self._n_actives = int(actives.sum())
