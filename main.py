from algorithm.problem_generation import Problem
from algorithm.branch_and_bound import BranchAndBound
from algorithm.genetic_algorithm import NaiveGeneticAlgorithm


def func(variables):
    x = variables[0]
    y = variables[1]
    return -(x-1)**2 - (y-2)**2 + 5


def main():
    # # 生成cost向量
    # pb = Problem([40, 90], max_problem=True)
    # # 约束时保证维度一致
    # pb.add_constraint([9, 7], '<=', 56)
    # pb.add_constraint([7, 20], '<=', 70)
    #
    # # 普通线性规划
    # # solver会打印并返回结果
    # # pb.solver()
    #
    # # 整型规划
    # integer_index = [1]
    # c, a, b, symbol = pb.origin()
    # pb_ilp = BranchAndBound(integer_index, c, a, b, symbol)
    # result = pb_ilp.solver()
    # for i, j in zip(result[0], result[1]):
    #     print('x_{} is {}'.format(i, j))
    #
    # print('最大值为{}'.format(result[2]))

    # 遗传算法
    sol_range = {0: [-5, 5], 1: [-5, 5]}  # 指定自变量区间
    pb = NaiveGeneticAlgorithm(size=50, dimension=2, sol_range=sol_range,
                               chrom_size=25, cp=0.8, mp=0.1, gen_max=500, fitness_function=func, fitness_symbol='+-')
    pb.solver()


if __name__ == '__main__':
    main()

