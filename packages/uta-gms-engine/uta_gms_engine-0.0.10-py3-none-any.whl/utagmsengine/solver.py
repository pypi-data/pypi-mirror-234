from typing import List, Dict, Optional

from pulp import LpProblem

from .utils.solver_utils import SolverUtils


class Solver:

    def __init__(self, show_logs: Optional[bool] = False):
        self.name = 'UTA GMS Solver'
        self.show_logs = show_logs

    def __str__(self):
        return self.name

    def get_hasse_diagram_dict(
            self,
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            weights: List[float],
            criteria: List[int],
            number_of_points: Optional[List[int]] = None
    ) -> Dict[str, set]:
        """
        Method for getting hasse diagram dict

        :param number_of_points:
        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param weights:
        :param criteria:

        :return refined_necessary:
        """
        if number_of_points is None:
            necessary: List[List[str]] = []
            for i in range(len(performance_table_list)):
                for j in range(len(performance_table_list)):
                    if i == j:
                        continue

                    problem: LpProblem = SolverUtils.calculate_solved_problem(
                        performance_table_list=performance_table_list,
                        preferences=preferences,
                        indifferences=indifferences,
                        weights=weights,
                        criteria=criteria,
                        alternative_id_1=i,
                        alternative_id_2=j,
                        show_logs=self.show_logs
                    )

                    if problem.variables()[0].varValue <= 0:
                        necessary.append([alternatives_id_list[i], alternatives_id_list[j]])

            direct_relations: Dict[str, set] = SolverUtils.calculate_direct_relations(necessary)
        else:
            necessary: List[List[str]] = []
            for i in range(len(performance_table_list)):
                for j in range(len(performance_table_list)):
                    if i == j:
                        continue

                    problem: LpProblem = SolverUtils.calculate_solved_problem_with_predefined_number_of_characteristic_points(
                        performance_table_list=performance_table_list,
                        preferences=preferences,
                        indifferences=indifferences,
                        weights=weights,
                        criteria=criteria,
                        number_of_points=number_of_points,
                        alternative_id_1=i,
                        alternative_id_2=j,
                        show_logs=self.show_logs
                    )

                    if problem.variables()[0].varValue <= 0:
                        necessary.append([alternatives_id_list[i], alternatives_id_list[j]])

            direct_relations: Dict[str, set] = SolverUtils.calculate_direct_relations(necessary)

        return direct_relations

    def get_ranking_dict(
            self,
            performance_table_list: List[List[float]],
            alternatives_id_list: List[str],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            weights: List[float],
            criteria: List[int],
            number_of_points: Optional[List[int]] = None
    ) -> Dict[str, float]:
        """
        Method for getting ranking dict

        :param number_of_points:
        :param performance_table_list:
        :param alternatives_id_list:
        :param preferences:
        :param indifferences:
        :param weights:
        :param criteria:

        :return refined_necessary:
        """

        if number_of_points is None:
            problem: LpProblem = SolverUtils.calculate_solved_problem(
                performance_table_list=performance_table_list,
                preferences=preferences,
                indifferences=indifferences,
                weights=weights,
                criteria=criteria,
                show_logs=self.show_logs
            )

            variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in
                                                           problem.variables()}

            alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_dict(
                variables_and_values_dict=variables_and_values_dict,
                performance_table_list=performance_table_list,
                alternatives_id_list=alternatives_id_list,
                weights=weights
            )
        else:
            problem: LpProblem = SolverUtils.calculate_solved_problem_with_predefined_number_of_characteristic_points(
                performance_table_list=performance_table_list,
                preferences=preferences,
                indifferences=indifferences,
                weights=weights,
                criteria=criteria,
                number_of_points=number_of_points,
                show_logs=self.show_logs
            )

            variables_and_values_dict: Dict[str, float] = {variable.name: variable.varValue for variable in problem.variables()}

            u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

            characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
                number_of_points, performance_table_list, u_list_dict
            )

            alternatives_and_utilities_dict: Dict[str, float] = SolverUtils.get_alternatives_and_utilities_using_interpolation_dict(
                variables_and_values_dict=variables_and_values_dict,
                performance_table_list=performance_table_list,
                weights=weights,
                characteristic_points=characteristic_points,
                alternatives_id_list=alternatives_id_list,
            )

        return alternatives_and_utilities_dict
