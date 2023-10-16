import pytest

from src.utagmsengine.parser import Parser

from typing import List


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
def alternatives_id_list_dummy():
    return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


@pytest.fixture()
def criteria_list_dummy():
    return [1, 1, 1]


def test_get_performance_table_list_xml(performance_table_list_dummy):
    parser = Parser()
    performance_table_list: List[List[float]] = parser.get_performance_table_list_xml('performance_table.xml')

    assert performance_table_list == performance_table_list_dummy


def test_get_alternatives_id_list_xml(alternatives_id_list_dummy):
    parser = Parser()
    alternatives_id_list: List[str] = parser.get_alternatives_id_list_xml('alternatives.xml')

    assert alternatives_id_list == alternatives_id_list_dummy


def test_get_criteria_xml(criteria_list_dummy):
    parser = Parser()

    criteria_list: List[str] = parser.get_criteria_xml('performance_table.xml')

    assert criteria_list == criteria_list_dummy


def test_get_performance_table_list_csv(performance_table_list_dummy):
    parser = Parser()
    performance_table_list: List[List[float]] = parser.get_performance_table_list_csv('../tests/files/alternatives.csv')

    assert performance_table_list == performance_table_list_dummy


def test_get_alternatives_id_list_csv(alternatives_id_list_dummy):
    parser = Parser()
    alternatives_id_list: List[str] = parser.get_alternatives_id_list_csv('../tests/files/alternatives.csv')

    assert alternatives_id_list == alternatives_id_list_dummy


def test_get_criteria_csv(criteria_list_dummy):
    parser = Parser()

    criteria_list: List[str] = parser.get_criteria_csv('../tests/files/alternatives.csv')

    assert criteria_list == criteria_list_dummy

