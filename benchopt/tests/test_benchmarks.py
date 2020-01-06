import pytest
import numpy as np

from benchopt.base import SAMPLING_STRATEGIES

from benchopt.util import get_all_benchmarks
from benchopt.util import get_benchmark_objective
from benchopt.util import list_benchmark_solvers
from benchopt.util import list_benchmark_datasets


BENCHMARKS = get_all_benchmarks()
SOLVERS = [(benchmark, solver) for benchmark in BENCHMARKS
           for solver in list_benchmark_solvers(benchmark)]
DATASETS = [(benchmark, dataset) for benchmark in BENCHMARKS
            for dataset in list_benchmark_datasets(benchmark)]


def class_ids(parameter):
    if hasattr(parameter, 'name'):
        return parameter.name.lower()
    return None


@pytest.mark.parametrize('benchmark_name, dataset_class', DATASETS,
                         ids=class_ids)
def test_benchmark_objective(benchmark_name, dataset_class):
    """Check that the objective function and the datasets are well defined."""
    objective_class = get_benchmark_objective(benchmark_name)
    objective = objective_class()

    parameters = {}
    dataset = dataset_class(**parameters)
    scale, data = dataset.get_data()
    objective.set_data(**data)

    # check that the reported scale si correct and that the result of
    # the objective function is a scalar
    beta_hat = np.zeros(scale)
    objective_value = objective(beta=beta_hat)
    assert np.isscalar(objective_value), (
        "The output of the objective function should be a scalar."
    )


@pytest.mark.parametrize('benchmark_name, solver_class', SOLVERS,
                         ids=class_ids)
def test_solver_class(benchmark_name, solver_class):
    """Check that all installed solver_class respects the public API"""

    # Check that the solver_class exposes a name
    assert hasattr(solver_class, 'name'), "All solver should expose a name"
    assert isinstance(solver_class.name, str), (
        "The solver's name should be a string"
    )

    # Check that the solver_class uses a valid sampling_strategy
    assert solver_class.sampling_strategy in SAMPLING_STRATEGIES

    # Check that the solver_class exposes a known install cmd
    assert solver_class.install_cmd in [None, 'pip', 'bash']

    # Check that the solver_class exposes a known install cmd
    if solver_class.install_cmd == 'pip':
        assert hasattr(solver_class, 'package_name')
    if solver_class.install_cmd == 'bash':
        assert hasattr(solver_class, 'install_script')
        assert hasattr(solver_class, 'cmd_name')


@pytest.mark.parametrize('benchmark_name, dataset_class', DATASETS,
                         ids=class_ids)
def test_dataset_class(benchmark_name, dataset_class):
    """Check that all installed dataset_class respects the public API"""

    # Check that the dataset_class exposes a name
    assert hasattr(dataset_class, 'name'), "All dataset should expose a name"
    assert isinstance(dataset_class.name, str), (
        "The dataset's name should be a string")

    # Ensure that the dataset exposes a `get_data` function
    # that is callable
    dataset = dataset_class()
    assert hasattr(dataset, 'get_data'), (
        "All dataset should implement get_data"
    )
    data = dataset.get_data()
    assert isinstance(data, tuple), (
        "Ouput of get_data should be a 2-tuple"
    )
    assert len(data) == 2, (
        "Ouput of get_data should be a 2-tuple"
    )

    scale, data = data

    assert isinstance(scale, int)
    assert isinstance(data, dict)
