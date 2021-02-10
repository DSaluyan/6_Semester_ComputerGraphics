import matplotlib.pyplot as plt
import numpy as np


def plot_contour(points, ax, params=None):
    if params is None:
        params = {}
    ax.plot(np.append(points[:, 0], [points[0, 0]]),
            np.append(points[:, 1], [points[0, 1]]),
            **params)


def main():
    # input points
    points = np.array([[float(elem) for elem in input(f'Введите точку {i}: ').split(',')]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])

    # plotting
    fig, ax = plt.subplots()
    plot_contour(points, ax)

    # transformation matrix
    T = np.array([[1, 0], [0, 1]])
    T = T * np.array([-1, -1])
    points = np.dot(points, T)

    # plotting again
    plot_contour(points, ax)
    plt.title("Отображение фигуры")
    plt.show()


if __name__ == "__main__":
    main()
