from algorithm.problem_generation import Problem
from algorithm.branch_and_bound import BranchAndBound


def main():
    pb = Problem([40, 90], max_problem=True)
    # 约束时保证维度一致
    pb.add_constraint([9, 7], '<=', 56)
    pb.add_constraint([7, 20], '<=', 70)

    # solver会打印并返回结果
    # pb.solver()

    # 整型规划
    integer_index = [0, 1]
    c, a, b, symbol = pb.origin()
    pb_ilp = BranchAndBound(integer_index, c, a, b, symbol)
    result = pb_ilp.solver()
    for i, j in zip(result[0], result[1]):
        print('x_{} is {}'.format(i, j))

    print('最大值为{}'.format(result[2]))


if __name__ == '__main__':
    main()

