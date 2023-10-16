from typing import Tuple, List, Dict

from pulp import LpVariable, LpProblem, LpMaximize, lpSum, LpAffineExpression, GLPK


class SolverUtils:

    @staticmethod
    def calculate_solved_problem(
            performance_table_list: List[List[float]],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            weights: List[float],
            criteria: List[int],
            alternative_id_1: int = -1,
            alternative_id_2: int = -1,
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems
        using general function

        :param show_logs:
        :param performance_table_list:
        :param preferences:
        :param indifferences:
        :param weights:
        :param criteria:
        :param alternative_id_1:
        :param alternative_id_2:

        :return:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i] == 1:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][-1] == weights[i]
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][0] == weights[i]
                problem += u_list[i][-1] == 0

        problem += lpSum(the_greatest_performance) == 1

        # Monotonicity constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i])):
                if criteria[i] == 1:
                    problem += u_list[i][j] >= u_list[i][j - 1]
                else:
                    problem += u_list[i][j - 1] >= u_list[i][j]

        # Bounds constraint
        for i in range(len(u_list)):
            for j in range(1, len(u_list[i]) - 1):
                if criteria[i] == 1:
                    problem += u_list[i][-1] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][0]
                else:
                    problem += u_list[i][0] >= u_list[i][j]
                    problem += u_list[i][j] >= u_list[i][-1]

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

        if alternative_id_1 >= 0 and alternative_id_2 >= 0:
            left_alternative: List[float] = performance_table_list[alternative_id_2]
            right_alternative: List[float] = performance_table_list[alternative_id_1]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

        problem += epsilon

        problem.solve(solver=GLPK(msg=show_logs))

        return problem

    @staticmethod
    def calculate_solved_problem_with_predefined_number_of_characteristic_points(
            performance_table_list: List[List[float]],
            preferences: List[List[int]],
            indifferences: List[List[int]],
            weights: List[float],
            criteria: List[int],
            number_of_points: List[int],
            alternative_id_1: int = -1,
            alternative_id_2: int = -1,
            show_logs: bool = False,
    ) -> LpProblem:
        """
        Main calculation method for problem-solving.
        The idea is that this should be a generic method used across different problems
        using predefined number of linear segments/characteristic points

        :param show_logs:
        :param performance_table_list:
        :param preferences:
        :param indifferences:
        :param weights:
        :param criteria:
        :param number_of_points:
        :param alternative_id_1:
        :param alternative_id_2:

        :return:
        """
        problem: LpProblem = LpProblem("UTA-GMS", LpMaximize)

        epsilon: LpVariable = LpVariable("epsilon")

        u_list, u_list_dict = SolverUtils.create_variables_list_and_dict(performance_table_list)

        characteristic_points: List[List[float]] = SolverUtils.calculate_characteristic_points(
            number_of_points, performance_table_list, u_list_dict
        )

        # Normalization constraints
        the_greatest_performance: List[LpVariable] = []
        for i in range(len(u_list)):
            if criteria[i] == 1:
                the_greatest_performance.append(u_list[i][-1])
                problem += u_list[i][-1] == weights[i]
                problem += u_list[i][0] == 0
            else:
                the_greatest_performance.append(u_list[i][0])
                problem += u_list[i][0] == weights[i]
                problem += u_list[i][-1] == 0

        u_list_of_characteristic_points = []
        for i in range(len(characteristic_points)):
            pom = []
            for j in range(len(characteristic_points[i])):
                pom.append(u_list_dict[i][characteristic_points[i][j]])
            u_list_of_characteristic_points.append(pom[:])

        # Preference constraint
        for preference in preferences:
            left_alternative: List[float] = performance_table_list[preference[0]]
            right_alternative: List[float] = performance_table_list[preference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

            # Check if preference is a characteristic point, if not add it to characteristic points
            for i in range(len(left_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if left_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(left_side[i])

            for i in range(len(right_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if right_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(right_side[i])

        # Indifference constraint
        for indifference in indifferences:
            left_alternative: List[float] = performance_table_list[indifference[0]]
            right_alternative: List[float] = performance_table_list[indifference[1]]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) == lpSum(right_side)

            # Check if indifference is a characteristic point, if not add it to characteristic points
            for i in range(len(left_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if left_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(left_side[i])

            for i in range(len(right_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if right_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(right_side[i])
        # code only for hasse graph calculation
        if alternative_id_1 >= 0 and alternative_id_2 >= 0:
            left_alternative: List[float] = performance_table_list[alternative_id_2]
            right_alternative: List[float] = performance_table_list[alternative_id_1]

            left_side: List[LpVariable] = []
            right_side: List[LpVariable] = []
            for i in range(len(u_list_dict)):
                left_side.append(u_list_dict[i][left_alternative[i]])
                right_side.append(u_list_dict[i][right_alternative[i]])

            problem += lpSum(left_side) >= lpSum(right_side) + epsilon

            # Check if preference is a characteristic point, if not add it to characteristic points
            for i in range(len(left_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if left_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(left_side[i])

            for i in range(len(right_side)):
                exist = 0
                for j in range(len(u_list_of_characteristic_points[i])):
                    if right_side[i].name == u_list_of_characteristic_points[i][j].name:
                        exist = 1
                        break
                if exist == 0:
                    u_list_of_characteristic_points[i].append(right_side[i])

        sorted_u_list_of_characteristic_points = [sorted(lp_var_list, key=lambda var: float(var.name.split("_")[-1]))
                                                  for lp_var_list in u_list_of_characteristic_points]

        # Use linear interpolation to create constraints
        for i in range(len(u_list_of_characteristic_points)):
            for j in range(len(characteristic_points[i]), len(u_list_of_characteristic_points[i])):
                point_before = 0
                point_after = 1
                while characteristic_points[i][point_before] > float(
                        u_list_of_characteristic_points[i][j].name.split("_")[-1]) or float(
                    u_list_of_characteristic_points[i][j].name.split("_")[-1]) > characteristic_points[i][point_after]:
                    point_before += 1
                    point_after += 1
                value = u_list_of_characteristic_points[i][point_before] + (
                        (u_list_of_characteristic_points[i][point_after] - u_list_of_characteristic_points[i][
                            point_before]) *
                        (float(u_list_of_characteristic_points[i][j].name.split("_")[-1]) - characteristic_points[i][
                            point_before]) /
                        (characteristic_points[i][point_after] - characteristic_points[i][point_before])
                )

                problem += u_list_of_characteristic_points[i][j] == value

        # Monotonicity constraint
        for i in range(len(sorted_u_list_of_characteristic_points)):
            for j in range(1, len(sorted_u_list_of_characteristic_points[i])):
                if criteria[i] == 1:
                    problem += sorted_u_list_of_characteristic_points[i][j] >= \
                               sorted_u_list_of_characteristic_points[i][j - 1]
                else:
                    problem += sorted_u_list_of_characteristic_points[i][j - 1] >= \
                               sorted_u_list_of_characteristic_points[i][j]

        # Bounds constraint
        for i in range(len(sorted_u_list_of_characteristic_points)):
            for j in range(1, len(sorted_u_list_of_characteristic_points[i]) - 1):
                if criteria[i] == 1:
                    problem += sorted_u_list_of_characteristic_points[i][-1] >= \
                               sorted_u_list_of_characteristic_points[i][j]
                    problem += sorted_u_list_of_characteristic_points[i][j] >= \
                               sorted_u_list_of_characteristic_points[i][0]
                else:
                    problem += sorted_u_list_of_characteristic_points[i][0] >= \
                               sorted_u_list_of_characteristic_points[i][j]
                    problem += sorted_u_list_of_characteristic_points[i][j] >= \
                               sorted_u_list_of_characteristic_points[i][-1]

        problem += epsilon

        glpk_solver = GLPK(msg=show_logs)
        glpk_solver.options += ['--nopresol']

        problem.solve(glpk_solver)

        return problem

    @staticmethod
    def create_variables_list_and_dict(performance_table: List[list]) -> Tuple[List[list], List[dict]]:
        """
        Method responsible for creating a technical list of variables and a technical dict of variables that are used
        for adding constraints to the problem.

        :param performance_table:

        :return: ex. Tuple([[u_0_0.0, u_0_2.0], [u_1_2.0, u_1_9.0]], [{26.0: u_0_26.0, 2.0: u_0_2.0}, {40.0: u_1_40.0, 2.0: u_1_2.0}])
        """
        u_list: List[List[LpVariable]] = []
        u_list_dict: List[Dict[float, LpVariable]] = []

        for i in range(len(performance_table[0])):
            row: List[LpVariable] = []
            row_dict: Dict[float, LpVariable] = {}

            for j in range(len(performance_table)):
                variable_name: str = f"u_{i}_{performance_table[j][i]}"
                variable: LpVariable = LpVariable(variable_name)

                if performance_table[j][i] not in row_dict:
                    row_dict[performance_table[j][i]] = variable

                flag: int = 1
                for var in row:
                    if str(var) == variable_name:
                        flag: int = 0
                if flag:
                    row.append(variable)

            u_list_dict.append(row_dict)

            row: List[LpVariable] = sorted(row, key=lambda var: float(var.name.split("_")[-1]))
            u_list.append(row)

        return u_list, u_list_dict

    @staticmethod
    def calculate_direct_relations(necessary: List[List[str]]) -> Dict[str, set]:
        """
        Method for getting only direct relations in Hasse Diagram

        :param necessary:

        :return:
        """
        direct_relations: Dict[str, set] = {}

        for relation in necessary:
            node1, node2 = relation
            direct_relations.setdefault(node1, set()).add(node2)

        for node1, related_nodes in direct_relations.items():
            related_nodes_copy: Dict[str] = related_nodes.copy()
            for node2 in related_nodes:
                # Check if node2 is also related to any other node that is related to node1
                for other_node in related_nodes:
                    if other_node != node2 and other_node in direct_relations and node2 in direct_relations[other_node]:
                        # If such a relationship exists, remove the relation between node1 and node2
                        related_nodes_copy.remove(node2)
                        break
            direct_relations[node1]: Dict[str] = related_nodes_copy

        return direct_relations

    @staticmethod
    def get_alternatives_and_utilities_dict(
            variables_and_values_dict,
            performance_table_list,
            alternatives_id_list,
            weights
    ) -> Dict[str, float]:

        utilities: List[float] = []
        for i in range(len(performance_table_list)):
            utility: float = 0.0
            for j in range(len(weights)):
                variable_name: str = f"u_{j}_{performance_table_list[i][j]}"
                utility += round(variables_and_values_dict[variable_name], 4)

            utilities.append(utility)

        utilities_dict: Dict[str, float] = {}
        # TODO: Sorting possibly unnecessary, but for now it's nicer for human eye :)
        for i in range(len(utilities)):
            utilities_dict[alternatives_id_list[i]] = utilities[i]
        sorted_dict: Dict[str, float] = dict(sorted(utilities_dict.items(), key=lambda item: item[1]))

        return sorted_dict

    @staticmethod
    def calculate_characteristic_points(
            number_of_points,
            performance_table_list,
            u_list_dict
    ) -> List[List[float]]:
        columns: List[Tuple[float]] = list(zip(*performance_table_list))
        min_values: List[float] = [min(col) for col in columns]
        max_values: List[float] = [max(col) for col in columns]

        characteristic_points: List[List[float]] = []
        for i in range(len(min_values)):
            pom = []
            for j in range(number_of_points[i]):
                x = min_values[i] + ((j) / (number_of_points[i] - 1)) * (max_values[i] - min_values[i])
                if x not in u_list_dict[i]:
                    new: str = f"u_{i}_{x}"
                    variable: LpVariable = LpVariable(new)
                    new: Dict[float, LpVariable] = {x: variable}
                    u_list_dict[i].update(new)
                pom.append(x)
            characteristic_points.append(pom[:])

        return characteristic_points

    @staticmethod
    def linear_interpolation(x, x1, y1, x2, y2) -> float:
        result = y1 + ((x - x1) * (y2 - y1)) / (x2 - x1)
        return result

    @staticmethod
    def get_alternatives_and_utilities_using_interpolation_dict(
            variables_and_values_dict,
            performance_table_list,
            weights,
            characteristic_points,
            alternatives_id_list
    ) -> Dict[str, float]:
        utilities = []
        for i in range(len(performance_table_list)):
            utility = 0.0
            for j in range(len(weights)):
                variable_name = f"u_{j}_{performance_table_list[i][j]}"

                if variable_name in variables_and_values_dict:
                    utility += variables_and_values_dict[variable_name]
                else:
                    before_point = 0
                    after_point = 1
                    while characteristic_points[j][before_point] > performance_table_list[i][j] \
                            or performance_table_list[i][j] > characteristic_points[j][after_point]:
                        before_point += 1
                        after_point += 1

                    variable_name_1 = f"u_{j}_{characteristic_points[j][before_point]}"
                    variable_name_2 = f"u_{j}_{characteristic_points[j][after_point]}"

                    utility += SolverUtils.linear_interpolation(
                        performance_table_list[i][j],
                        characteristic_points[j][before_point],
                        variables_and_values_dict[variable_name_1],
                        characteristic_points[j][after_point],
                        variables_and_values_dict[variable_name_2]
                    )

            utilities.append(utility)

        utilities_dict: Dict[str, float] = {}
        for i in range(len(utilities)):
            utilities_dict[alternatives_id_list[i]] = utilities[i]
        sorted_dict = dict(sorted(utilities_dict.items(), key=lambda item: item[1]))

        return sorted_dict
