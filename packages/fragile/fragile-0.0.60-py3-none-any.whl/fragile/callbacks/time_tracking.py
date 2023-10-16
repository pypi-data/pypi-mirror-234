import judo
from judo.data_types import dtype

from fragile.core.api_classes import Callback
from fragile.core.typing import StateDict


class TrackSteps(Callback):
    name = "track_steps"
    default_inputs = {"n_step": {"clone": True}}
    default_outputs = ("n_step",)

    @property
    def param_dict(self) -> StateDict:
        return {"n_step": {"dtype": dtype.int32}}

    def update_steps(self) -> None:
        actives = self.swarm.state.actives
        infos = self.swarm.state.get("infos", inactives=True)
        if infos is None:
            return
        new_steps = judo.tensor([info.get("n_step") for info in infos], dtype=dtype.int32)
        steps = self.swarm.state.get("n_step", inactives=True)
        steps[actives] = steps[actives] + new_steps[actives]
        self.swarm.state.update(n_step=steps, inactives=True)

    def after_env(self):
        self.update_steps()
