import numpy as np
import warnings
warnings.filterwarnings('ignore')


class SimplexMethod:
    def __init__(self, c_vector, a_matrix, b_vector, basis_index):
        temp = np.array([a_matrix[0]])
        for i in range(1, len(a_matrix)):
            temp = np.concatenate([temp, np.array([a_matrix[i]])], axis=0)

        self.c_vector = np.array(c_vector).astype(float)
        self.a_matrix = temp.astype(float)
        self.b_vector = np.array(b_vector).astype(float)
        non_basis_index = []
        for i in range(len(c_vector)):
            if i not in basis_index:
                non_basis_index.append(i)

        # 初始化基与非基部分
        self.non_basis = self.a_matrix[:, non_basis_index]
        self.basis = self.a_matrix[:, basis_index]  # 初始基
        self.basis_index = np.array(basis_index)
        self.non_basis_index = np.array(non_basis_index)
        self.cost_basis = np.array([self.c_vector[i] for i in self.basis_index])
        self.cost_nonbasis = np.array([self.c_vector[i] for i in self.non_basis_index])

    def solver(self):
        # 1. 计算非基变量的检验数
        b = np.dot(np.linalg.inv(self.basis), self.non_basis)
        sigma_non = self.cost_nonbasis - np.dot(np.dot(self.cost_basis, np.linalg.inv(self.basis)), self.non_basis)
        # 2. 检验数最大的换入基变量
        x_in = sigma_non.tolist().index(max(sigma_non))
        B_inv_b = np.dot(np.linalg.inv(self.basis), self.b_vector)
        B_inv_p = np.dot(np.linalg.inv(self.basis), self.non_basis[:, x_in])
        # 3. theta最小的换出基变量
        theta = np.stack(B_inv_b, axis=1) / B_inv_p
        # 除去负值
        for i in range(len(theta[0])):
            if theta[0][i] < 0:
                theta[0][i] = np.nan_to_num(np.inf)
        x_out = np.nan_to_num(theta)[0].tolist().index(min(np.nan_to_num(theta)[0]))

        # 4. 开始循环迭代，直到检验数均小于0
        while max(sigma_non) > 0:
            # 找到主元，构建行变换矩阵
            pivot = B_inv_p[x_out]  # 注意主元在B-1P中，不在P中
            P = self.non_basis[:, x_in].copy()
            for i in range(len(P)):
                if i == x_out:
                    P[i] = 1 / pivot
                else:
                    P[i] = -P[i] / pivot
            E = np.eye(len(self.basis_index))
            E[:, x_out] = P

            # 得到新的B-1b
            B_inv_b = np.dot(E, B_inv_b)

            # 交换序号
            self.basis_index[x_out], self.non_basis_index[x_in] = self.non_basis_index[x_in], self.basis_index[x_out]
            # 交换系数矩阵
            P_out = self.basis[:, x_out].copy()
            P_in = self.non_basis[:, x_in].copy()
            self.basis[:, x_out] = P_in
            self.non_basis[:, x_in] = P_out
            # 交换cost向量
            self.cost_basis[x_out], self.cost_nonbasis[x_in] = self.cost_nonbasis[x_in], self.cost_basis[x_out]

            # 计算新的检验数
            try:
                sigma_non = self.cost_nonbasis - np.dot(np.dot(self.cost_basis, np.linalg.inv(self.basis)), self.non_basis)
            except Exception:
                return False

            x_in = sigma_non.tolist().index(max(sigma_non))
            B_inv_p = np.dot(np.linalg.inv(self.basis), self.non_basis[:, x_in])

            # theta最小的换出基变量
            theta = np.stack(B_inv_b, axis=1) / B_inv_p
            # 除去负值
            for i in range(len(theta[0])):
                if theta[0][i] < 0:
                    theta[0][i] = np.nan_to_num(np.inf)
            x_out = np.nan_to_num(theta)[0].tolist().index(min(np.nan_to_num(theta)[0]))

        res_x = self.basis_index
        res_B_inv_b = np.dot(np.linalg.inv(self.basis), self.b_vector)
        res_z = np.dot(self.cost_basis, res_B_inv_b)
        res_B_inv_b = np.stack(res_B_inv_b, axis=1)[0]

        return [res_x, res_B_inv_b, res_z]

