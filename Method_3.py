import scipy.optimize as opt

# funcF = [-4, -3, 2]
# Arr_left_constraints = [[1, 3, 0], [4, 4, -3]]
# Arr_right_constraints = [5, -5]
#
# left_const = [[-1, 3, 0]]
# right_const = [7]

# bnd = [(0, float("inf")), (0, float("inf")), (0, float("inf"))]
# res = opt.linprog(c=funcF, A_ub=Arr_left_constraints, b_ub=Arr_right_constraints, A_eq=left_const, b_eq=right_const, bounds=bnd)

# Проверка кода, по примеру из лекции
funcF = [-3, 0, -2]
Arr_left_constraints = [[-2, -1, 5], [1, 0, -2], [0, 2, -1]]
Arr_right_constraints = [6, 2, 5]

bnd = [(0, float("inf")), (0, float("inf")), (0, float("inf"))]
res = opt.linprog(c=funcF, A_ub=Arr_left_constraints, b_ub=Arr_right_constraints, bounds=bnd)

print(res)