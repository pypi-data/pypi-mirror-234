from typing import Any, Dict

import judo
from judo.data_types import dtype
import numpy as np
import pytest

from fragile.core.state import State


param_dict_list = {
    "list_param_int": {"shape": None, "dtype": int},
    "list_param_list": {"shape": None, "dtype": list},
    "list_param_dict": {"shape": None, "dtype": dict},
    "list_param_set": {"shape": None, "dtype": set},
}

param_dict_vector = {
    "vec_float_16": {"dtype": dtype.float16},
    "vec_float_32": {"dtype": dtype.float32},
    "vec_bool": {"dtype": dtype.bool},
    "vec_int_shape": {"shape": tuple(), "dtype": dtype.int64},
}

param_dict_tensor = {
    "tensor_float_20_17": {"shape": (20, 17), "dtype": dtype.float16},
    "tensor_float_1": {"shape": (1,), "dtype": dtype.float32},
    "tensor_int_1_17_5": {"shape": (1, 17, 5), "dtype": dtype.int64},
}


param_dict_mix = {
    "observs": {"shape": (20, 17), "dtype": dtype.float16},
    "rewards": {"dtype": dtype.float32},
    "oobs": {"dtype": dtype.bool},
    "actions": {"shape": (1, 17), "dtype": dtype.int64},
    "list_param": {"shape": None, "dtype": int},
}

param_dict_examples = [param_dict_list, param_dict_vector, param_dict_tensor, param_dict_mix]
param_dict_ids = ["list_param_dict", "vector_param_dict", "tensor_param_dict", "mix_param_dict"]


@pytest.fixture(params=param_dict_examples, ids=param_dict_ids)
def param_dict(request) -> Dict[str, Any]:
    return request.param


@pytest.fixture()
def n_walkers() -> int:
    return 7


class TestState:
    def test_init(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name in param_dict.keys():
            assert name in state.names

    def test_getitem(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name in param_dict.keys():
            assert hasattr(state, name)
            assert state[name] is not None
            assert np.array_equal(judo.to_numpy(state[name]), judo.to_numpy(state.get(name)))

    def test_setitem(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name in param_dict.keys():
            add_val = [1] if isinstance(state[name], list) else 1
            new_value = state[name] + add_val
            state[name] = new_value
            assert np.array_equal(judo.to_numpy(state[name]), judo.to_numpy(new_value))

    def test_reset(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name, value in param_dict.items():
            assert len(state[name]) == n_walkers
            if "dtype" in value and not isinstance(state[name], list):
                assert state[name].dtype == value["dtype"]
            if "shape" in value and value["shape"] is not None:
                assert state[name].shape == (n_walkers,) + value["shape"]
            elif value.get("shape", False) is not None:
                assert state[name].shape == (n_walkers,)

    def __test_setitem_wrong_shape(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name in param_dict.keys():
            if "shape" in param_dict[name]:
                with pytest.raises(ValueError):
                    state[name] = [1] * (len(param_dict[name]["shape"]) + 1)

    def __test_setitem_wrong_dtype(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        for name in param_dict.keys():
            if "dtype" in param_dict[name]:
                with pytest.raises(TypeError):
                    state[name] = "wrong_dtype"

    def test_copy(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        copy_state = state.copy()
        assert copy_state is not state
        assert copy_state.names == state.names
        for name in param_dict.keys():
            assert np.array_equal(judo.to_numpy(copy_state[name]), judo.to_numpy(state[name]))

    def test_copy_change(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        copy_state = state.copy()
        for name in param_dict.keys():
            if isinstance(state[name], (int, float, bool)):
                copy_state[name] += 1
                assert copy_state[name] != state[name]
            elif isinstance(state[name], (list, tuple, set)):
                copy_state[name].append(1)
                assert len(copy_state[name]) != len(state[name])
            elif isinstance(state[name], dict):
                copy_state[name]["new_key"] = "new_value"
                assert len(copy_state[name]) != len(state[name])

    def test_len(self, param_dict, n_walkers):
        state = State(n_walkers=n_walkers, param_dict=param_dict)
        state.reset()
        n_walkers = len(state)
        assert n_walkers == state.n_walkers
