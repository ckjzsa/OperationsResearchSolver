from OperationsResearchSolver.algorithm.problem_generation import Problem
from OperationsResearchSolver.algorithm.branch_and_bound import BranchAndBound


def main():
    pb = Problem([40, 90], max_problem=True)
    # 约束时保证维度一致
    pb.add_constraint([9, 7], '<=', 56)
    pb.add_constraint([7, 20], '<=', 70)

    # solver会打印并返回结果
    pb.solver()

    # 整型规划
    ILP = True
    c, a, b = pb.standardization()
    pb_ilp = BranchAndBound(c, a, b)


if __name__ == '__main__':
    main()

