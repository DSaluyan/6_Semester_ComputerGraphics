import matplotlib.pyplot as plt
from sympy import nan  # для проверки на NaN
from sympy import Piecewise  # кусочная функция
from sympy import Matrix  # матрицы из sympy
from numpy import linspace  # range для нецелых
from sympy.abc import t  # t в качестве символьной переменной (чтобы не использовать symbols() или var())


def plot_contour(points, ax, contour=True, **params):  # из первой лабы, но без 3D
    if params is None:
        params = {}
    x = [points[i][0] for i in range(0, len(points))]
    y = [points[i][1] for i in range(0, len(points))]
    if contour:
        ax.plot([*x, points[0][0]],
                [*y, points[0][1]],
                **params)
    else:
        ax.plot(x, y, **params)


def generateNodalVector(N, k):  # генерация узлового вектора (это 100% правильно, но перепроверь)
    return_list = []
    n = N - 1
    for i in range(n + k + 1):
        if i < k:
            return_list.append(0)
        elif i <= n:
            return_list.append(i - k + 1)
        else:
            return_list.append(n - k + 2)
    return return_list


def drawBSpline(points, k: int, ax):
    N = len(points)  # количество точек
    n = N - 1  # n из материалов Moodle
    X = generateNodalVector(N, k)  # узловой вектор
    J = [[]]  # вектор коэффициентов
    for i in range(0, n + k):  # начальные коэффициенты (по Moodle это J i,1(t))
        J[0].append(Piecewise((1, (X[i] <= t) & (t < X[i + 1])), (0, True)))
    for cur_k in range(0, k - 1):  # реккурентное задание (ТЕПЕРЬ ОШИБКА ЗДЕСЬ, А ВЫВОД РАБОТАЕТ)
        J.append([])  # задание следующих коэффициентов
        for i in range(0, len(J[cur_k]) - 1):
            # print(cur_k + 1, i, "_______")
            # print((t - X[i]) / X[i + cur_k - 1])
            # print((X[i + cur_k] - t) / (X[i + cur_k] - X[i + 1]))
            J[cur_k + 1].append(J[cur_k][i] * (t - X[i]) / X[i + cur_k - 1] +
                                J[cur_k][i + 1] * (X[i + cur_k] - t) / (X[i + cur_k] - X[i + 1]))
            if J[cur_k + 1][-1] == nan:
                J[cur_k + 1][-1] = 0
    P = J[k - 1][0] * points[0]  # создание итоговой функции
    for i in range(1, N):
        P = P + J[k - 1][i] * points[i]
    x_func = P[0]
    y_func = P[1]
    spline_points = []
    t_values = linspace(0, n - k + 2, 100)
    for t_value in t_values[:-1]:
        spline_points.append([x_func.subs(t, t_value), y_func.subs(t, t_value)])
    plot_contour(spline_points, ax, contour=False)


def main():
    points = [Matrix([float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')])
              for i in range(1, int(input('Введите количество точек: ')) + 1)]
    k = int(input('Введите порядок B-сплайна (0 для всех от 1 до N-1): '))
    # plotting
    plt.figure()
    ax = plt.axes()
    plot_contour(points, ax, contour=False)
    if k != 0:
        drawBSpline(points, k, ax)
    else:
        for i in range(1, len(points)):  # условно, надо сначала с одиночным случаем разобраться
            drawBSpline(points, i, ax)
    plt.show()


if __name__ == "__main__":
    main()
