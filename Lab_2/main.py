"""
Дорогой Даниил,

Прежде чем задавать вопросы по тому, что я уже сделал, попробуй прочитать мои комментарии
Если это не поможет, попробуй найти ответы на вопросы в https://docs.sympy.org/latest/index.html
Если и это не поможет, то я сам в этом, наверно, не разбираюсь, ахвавзавхаз

Лаба в зачаточном состоянии, но это точно тема 2 и вариант 9 (хотя мб и 10, если поймем, как с ним делать)
Ещё не поздно поменять вариант, если это нам будет не под силу
Все источники с инфой я кидал тебе в ЛС ВКонтакте

gl hf
"""
import matplotlib.pyplot as plt
from sympy import nan  # для проверки на NaN
from sympy import Piecewise  # кусочная функция
from sympy import Matrix  # матрицы из sympy
from sympy import plot_parametric  # построение
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


def drawBSpline(points, k):
    N = len(points)  # количество точек
    n = N - 1  # n из материалов Moodle
    X = generateNodalVector(N, k)  # узловой вектор
    J = [[]]  # вектор коэффициентов
    for i in range(0, N):  # начальные коэффициенты (по Moodle это J i,1(t))
        J[0].append(Piecewise((1, (X[i] <= t) & (t < X[i + 1])), (0, True)))
    for cur_k in range(1, k):  # реккурентное задание
        J.append([])  # задание следующих коэффициентов
        for i in range(0, N - 1):  # надо добавить, что 0 / 0 = 0
            J[cur_k].append(J[cur_k - 1][i] * (t - X[i]) / X[i + k - 1] +
                            J[cur_k - 1][i + 1] * (X[i + k] - t) / (X[i + k] - X[i + 1]))
            if J[cur_k][len(J[cur_k]) - 1] == nan:
                J[cur_k][len(J[cur_k]) - 1] = 0
        J[cur_k].append(J[cur_k - 1][N - 1] * (t - X[N - 1]) / X[N + k - 2])  # обработка последнего отдельно, так как
        # здесь уже не существует J[cur_k - 1][i + 1]
    P = J[k - 1][0] * points[0]  # создание итоговой функции
    for i in range(1, N):
        P = P + J[k - 1][i] * points[i]
    # координата x - print(P.row(0))
    # координата y - print(P.row(1))
    plot_parametric((P.row(0), P.row(1)), (t, 0, n - k + 2))  # вывод, который не работает (ГЛАВНАЯ ПРОБЛЕМА)


def main():
    points = [Matrix([float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')])
              for i in range(1, int(input('Введите количество точек: ')) + 1)]
    k = int(input('Введите порядок B-сплайна (0 для всех от 1 до N-1): '))
    # plotting
    plt.figure()
    ax = plt.axes()
    plot_contour(points, ax)
    if k != 0:
        drawBSpline(points, k)
    else:
        for i in range(1, len(points)):  # условно, надо сначала с одиночным случаем разобраться
            drawBSpline(points, i)
    plt.show()


if __name__ == "__main__":
    main()
