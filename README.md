# OperationsResearchSolver
A Self-made OR solver by Adrian Chen.

## Introduction

This is a simple OR solver with simplex method, Big-M method, branch-and-bound and cutting plane algorithms.


## Example
Consider a simple linear programming problem:

<img src="./example.jpg" width = "1000"/>


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

## To-do-list
1. ~~Simplex method~~

2. ~~Big-M method~~

3. Branch-and-bound

4. Cutting plane

5. Solution conditions judgement

6. Add multi-constraints at same time
