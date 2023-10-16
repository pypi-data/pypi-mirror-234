from evotorch.algorithms import GeneticAlgorithm
from evotorch.algorithms.searchalgorithm import SearchAlgorithm
from evotorch.core import Problem, SolutionBatch
from evotorch.operators import GaussianMutation, OnePointCrossOver
import judo
import numpy
import pytest

from fragile.callbacks.root_walker import BestWalker
from fragile.core.policy import ZeroContinuous
from fragile.core.swarm import FunctionMapper
from fragile.core.walkers import Walkers
from fragile.optimize.evotorch import EvotorchEnv


def create_searcher(popsize):
    import torch

    def sphere(x: torch.Tensor) -> torch.Tensor:
        return torch.sum(x.pow(2.0))

    problem = Problem(
        "min",
        sphere,
        initial_bounds=(([-5.12, -5.12]), ([5.12, 5.12])),
        solution_length=2,
        dtype=judo.dtype.float32,
        eval_dtype=judo.dtype.float32,
        device=judo.Backend.get_device(),
    )
    searcher = GeneticAlgorithm(
        problem,
        popsize=popsize,
        re_evaluate=True,
        elitist=True,
        operators=[
            OnePointCrossOver(problem, tournament_size=3),
            GaussianMutation(problem, stdev=0.05),
        ],
    )
    return searcher


def create_evotorch(max_epochs=10):
    n_walkers = 200
    walkers = Walkers(score_scale=2, accumulate_reward=False, freeze_walkers=False)
    searcher = create_searcher(popsize=n_walkers)
    env = EvotorchEnv(searcher)
    policy = ZeroContinuous()
    callbacks = [BestWalker()]

    swarm = FunctionMapper(
        policy=policy,
        walkers=walkers,
        env=env,
        callbacks=callbacks,
        n_walkers=n_walkers,
        max_epochs=max_epochs,
    )
    return swarm


@pytest.fixture(scope="module")
def swarm():
    swarm = create_evotorch(max_epochs=200)
    return swarm


class TestEvotorchEnv:
    def test_properties(self, swarm):
        assert isinstance(swarm.env.algorithm, SearchAlgorithm)
        assert isinstance(swarm.env.population, SolutionBatch)
        assert isinstance(swarm.env.problem, Problem)
        assert swarm.env.population == swarm.env.algorithm.population
        assert swarm.env.problem == swarm.env.algorithm.problem
        assert swarm.env.dtype == swarm.env.algorithm.population.dtype
        assert swarm.env.eval_dtype == swarm.env.algorithm.population.eval_dtype
        assert swarm.env.solution_length == swarm.env.algorithm.population.solution_length

    def test_score_gets_higher(self, swarm):
        target_score = 0.005
        swarm.run()
        root_score = float(swarm.root.score)
        beats_target = root_score <= target_score if swarm.minimize else root_score >= target_score
        assert beats_target, (root_score, target_score)

    def test_get_bounds(self, swarm):
        bounds = swarm.env._get_bounds()
        assert isinstance(bounds, judo.Bounds)
        bounds_l = swarm.env.problem.initial_lower_bounds
        if len(bounds_l.shape) == 0:
            bounds_l = bounds_l * judo.ones(swarm.env.solution_length)
        bounds_h = swarm.env.problem.initial_upper_bounds
        if len(bounds_h.shape) == 0:
            bounds_h = bounds_h * judo.ones(swarm.env.solution_length)
        assert numpy.allclose(judo.to_numpy(bounds.low), judo.to_numpy(bounds_l)), (
            bounds_l,
            bounds.low,
        )
        assert numpy.allclose(judo.to_numpy(bounds.high), judo.to_numpy(bounds_h)), (
            bounds_h,
            bounds.high,
        )
