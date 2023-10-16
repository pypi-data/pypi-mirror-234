from xmcda.criteria import Criteria
from xmcda.XMCDA import XMCDA
import csv
import _io
from typing import List

from .utils.parser_utils import ParserUtils


class Parser:
    def get_performance_table_list_xml(self, path: str) -> List[List]:
        """
        Method responsible for getting list of performances

        :param path: Path to XMCDA file (performance_table.xml)

        :return: List of alternatives ex. [[26.0, 40.0, 44.0], [2.0, 2.0, 68.0], [18.0, 17.0, 14.0], ...]
        """
        performance_table_list: List[List[float]] = []
        xmcda: XMCDA = ParserUtils.load_file(path)
        criteria_list: List = self.get_criteria_xml(path)

        for alternative in xmcda.alternatives:
            performance_list: List[float] = []
            for i in range(len(criteria_list)):
                performance_list.append(xmcda.performance_tables[0][alternative][xmcda.criteria[i]])
            performance_table_list.append(performance_list)

        return performance_table_list

    @staticmethod
    def get_alternatives_id_list_xml(path: str) -> List[str]:
        """
        Method responsible for getting list of alternatives ids

        :param path: Path to XMCDA file (alternatives.xml)

        :return: List of alternatives ex. ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        """
        alternatives_id_list: List[str] = []
        xmcda: XMCDA = ParserUtils.load_file(path)

        for alternative in xmcda.alternatives:
            alternatives_id_list.append(alternative.id)

        return alternatives_id_list

    @staticmethod
    def get_criteria_xml(path: str):
        """
        Method responsible for getting list of criteria

        :param path: Path to XMCDA file

        :return: List of criteria ex. ['g1', 'g2', 'g3']
        """
        criteria_list: List = []
        xmcda: XMCDA = ParserUtils.load_file(path)
        criteria_xmcda: Criteria = xmcda.criteria

        for criteria in criteria_xmcda:
            criteria_list.append(criteria.id)

        # Recognition of the type of criteria
        type_of_criterion: List[int] = []
        for i in range(len(criteria_list)):
            if criteria_list[i][0] == 'g':
                type_of_criterion.append(1)
            else:
                type_of_criterion.append(0)

        return type_of_criterion

    @staticmethod
    def get_performance_table_list_csv(csvfile: _io.TextIOWrapper) -> List[List[float]]:
        """
        Method responsible for getting list of performances from CSV file

        :param csvfile: python file object of csv file

        :return: List of alternatives ex. [[26.0, 40.0, 44.0], [2.0, 2.0, 68.0], [18.0, 17.0, 14.0], ...]
        """
        performance_table_list: List[List[float]] = []

        csv_reader = csv.reader(csvfile, delimiter=';')
        next(csv_reader)  # Skip the header row
        next(csv_reader)
        for row in csv_reader:
            performance_list = [float(value) for value in row]
            performance_table_list.append(performance_list)

        return performance_table_list

    @staticmethod
    def get_alternatives_id_list_csv(csvfile: _io.TextIOWrapper) -> List[str]:

        """
        Method responsible for getting list of alternatives ids

        :param csvfile: python file object of csv file

        :return: List of alternatives ex. ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        """
        csv_reader = csv.reader(csvfile, delimiter=';')
        next(csv_reader)  # Skip the header row
        alternatives_id_list = next(csv_reader)  # Read the second row (names row)

        return alternatives_id_list

    @staticmethod
    def get_criteria_csv(csvfile: _io.TextIOWrapper) -> List[int]:
        """
        Method responsible for getting list of criteria

        :param csvfile: python file object of csv file

        :return: List of criteria ex. ['g1', 'g2', 'g3']
        """
        csv_reader = csv.reader(csvfile, delimiter=';')
        criteria_list = next(csv_reader)

        # Recognition of the type of criteria
        type_of_criterion: List[int] = []
        for i in range(len(criteria_list)):
            if criteria_list[i][0] == 'g':
                type_of_criterion.append(1)
            else:
                type_of_criterion.append(0)

        return type_of_criterion
