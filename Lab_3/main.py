import matplotlib.pyplot as plt  # библиотека для визуализации
from sympy import Piecewise  # кусочная функция
from sympy import Matrix  # матрицы из sympy
from numpy import linspace  # генератор промежуточных точек
from sympy.abc import t, u  # t, u в качестве символьной переменной (чтобы не использовать symbols() или var())
import numpy as np
from math import cos, sin, radians


def amax(obj):
    if isinstance(obj, list):
        return max([amax(sub_list) for sub_list in obj])
    else:
        return obj


def my_dot(lhs, rhs):
    if len(lhs) == 0:
        raise IndexError
    elif len(rhs) == 0:
        raise IndexError
    elif len(lhs[0]) == 0:
        raise IndexError
    elif len(rhs[0]) == 0:
        raise IndexError
    else:
        for row in lhs:
            if len(row) != len(lhs[0]) or len(row) != len(rhs):
                raise IndexError
        for row in rhs:
            if len(row) != len(rhs[0]):
                raise IndexError
        answer = [[sum([lhs[m][current] * rhs[current][n]
                        for current in range(0, len(rhs))])
                   for n in range(0, len(rhs[0]))]
                  for m in range(0, len(lhs))]
        return answer


def plot3d_wireframe(points, ax, **params):
    if params is None:
        params = {}
    x = np.array([[point[0] for point in points_row] for points_row in points], dtype='float64')
    y = np.array([[point[1] for point in points_row] for points_row in points], dtype='float64')
    z = np.array([[point[2] for point in points_row] for points_row in points], dtype='float64')
    ax.plot_wireframe(x, y, z, **params)


def plot3d_surface(points, ax, alpha=1.0, **params):
    if params is None:
        params = {}
    x = np.array([[point[0] for point in points_row] for points_row in points], dtype='float64')
    y = np.array([[point[1] for point in points_row] for points_row in points], dtype='float64')
    z = np.array([[point[2] for point in points_row] for points_row in points], dtype='float64')
    ax.plot_surface(x, y, z, alpha=alpha, **params)


def generateNodalVector(n, k):  # генерация узлового вектора
    return_list = []
    for i in range(n + k + 1):
        if i < k:
            return_list.append(0)
        elif i <= n:
            return_list.append(i - k + 1)
        else:
            return_list.append(n - k + 2)
    return return_list


def generateBasicFunctions(X, k, var):  # построение вектора базисных функций
    J = []
    if k == 1:
        for i in range(0, len(X) - 1):
            J.append(Piecewise((1, (X[i] <= var) & (var < X[i + 1])), (0, True)))
    else:
        J_previous = generateBasicFunctions(X, k - 1, var)
        for i in range(0, len(J_previous) - 1):
            if X[i + k - 1] - X[i] == 0:  # проверка деления на 0
                first_operand = 0
            else:
                first_operand = J_previous[i] * (var - X[i]) / (X[i + k - 1] - X[i])
            if X[i + k] - X[i + 1] == 0:  # проверка деления на 0
                second_operand = 0
            else:
                second_operand = J_previous[i + 1] * (X[i + k] - var) / (X[i + k] - X[i + 1])
            J.append(first_operand + second_operand)
    return J


def drawBSplineSurface(points, m: int, n: int, ax):  # отрисовка B-сплайновой поверхности
    X1 = generateNodalVector(m, m)  # узловой вектор
    J1 = generateBasicFunctions(X1, m, t)  # рекурсивное создание базисных функций
    X2 = generateNodalVector(n, n)  # узловой вектор
    J2 = generateBasicFunctions(X2, n, u)  # рекурсивное создание базисных функций
    P = Matrix([[0], [0], [0]])
    for i in range(0, m + 1):
        for j in range(0, n + 1):
            P = P + J1[i] * J2[j] * Matrix(points[i][j])
    x_func = P[0]  # выделение функций для каждой из координат
    y_func = P[1]
    z_func = P[2]
    spline_points = []
    t_values = linspace(0, 1.99999, 30)  # значения параметра для построения
    u_values = linspace(0, 1.99999, 30)
    for t_value in t_values:
        spline_points.append([])
        for u_value in u_values:
            spline_points[-1].append([x_func.subs([(t, t_value), (u, u_value)]),
                                      y_func.subs([(t, t_value), (u, u_value)]),
                                      z_func.subs([(t, t_value), (u, u_value)])])
    plot3d_surface(spline_points, ax)


def main():
    with open("input.txt", 'r') as cin:
        m = int(cin.readline())
        n = int(cin.readline())
        if m < 3 or n < 3:
            print('Нельзя построить b-сплайновую поверхность')
            return 0
        points = [[[float(elem) for elem in cin.readline().split(',')]
                   for j in range(1, n + 2)] for i in range(1, m + 2)]
    # m = int(input('Введите первый порядок b-сплайновой поверхности: '))
    # n = int(input('Введите второй порядок b-сплайновой поверхности: '))
    # if m < 3 or n < 3:
    #     print('Нельзя построить b-сплайновую поверхность')
    #     return 0
    # points = [[[float(elem) for elem in input(f'Введите точку задающего многогранника [{i}][{j}]: ').split(',')]
    #            for j in range(1, n + 2)] for i in range(1, m + 2)]
    # построение
    plt.figure()
    ax = plt.axes(projection='3d')
    plot3d_wireframe(points, ax)
    drawBSplineSurface(points, m, n, ax)

    turn_x = radians(float(input('Введите угол поворота относительно оси Х в градусах: ')))
    turn_y = radians(float(input('Введите угол поворота относительно оси Y в градусах: ')))
    turn_x_matrix = [[1, 0, 0],
                     [0, cos(turn_x), -sin(turn_x)],
                     [0, sin(turn_x), cos(turn_x)]]
    turn_y_matrix = [[cos(turn_y), 0, sin(turn_y)],
                     [0, 1, 0],
                     [-sin(turn_y), 0, cos(turn_y)]]
    turned_points = [my_dot(my_dot(elem, turn_x_matrix), turn_y_matrix) for elem in points]
    max_coord = amax([points, turned_points])
    drawBSplineSurface(turned_points, m, n, ax)
    ax.plot([0, max_coord], [0, 0], [0, 0])
    ax.plot([0, 0], [0, max_coord], [0, 0])
    ax.plot([0, 0], [0, 0], [0, max_coord])
    plt.title(f'Построение B-сплайна {m}-{n} порядка')
    plt.legend(['Ось X', 'Ось Y', 'Ось Z'])
    plt.show()
    # while True:
    #     point_for_change = int(input('Введите 0 для выхода или номер точки для изменения её координат: '))
    #     if point_for_change == 0:
    #         break
    #     else:
    #         points[point_for_change - 1] = [float(elem)
    #                                         for elem in
    #                                         input(f'Введите точку фигуры {point_for_change}: ').split(',')]
    #         plt.figure()
    #         ax = plt.axes(projection='3d')
    #         plot3d_surface(points, ax)
    #         drawBSplineSurface(points, m, n, ax)
    #         # plt.title(f'Построение B-сплайна {k}-ого порядка')
    #         # plt.legend(['Исходные точки', f'B-сплайн {k}-ого порядка'])
    #         plt.show()


if __name__ == "__main__":
    main()
