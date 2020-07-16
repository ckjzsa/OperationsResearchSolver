import numpy as np
import math
from OperationsResearchSolver.algorithm.problem_generation import Problem
from OperationsResearchSolver.algorithm.big_m import BigM
from OperationsResearchSolver.algorithm.simplex_method import SimplexMethod


class BranchAndBound:
    def __init__(self, integer_index, cost_vector, a_matrix=[], b_vector=[], logic_symbol=[], max_problem=True):
        if max_problem:
            self.cost_vector = cost_vector
        else:
            self.cost_vector = [i * -1 for i in cost_vector]

        self.a_matrix = a_matrix
        self.b_vector = b_vector
        self.logic_symbol = logic_symbol
        self.integer_index = integer_index

        # 初始上界和下界
        self.upper_bound = self.initial_z_value
        self.lower_bound = 0

        self.queue = []

        pass

    def add_constraint(self, a_vector, logic_symbol, b_scalar):
        self.a_matrix.append(a_vector)
        self.b_vector.append([b_scalar])
        self.logic_symbol.append([logic_symbol])

    def solver(self, cost_vector, a_matrix, b_vector, logic_symbol, max_problem=True):
        # 获得初始解
        pb = Problem(cost_vector, a_matrix, b_vector, logic_symbol, max_problem)
        c, a, b = pb.standardization()
        pb_bigm = BigM(c, a, b)
        c, a, b, basis_index = pb_bigm.add_manual_variable()
        initialization = SimplexMethod(c, a, b, basis_index)
        x_index, x_value, z_value = initialization.solver()
        x_index += 1

        initial_res = [x_index.tolist(), x_value.tolist(), z_value[0]]

        # 获得初值
        self.initial_x_index = initial_res[0] - 1
        self.initial_x_value = initial_res[1]
        self.initial_z_value = initial_res[2]

        while self.queue:
            # 分为两个问题
            pb1 =
            for x_index, x_value in zip(self.initial_x_index, self.initial_x_value):
                if x_index in self.integer_index and math.ceil(x_index) != x_value:
                    pb1 =

        pass
