from algorithm.simplex_method import SimplexMethod
from algorithm.big_m import BigM


class Problem:
    def __init__(self, cost_vector, max_problem=True):
        # 默认x均>=0
        if max_problem:
            self.cost_vector = cost_vector
        else:
            self.cost_vector = [i * -1 for i in cost_vector]

        self.a_matrix = []
        self.b_vector = []
        self.logic_symbol = []
        self.slack_variable_count = []
        self.larger_count = []

    def add_constraint(self, a_vector, logic_symbol, b_scalar):
        self.a_matrix.append(a_vector)
        self.b_vector.append([b_scalar])
        self.logic_symbol.append([logic_symbol])

    def standardization(self):
        # 保证符号为<=
        for i in range(len(self.logic_symbol)):
            if self.logic_symbol[i][0] == '>=':
                self.larger_count.append(i)

        # 统计松弛变量的序号
        for i in range(len(self.logic_symbol)):
            if self.logic_symbol[i][0] != '=':
                self.slack_variable_count.append(i)

        # 加入松弛变量
        self.cost_vector += [0 for _ in range(len(self.slack_variable_count))]

        slack_variable_index = 0
        for i in range(len(self.logic_symbol)):
            slack = [0 for _ in range(len(self.slack_variable_count))]
            if i in self.slack_variable_count:
                slack[slack_variable_index] = 1
            if i in self.larger_count:
                slack[slack_variable_index] = -1
            slack_variable_index += 1
            self.a_matrix[i] += slack

        return self.cost_vector, self.a_matrix, self.b_vector

    def solver(self):
        c, a, b = self.standardization()
        pb_bigm = BigM(c, a, b)
        c, a, b, basis_index = pb_bigm.add_manual_variable()
        initialization = SimplexMethod(c, a, b, basis_index)
        x_index, x_value, z_value = initialization.solver()
        x_index += 1
        for x, value in zip(x_index, x_value):
            print('x_{} is {}'.format(x, value))
        print('The maximum value of this question is {}'.format(z_value[0]))

        return [x_index.tolist(), x_value.tolist(), z_value[0]]

