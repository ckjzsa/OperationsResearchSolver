# OperationsResearchSolver
A Self-developed OR solver by Adrian Chen.

## Introduction

This is a simple OR solver with simplex method, Big-M method, branch-and-bound and cutting plane algorithms.


## Example
### Simple LP
Consider a simple linear programming problem:

<img src="./examples/LP.png" width = "400"/>


Then you can solve this problem with code below:
```
def main():
    pb = Problem([0, 0.1, 0.2, 0.3, 0.8], max_problem=False)
    # 约束时保证维度一致
    pb.add_constraint([1, 2, 0, 1, 0], '=', 100)
    pb.add_constraint([0, 0, 2, 2, 1], '=', 100)
    pb.add_constraint([3, 1, 2, 0, 3], '=', 100)
    c, a, b = pb.standardization()
    pb_bigm = BigM(c, a, b)
    c, a, b, basis_index = pb_bigm.add_manual_variable()
    initialization = SimplexMethod(c, a, b, basis_index)
    x_index, x_value, z_value = initialization.solver()
    x_index += 1
    for x, value in zip(x_index, x_value):
        print('x_{} is {}'.format(x, value))
    print('The maximum value of this question is {}'.format(z_value[0]))
```

### Integer LP 
Consider a integer linear programming problem:

<img src="./examples/MIP.png" width = "400"/>


Then you can solve this problem with code below:
```
def main():
    pb = Problem([40, 90], max_problem=True)
    # 约束时保证维度一致
    pb.add_constraint([9, 7], '<=', 56)
    pb.add_constraint([7, 20], '<=', 70)

    # 整型规划
    integer_index = [0, 1]
    c, a, b, symbol = pb.origin()
    pb_ilp = BranchAndBound(integer_index, c, a, b, symbol)
    result = pb_ilp.solver()
    for i, j in zip(result[0], result[1]):
        print('x_{} is {}'.format(i, j))
    print('最大值为{}'.format(result[2]))
```

### Genetic Algorithm
Consider a simple multi-variable optimization problem:

<img src="./examples/GA.png" width = "200"/>


The user should define functions first, the variables should be input as a list:
```
def func(variables):
    x = variables[0]
    y = variables[1]
    return -(x-1)**2 - (y-2)**2 + 5
```
Then initialize genetic algorithm solver and solve it:
```
def main():
    # 遗传算法
    sol_range = {0: [-5, 5], 1: [-5, 5]}  # 指定自变量区间
    pb = NaiveGeneticAlgorithm(size=50, dimension=2, sol_range=sol_range,
                               chrom_size=25, cp=0.8, mp=0.1, gen_max=500, fitness_function=func, fitness_symbol='+-')
    pb.solver()

```
Which should be noted is that  ```fitness_symbol``` indicates the range of functions: '+' means greater than zero, '-' means less than zero, while '+-' or '-+' means all real numbers.

## Debug
1. Pivot in simplex method is based on B inverse b, not P;

2. Fix the problem that the initial basis should be a diagonal matrix rather than a random unit matrix.

3. Optimize bound judgement in ILP solver.

4. Introduce old-solution-buffer to avoid endless loop.

5. Adjust genetic algorithm in terms of negative/positive values of fitness.


## To-do-list
1. ~~Simplex method~~

2. ~~Big-M method~~

3. ~~Branch-and-bound~~

4. Cutting plane

5. ~~Solution conditions judgement~~

6. Add multi-constraints at same time

7. 0-1 integer programming

8. ~~Genetic algorithm~~

9. Dual problem generation

10. Column generation

11. Branch and price

## Cite my solver
    @misc{adrianorsolver,
    title={Operations Research Solver},
    author={Chen, Kehua},
    url={https://github.com/ckjzsa/OperationsResearchSolver/},
    year={2020},
    publisher={Github}}

