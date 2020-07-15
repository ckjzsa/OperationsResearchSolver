from OperationsResearchSolver.algorithm.problem_generation import Problem


def main():
    pb = Problem([0, 0.1, 0.2, 0.3, 0.8], max_problem=False)
    # 约束时保证维度一致
    pb.add_constraint([1, 2, 0, 1, 0], '=', 100)
    pb.add_constraint([0, 0, 2, 2, 1], '=', 100)
    pb.add_constraint([3, 1, 2, 0, 3], '=', 100)
    # solver会打印并返回结果
    pb.solver()


if __name__ == '__main__':
    main()

