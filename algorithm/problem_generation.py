from algorithm.simplex_method import SimplexMethod
from algorithm.big_m import BigM


class Problem:
    def __init__(self, cost_vector, a_matrix=[], b_vector=[], logic_symbol=[], max_problem=True, ilp=False):
        # 默认x均>=0
        if max_problem:
            self.cost_vector = cost_vector
        else:
            self.cost_vector = [i * -1 for i in cost_vector]

        self.a_matrix = a_matrix
        self.b_vector = b_vector
        self.logic_symbol = logic_symbol
        self.slack_variable_count = []
        self.larger_count = []
        self.ilp = ilp

        # 记录原来的行列数，后面复原
        self.original_row = len(a_matrix)
        if len(a_matrix) != 0:
            self.original_column = len(a_matrix[0])
        else:
            self.original_column = 0

    def origin(self):
        origin_c = self.cost_vector
        origin_a = self.a_matrix
        origin_b = self.b_vector
        origin_symbol = self.logic_symbol

        return origin_c, origin_a, origin_b, origin_symbol

    def add_constraint(self, a_vector, logic_symbol, b_scalar):
        self.a_matrix.append(a_vector)
        self.b_vector.append([b_scalar])
        self.logic_symbol.append([logic_symbol])
        self.original_row += 1
        self.original_column = len(a_vector)

    def standardization(self):
        # 统计大于号的位置
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
            if i in self.slack_variable_count:  # 添加松弛变量
                slack[slack_variable_index] = 1
            if i in self.larger_count:  # 大于号添加剩余变量
                slack[slack_variable_index] = -1
            slack_variable_index += 1
            self.a_matrix[i] += slack

        return self.cost_vector, self.a_matrix, self.b_vector, self.logic_symbol

    def solver(self):
        c, a, b, _ = self.standardization()
        pb_bigm = BigM(c, a, b)
        c, a, b, basis_index, mannual_index = pb_bigm.add_manual_variable()
        initialization = SimplexMethod(c, a, b, basis_index)
        x_index, x_value, z_value = initialization.solver()
        x_index += 1
        if not self.ilp:
            for x, value in zip(x_index, x_value):
                print('x_{} is {}'.format(x, value))
            print('The maximum value of this question is {}'.format(z_value[0]))

            for index in x_index:
                if index in mannual_index:
                    print('无可行解！')
                    return False

        self.cost_vector = self.cost_vector[:self.original_column]
        self.a_matrix = [row[:self.original_column] for row in self.a_matrix[:self.original_row]]
        self.b_vector = self.b_vector[:self.original_row]
        self.logic_symbol = self.logic_symbol[:self.original_row]

        return [x_index.tolist(), x_value.tolist(), z_value[0]]

