import numpy as np
import math
from algorithm.problem_generation import Problem
from algorithm.big_m import BigM
from algorithm.simplex_method import SimplexMethod
import copy


class BranchAndBound:
    def __init__(self, integer_index, cost_vector, a_matrix=[], b_vector=[], logic_symbol=[], max_problem=True):
        if max_problem:
            self.cost_vector = copy.deepcopy(cost_vector)
        else:
            self.cost_vector = [i * -1 for i in cost_vector]

        self.a_matrix = copy.deepcopy(a_matrix)
        self.b_vector = copy.deepcopy(b_vector)
        self.logic_symbol = copy.deepcopy(logic_symbol)
        self.integer_index = integer_index

        self.queue = []

        # 获得初始解
        pb = Problem(cost_vector, a_matrix, b_vector, logic_symbol, max_problem, ilp=True)
        [x_index, x_value, z_value] = pb.solver()

        initial_res = [x_index, x_value, z_value]
        # 初始上界和下界
        self.upper_bound = z_value
        self.lower_bound = 0

        self.queue.append([initial_res, self.cost_vector, self.a_matrix, self.b_vector, self.logic_symbol])

        pass

    def solver(self):
        while self.queue:
            # 获取队列中的数据
            res = self.queue[0][0]
            c = self.queue[0][1]
            a = self.queue[0][2]
            b = self.queue[0][3]
            symbol = self.queue[0][4]
            self.queue.pop(0)

            # 获得初值
            initial_x_index = [i-1 for i in res[0]]
            initial_x_value = res[1]
            initial_z_value = res[2]

            if initial_z_value < self.lower_bound:
                continue

            branch_index = None
            branch_value = None

            # 寻找非整数的解
            for x_index, x_value in zip(initial_x_index, initial_x_value):
                if x_index in self.integer_index and math.ceil(x_value) != x_value:
                    branch_index = x_index
                    branch_value = x_value
                    break

            if branch_index is None:  # 所有解均为整数, 更新下界
                if initial_z_value > self.lower_bound:
                    self.lower_bound = initial_z_value
                    self.opt_z = initial_z_value

            # 进行分支
            # 小于的部分
            c_less = copy.deepcopy(c)
            a_less = copy.deepcopy(a)
            b_less = copy.deepcopy(b)
            symbol_less = copy.deepcopy(symbol)

            pb_less = Problem(c_less, a_less, b_less, symbol_less, ilp=True)
            add_a = [0] * len(a[0])
            add_a[branch_index] = 1
            pb_less.add_constraint(add_a, '<=', math.floor(branch_value))
            res_less = pb_less.solver()

            # 补充判断是否有可行解
            if not res_less:
                pass
            else:
                integer_count = 0
                for x_index, x_value in zip([i-1 for i in res_less[0]], res_less[1]):
                    if x_index in self.integer_index and math.ceil(x_value) != x_value and res_less[2] < self.upper_bound:
                        self.upper_bound = res_less[2]
                    elif x_index in self.integer_index and math.ceil(x_value) == x_value:
                        # 全部满足整数条件
                        integer_count += 1
                if integer_count == len(self.integer_index) and res_less[2] > self.lower_bound:
                    self.lower_bound = res_less[2]
                    self.result = res_less
                elif res_less[2] < self.lower_bound:  # 如果结果小于下界，则不满足要求
                    pass
                else:
                    # 生成新的约束，加入队列
                    add_a = [0] * len(a[0])
                    add_a[branch_index] = 1
                    c_queue_less = copy.deepcopy(c)
                    a_queue_less = copy.deepcopy(a)
                    a_queue_less.append(add_a)
                    b_queue_less = copy.deepcopy(b)
                    b_queue_less.append([math.floor(branch_value)])
                    symbol_queue_less = copy.deepcopy(symbol)
                    symbol_queue_less.append(['<='])
                    self.queue.append([res_less, c_queue_less, a_queue_less, b_queue_less, symbol_queue_less])

            # 大于的部分
            c_more = copy.deepcopy(c)
            a_more = copy.deepcopy(a)
            b_more = copy.deepcopy(b)
            symbol_more = copy.deepcopy(symbol)
            pb_more = Problem(c_more, a_more, b_more, symbol_more, ilp=True)
            add_a = [0] * len(a[0])
            add_a[branch_index] = 1
            pb_more.add_constraint(add_a, '>=', math.ceil(branch_value))
            res_more = pb_more.solver()

            if not res_more:
                pass
            else:
                integer_count = 0
                for x_index, x_value in zip([i-1 for i in res_more[0]], res_more[1]):
                    if x_index in self.integer_index and math.ceil(x_value) != x_value and res_more[2] < self.upper_bound:
                        self.upper_bound = res_more[2]
                    elif x_index in self.integer_index and math.ceil(x_value) == x_value:
                        # 全部满足整数条件
                        integer_count += 1
                if integer_count == len(self.integer_index) and res_more[2] > self.lower_bound:
                    self.lower_bound = res_more[2]
                    self.result = res_more
                elif res_more[2] < self.lower_bound:
                    pass
                else:
                    # 生成新的约束，加入队列
                    add_a = [0] * len(a[0])
                    add_a[branch_index] = 1
                    c_queue_more = copy.deepcopy(c)
                    a_queue_more = copy.deepcopy(a)
                    a_queue_more.append(add_a)
                    b_queue_more = copy.deepcopy(b)
                    b_queue_more.append([math.ceil(branch_value)])
                    symbol_queue_more = copy.deepcopy(symbol)
                    symbol_queue_more.append(['>='])
                    self.queue.append([res_more, c_queue_more, a_queue_more, b_queue_more, symbol_queue_more])

        return self.result
