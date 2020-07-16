import numpy as np


class BigM:
    def __init__(self, c_vector, a_matrix, b_vector):
        temp = np.array([a_matrix[0]])
        for i in range(1, len(a_matrix)):
            temp = np.concatenate([temp, np.array([a_matrix[i]])], axis=0)

        one_count = 0
        zero_count = 0
        unit_vector = []
        temp_index = [None] * len(a_matrix[0])
        for i in range(len(a_matrix[0])):
            for j in range(len(temp[:, i])):
                if temp[:, i][j] == 1:
                    one_count += 1
                    temp_index[i] = j
                elif temp[:, i][j] == 0:
                    zero_count += 1
            if one_count == 1 and zero_count == (len(a_matrix) - 1):
                unit_vector.append(i)
            one_count = 0
            zero_count = 0

        # 现有的单位向量的形状
        one_index = []
        for i in unit_vector:
            one_index.append(temp_index[i])

        # 目前的单位向量个数
        unit_vector_count = len(unit_vector)
        unit_vector_required = len(a_matrix) - unit_vector_count
        self.unit_vector_position = []
        for i in range(len(a_matrix)):
            if i not in one_index:
                self.unit_vector_position.append(i)

        self.num_manual_variable = unit_vector_required
        self.one_index = one_index
        self.basis_index = unit_vector
        self.cost_vector = c_vector
        self.b_vector = b_vector
        self.a_matrix = a_matrix
        self.bigM = max(c_vector) * 10 if max(c_vector) > 0 else 10.0
        self.manual_index = [i for i in range(len(self.cost_vector), len(self.cost_vector)+self.num_manual_variable)]

    def add_manual_variable(self):
        self.cost_vector += [-self.bigM for _ in range(self.num_manual_variable)]
        # 在A矩阵后面加上0列
        for _ in range(self.num_manual_variable):
            for i in range(len(self.a_matrix)):
                self.a_matrix[i] += [0]

        # 生成单位向量并加入index
        for i, j in zip(range(1, self.num_manual_variable+1), self.unit_vector_position):
            self.a_matrix[j][-i] = 1
            self.basis_index.append(len(self.a_matrix[0])-i)
            self.one_index.append(j)

        order_dict = {}
        for i, j in zip(self.basis_index, self.one_index):
            order_dict[i] = j

        # 根据单位矩阵的位置排序，最后返回的basis index必须为对角阵
        order_dict = sorted(order_dict.items(), key=lambda x: x[1], reverse=False)
        self.basis_index = []
        for i in order_dict:
            self.basis_index.append(i[0])

        return self.cost_vector, self.a_matrix, self.b_vector, self.basis_index, self.manual_index
