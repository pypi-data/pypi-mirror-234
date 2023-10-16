import copy

import judo
import numpy

from fragile.core.api_classes import Callback


class RootWalker(Callback):
    name = "root"

    def __init__(self, **kwargs):
        self._data = {}
        self.minimize = False
        super(RootWalker, self).__init__(**kwargs)

    def __getattr__(self, item):
        plural = item + "s"
        if plural in self._data:
            d = self._data[plural]
            try:
                return (
                    d[0]
                    if isinstance(d, (list, numpy.ndarray))
                    else (d.item() if len(d.shape) == 0 else d)
                )
            except IndexError:
                return d.item()

        elif item in self._data:
            d = self._data[item]
            try:
                return (
                    d[0]
                    if isinstance(d, (list, numpy.ndarray))
                    else (d.item() if len(d.shape) == 0 else d)
                )
            except IndexError:
                return d.item()

            return self._data[item][0]
        return self.__getattribute__(item)

    def __repr__(self) -> str:
        # score = self.data.get('scores', [numpy.nan])[0]
        return f"{self.__class__.__name__}: score: {self.scores}"

    def to_html(self):
        return (
            f"<strong>{self.__class__.__name__}</strong>: "
            f"Score: {self.scores}\n"
            # f"Score: {self.data.get('scores', [numpy.nan])[0]}\n"
        )

    @property
    def data(self):
        return self._data

    def setup(self, swarm):
        super(RootWalker, self).setup(swarm)
        self.minimize = swarm.minimize

    def reset(self, root_walker=None, state=None, **kwargs):
        if root_walker is None:
            value = [numpy.inf if self.minimize else -numpy.inf]
            self._data = {"scores": value, "rewards": value}
            self.update_root()
        else:
            self._data = {k: copy.deepcopy(v) for k, v in root_walker.items()}

    def before_walkers(self):
        self.update_root()

    def update_root(self):
        raise NotImplementedError()


class BestWalker(RootWalker):
    default_inputs = {"scores": {}, "oobs": {"optional": True}}

    def __init__(self, always_update: bool = False, fix_root=True, **kwargs):
        super(BestWalker, self).__init__(**kwargs)
        self.minimize = None
        self.always_update = always_update
        self._fix_root = fix_root

    def get_best_index(self):
        scores, oobs, terminals = self.get("scores"), self.get("oobs"), self.get("terminals")
        index = judo.arange(len(scores))
        bool_ix = ~oobs if terminals is None else judo.logical_or(~oobs, terminals)
        alive_scores = judo.copy(scores[bool_ix])
        if len(alive_scores) == 0:
            return 0
        ix = alive_scores.argmin() if self.minimize else alive_scores.argmax()
        ix = judo.astype(judo.clip(ix, 0, judo.inf), judo.int)
        try:
            return judo.copy(index[bool_ix][ix])
        except Exception as e:
            print(ix, bool_ix)
            raise e

    def get_best_walker(self):
        return self.swarm.state.export_walker(self.get_best_index())

    def update_root(self):
        best = self.get_best_walker()
        best_score = best["scores"] if judo.Backend.is_numpy() else best["scores"].item()

        # if not judo.Backend.is_numpy():# and judo.dtype.is_tensor(self.score):
        #    scores = self._data["scores"]
        #    score = scores[0] if isinstance(scores, list) else scores.item()
        # else:
        score = self.score
        score_improves = (best_score < score) if self.minimize else (best_score > score)
        if self.always_update or score_improves:  # or numpy.isinf(score):
            # new_best = {k: copy.deepcopy(v) for k, v in best.items()}
            self._data = copy.deepcopy(best)

    def fix_root(self):
        if self._fix_root:
            self.swarm.state.import_walker(copy.deepcopy(self.data))
            terminals = self.swarm.get("terminals")
            if not self.swarm.state.actives[0] and terminals is not None and not terminals[0]:
                self.swarm.state.actives[0] = True
                self.swarm.state._n_actives += 1

    def after_walkers(self):
        self.fix_root()


class TrackWalker(RootWalker):
    default_inputs = {"scores": {}, "oobs": {"optional": True}}

    def __init__(self, walker_index=0, **kwargs):
        super(TrackWalker, self).__init__(**kwargs)
        self.walker_index = walker_index

    def update_root(self):
        walker = self.swarm.state.export_walker(self.walker_index)
        self._data = copy.deepcopy({k: v.clone() for k, v in walker.items()})
