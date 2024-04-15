import numpy as np

n_value = int(input('Введите количество коэффициентов при переменных в целевой функции: '))
array_function = [-4, -3, 2, 0, 0, 0, 0]
array_function.insert(0, 0)
print('Коэффициенты при переменных в целевой функции: ', array_function)

# Создание матрицы ограничений
n_constraints = int(input('Введите количество ограничений: '))
matrix_constraints = [[1, 3, 0, 1, 0, 0, 0], [-1, 3, 0, 0, 0, 1, 0], [-4, -4, 3, 0, -1, 0, 1]]
right_constraints = [5, 7, 5]

for i in range(n_constraints):
    matrix_constraints[i].insert(0, right_constraints[i])
print('Исходная симплекс таблица: \n', np.array(matrix_constraints))

# Инициализация пустого списка базисов
basis = [0, 0, 0]

# Инициализация списка дельт
delta = [0] * (n_value + 1)


def finding_delta_list(delta_arr, matrix, n_const):
    for i in range(n_const + 1):
        value = 0
        for j in range(len(basis)):
            value = value + basis[j] * matrix[j][i]
        delta_arr[i] = value - array_function[i]
    print('delta: ', delta_arr, '\n')
    return delta_arr


def finding_resolving_post(delta_list):
    # Определение разрешающего столбца
    value_j = 0
    index_j = 0
    flag_j = False
    for i in range(1, len(delta_list)):
        if delta_list[i] < 0:
            if abs(delta_list[i] > abs(value_j)) or flag_j == False:
                value_j = delta_list[i]
                index_j = i
                flag_j = True
    print('Индекс(номер) разрешающего столбца: ', index_j, '\n')
    return value_j, index_j, flag_j


def finding_teta_arr(n_const, basis_arr, right_const, matrix, index_j):
    # Инициализация столбца тета
    teta_table = [0] * n_const
    for i in range(len(basis_arr)):
        if matrix[i][index_j] == 0:
            teta_table[i] = -1
        else:
            teta_table[i] = right_const[i] / matrix[i][index_j]
    print('Тета столбец: ', teta_table, '\n')
    return teta_table


def finding_resolving_list(teta_arr):
    # Определение разрешающей строки
    value_i = 0
    index_i = 0
    flag_i = False
    for i in range(len(teta_arr)):
        if teta_arr[i] > 0:
            if teta_arr[i] < value_i or flag_i == False:
                flag_i = True
                value_i = teta_arr[i]
                index_i = i
    print('Индекс разрешающей строки: ', index_i, '\n')
    return value_i, index_i, flag_i


def creating_new_table(n_val, n_const, matrix, index_i, index_j, count_iter):
    # Формирование новой таблицы

    new_matrix = []
    for i in range(n_const):
        new_matrix.append([0] * (n_val + 1))

    for i in range(n_val + 1):
        for j in range(n_const):
            if j != index_i and i != index_j:
                new_matrix[j][i] = (matrix[j][i] * matrix[index_i][index_j] -
                                    matrix[index_i][i] * matrix[j][index_j]) / matrix[index_i][index_j]
            elif j == index_i and i != index_j:
                new_matrix[j][i] = matrix[j][i] / matrix[index_i][index_j]
            elif j != index_i and i == index_j:
                new_matrix[j][i] = 0
            else:
                new_matrix[j][i] = 1
    print('Симплекс таблица после ', count_iter, ' итерации: \n', np.array(new_matrix))
    return new_matrix


def print_optim(basis_index_list, matrix, delta_list):
    for i in range(len(basis_index_list)):
        print('X', i + 1, ' = ', matrix[basis_index_list.index(i + 1)][0], sep="")
    print('fun = ', delta_list[0])


def prov_basis(basis_index_list):
    flg = True
    for i in range(1, 4):
        result = basis_index_list.count(i)
        if result > 0:
            flg = True
        else:
            flg = False
            break
    return flg


flag_whil = True
count = 1

# Ввод списка, хранящего порядок определяемых элементов
basis_index = [0] * n_constraints

while flag_whil:
    delta = finding_delta_list(delta, matrix_constraints, n_value)

    # Нахождение индекса разрешающего столбца
    value_allow_j, index_allow_j, flag_post = finding_resolving_post(delta)
    if flag_post == False:
        if prov_basis(basis_index) == True:
            print('План оптимален \n')
            print_optim(basis_index, matrix_constraints, delta)
            flag = False
            break

    # Определение столбца тета
    teta_table = finding_teta_arr(n_constraints, basis, right_constraints, matrix_constraints, index_allow_j)

    # Нахождение индекса разрешающей строки
    value_allow_i, index_allow_i, flag_list = finding_resolving_list(teta_table)
    if flag_list == False:
        print('Оптимального плана нет!')
        flag = False
        break

    basis_index[index_allow_i] = index_allow_j

    # Переопределение базисного столбца
    basis[index_allow_i] = array_function[index_allow_j]

    # Определение новой симплекс таблицы
    matrix_constraints = creating_new_table(n_value, n_constraints, matrix_constraints, index_allow_i, index_allow_j,
                                            count)
    count = count + 1