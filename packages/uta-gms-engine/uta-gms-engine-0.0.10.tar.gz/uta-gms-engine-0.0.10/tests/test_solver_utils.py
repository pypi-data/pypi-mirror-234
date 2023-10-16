from typing import Dict

import pytest
from pulp import LpProblem, value

from src.utagmsengine.utils.solver_utils import SolverUtils


@pytest.fixture()
def performance_table_list_dummy():
    return [[26.0, 40.0, 44.0],
            [2.0, 2.0, 68.0],
            [18.0, 17.0, 14.0],
            [35.0, 62.0, 25.0],
            [7.0, 55.0, 12.0],
            [25.0, 30.0, 12.0],
            [9.0, 62.0, 88.0],
            [0.0, 24.0, 73.0],
            [6.0, 15.0, 100.0],
            [16.0, 9.0, 0.0],
            [26.0, 17.0, 17.0],
            [62.0, 43.0, 0.0]]


@pytest.fixture()
def preferences_list_dummy():
    return [
        [6, 5],
        [5, 4]
    ]


@pytest.fixture()
def indifferences_list_dummy():
    return [
        [3, 6]
    ]


@pytest.fixture()
def weights_list_dummy():
    return [0.4, 0.25, 0.35]


@pytest.fixture()
def criteria_list_dummy():
    return [1, 1, 1]


@pytest.fixture()
def alternatives_id_list_dummy():
    return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


@pytest.fixture()
def problem_variable_values_dummy():
    return [0.4, 0.0, 0.2, 0.4, 0.0, 0.4, 0.4, 0.4, 0.0, 0.4, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.35, 0.0, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.35]


@pytest.fixture()
def predefined_number_of_linear_segments_problem_variable_values_dummy():
    return [0.152455, 0.0, 0.29776, 0.369222, 0.373194, 0.4, 0.0833728, 0.107194, 0.0, 0.172979, 0.185335, 0.234911, 0.25, 0.0, 0.35, 0.0, 0.0, 0.0, 0.266]


@pytest.fixture()
def necessary_dummy():
    return [['A', 'C'], ['A', 'E'], ['A', 'F'], ['A', 'J'], ['A', 'K'], ['C', 'J'], ['D', 'B'], ['D', 'C'], ['D', 'E'], ['D', 'F'], ['D', 'G'], ['D', 'H'], ['D', 'J'], ['D', 'K'], ['F', 'E'], ['F', 'J'], ['G', 'B'], ['G', 'C'], ['G', 'D'], ['G', 'E'], ['G', 'F'], ['G', 'H'], ['G', 'J'], ['G', 'K'], ['I', 'B'], ['K', 'C'], ['K', 'J'], ['L', 'J']]


@pytest.fixture()
def direct_relations_dummy():
    return {'A': {'F', 'K'}, 'C': {'J'}, 'D': {'G'}, 'F': {'E', 'J'}, 'G': {'B', 'H', 'D', 'F', 'K'}, 'I': {'B'}, 'K': {'C'}, 'L': {'J'}}


@pytest.fixture()
def alternatives_and_utilities_dict_dummy():
    return {'E': 0.0, 'C': 0.4667, 'F': 0.4667, 'J': 0.4667, 'K': 0.4667, 'L': 0.4667, 'B': 0.5333, 'H': 0.5333, 'I': 0.5333, 'A': 1.0, 'D': 1.0, 'G': 1.0}


@pytest.fixture()
def variables_and_values_dict_dummy():
    return {'epsilon': 0.18666667, 'u_0_0.0': 0.0, 'u_0_16.0': 0.46666667, 'u_0_18.0': 0.46666667, 'u_0_2.0': 0.0, 'u_0_25.0': 0.46666667, 'u_0_26.0': 0.46666667, 'u_0_35.0': 0.46666667, 'u_0_6.0': 0.0, 'u_0_62.0': 0.46666667, 'u_0_7.0': 0.0, 'u_0_9.0': 0.46666667, 'u_1_15.0': 0.0, 'u_1_17.0': 0.0, 'u_1_2.0': 0.0, 'u_1_24.0': 0.0, 'u_1_30.0': 0.0, 'u_1_40.0': 0.0, 'u_1_43.0': 0.0, 'u_1_55.0': 0.0, 'u_1_62.0': 0.0, 'u_1_9.0': 0.0, 'u_2_0.0': 0.0, 'u_2_100.0': 0.53333333, 'u_2_12.0': 0.0, 'u_2_14.0': 0.0, 'u_2_17.0': 0.0, 'u_2_25.0': 0.53333333, 'u_2_44.0': 0.53333333, 'u_2_68.0': 0.53333333, 'u_2_73.0': 0.53333333, 'u_2_88.0': 0.53333333}


@pytest.fixture()
def number_of_points_dummy():
    return [3, 3, 3]


def test_create_variables_list_and_dict(performance_table_list_dummy):
    u_arr, u_arr_dict = SolverUtils.create_variables_list_and_dict(performance_table_list_dummy)

    assert len(u_arr) == 3
    assert len(u_arr_dict) == 3
    assert len(u_arr[0]) == 11
    assert len(u_arr[1]) == 10
    assert len(u_arr[2]) == 10
    assert u_arr[0][0].name == 'u_0_0.0'
    assert u_arr_dict[0][26.0].name == 'u_0_26.0'


def test_calculate_solved_problem_with_predefined_number_of_characteristic_points(
    performance_table_list_dummy,
    preferences_list_dummy,
    indifferences_list_dummy,
    weights_list_dummy,
    criteria_list_dummy,
    number_of_points_dummy,
    predefined_number_of_linear_segments_problem_variable_values_dummy
):
    problem: LpProblem = SolverUtils.calculate_solved_problem_with_predefined_number_of_characteristic_points(
        performance_table_list=performance_table_list_dummy,
        preferences=preferences_list_dummy,
        indifferences=indifferences_list_dummy,
        weights=weights_list_dummy,
        criteria=criteria_list_dummy,
        number_of_points=number_of_points_dummy
    )

    variable_values = []
    for var in problem.variables():
        variable_values.append(value(var))

    assert variable_values == predefined_number_of_linear_segments_problem_variable_values_dummy


def test_calculate_solved_problem(
    performance_table_list_dummy,
    preferences_list_dummy,
    indifferences_list_dummy,
    weights_list_dummy,
    criteria_list_dummy,
    problem_variable_values_dummy
):
    problem: LpProblem = SolverUtils.calculate_solved_problem(
        performance_table_list=performance_table_list_dummy,
        preferences=preferences_list_dummy,
        indifferences=indifferences_list_dummy,
        weights=weights_list_dummy,
        criteria=criteria_list_dummy,
        alternative_id_1=1,
        alternative_id_2=2
    )

    variable_values = []
    for var in problem.variables():
        variable_values.append(value(var))

    assert variable_values == problem_variable_values_dummy


def test_calculate_direct_relations(necessary_dummy, direct_relations_dummy):
    direct_relations: Dict[str, set] = SolverUtils.calculate_direct_relations(necessary_dummy)

    assert direct_relations == direct_relations_dummy


def test_get_alternatives_and_utilities_dict(
        variables_and_values_dict_dummy,
        performance_table_list_dummy,
        alternatives_id_list_dummy,
        weights_list_dummy,
        alternatives_and_utilities_dict_dummy
):
    alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
        variables_and_values_dict=variables_and_values_dict_dummy,
        performance_table_list=performance_table_list_dummy,
        alternatives_id_list=alternatives_id_list_dummy,
        weights=weights_list_dummy
    )

    assert alternatives_and_utilities_dict == alternatives_and_utilities_dict_dummy


