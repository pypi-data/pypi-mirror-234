import judo
import numpy as np
import pytest

from fragile.core.state import State


@pytest.fixture(scope="module")
def state():
    s = State(n_walkers=3, param_dict={"x": {"shape": None, "dtype": int}})
    s.reset()
    return s


def test_values(state):
    vals = list(state.values())
    assert np.array_equal(vals, [[None, None, None]]), vals


def test_items(state):
    param_dict = dict(state.param_dict)
    param_dict["y"] = {"shape": None, "dtype": int}
    state = State(n_walkers=state.n_walkers, param_dict=param_dict)
    state.update(x=[1, 2, 3], y=[4, 5, 6])
    my_value = np.array(list(state.items()), dtype=object)
    test_value = np.array([("x", [1, 2, 3]), ("y", [4, 5, 6])], dtype=object)
    assert np.array_equal(my_value, test_value)


def test_itervals(state):
    param_dict = dict(state.param_dict)
    param_dict["y"] = {"shape": None, "dtype": int}
    state = State(n_walkers=state.n_walkers, param_dict=param_dict)
    state.update(x=[1, 2, 3], y=[4, 5, 6])
    assert np.array_equal(list(state.itervals()), [(1, 4), (2, 5), (3, 6)])


def test_iteritems(state):
    param_dict = dict(state.param_dict)
    param_dict["y"] = {"shape": None, "dtype": int}
    state = State(n_walkers=state.n_walkers, param_dict=param_dict)
    state.update(x=[1, 2, 3], y=[4, 5, 6])
    assert np.array_equal(
        list(state.iteritems()),
        [(("x", "y"), (1, 4)), (("x", "y"), (2, 5)), (("x", "y"), (3, 6))],
    )


def test_update(state):
    param_dict = dict(state.param_dict)
    param_dict["y"] = {"shape": None, "dtype": int}
    state = State(n_walkers=state.n_walkers, param_dict=param_dict)
    state.update(x=[1, 2, 3], y=[4, 5, 6])
    assert np.array_equal(state["x"], [1, 2, 3])
    assert np.array_equal(state["y"], [4, 5, 6])


def test_to_dict(state):
    state["x"] = [1, 2, 3]
    state_dict = state.to_dict()
    assert isinstance(state_dict, dict)
    assert "x" in state_dict.keys()
    assert "n_walkers" not in state_dict.keys()
    assert state.n_walkers == len(state_dict["x"])
    assert "param_dict" not in state_dict.keys()
    assert np.array_equal(state_dict["x"], [1, 2, 3])


def test_copy(state):
    state["x"] = [1, 2, 3]
    state_copy = state.copy()
    assert isinstance(state_copy, State)
    assert np.array_equal(list(state_copy.values()), [[1, 2, 3]])
    assert np.array_equal(list(state_copy["x"]), [1, 2, 3])


def test_reset(state):
    state["x"] = [1, 2, 3]
    state.reset()
    assert np.array_equal(list(state.values()), [[None, None, None]])


def test_params_to_arrays(state):
    param_dict_list = {
        "list_param_int": {"shape": None, "dtype": int},
        "list_param_list": {"shape": None, "dtype": list},
        "list_param_dict": {"shape": None, "dtype": dict},
        "list_param_set": {"shape": None, "dtype": set},
    }
    tensor_dict = state.params_to_arrays(param_dict_list, n_walkers=2)
    assert isinstance(tensor_dict, dict)
    assert "list_param_int" in tensor_dict.keys()
    assert "list_param_list" in tensor_dict.keys()
    assert "list_param_dict" in tensor_dict.keys()
    assert "list_param_set" in tensor_dict.keys()
    assert isinstance(tensor_dict["list_param_int"], list)
    assert isinstance(tensor_dict["list_param_list"], list)
    assert isinstance(tensor_dict["list_param_dict"], list)
    assert isinstance(tensor_dict["list_param_set"], list)
    assert np.array_equal(tensor_dict["list_param_int"], [None, None])
    assert np.array_equal(tensor_dict["list_param_list"], [None, None])
    assert np.array_equal(tensor_dict["list_param_dict"], [None, None])
