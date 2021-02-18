import matplotlib.pyplot as plt
import numpy as np


def plot3d_contour(points, ax, contour=True, **params):
    if params is None:
        params = {}
    if contour:
        ax.plot3D(np.append(points[:, 0], [points[0, 0]]),
                  np.append(points[:, 1], [points[0, 1]]),
                  np.append(points[:, 2], [points[0, 2]]),
                  **params)
    else:
        ax.plot3D(points[:, 0], points[:, 1], points[:, 2], **params)


def main():
    print("__________________пункт пятый__________________")
    # input points
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    # plotting
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plot3d_contour(points, ax)

    # transformation matrix
    turn_x = np.radians(float(input('Введите угол поворота относительно оси Х в градусах: ')))
    turn_y = np.radians(float(input('Введите угол поворота относительно оси Y в градусах: ')))
    turn_z = np.radians(float(input('Введите угол поворота относительно оси Z в градусах: ')))
    turn_x_matrix = np.array([[1, 0, 0],
                              [0, np.cos(turn_x), -np.sin(turn_x)],
                              [0, np.sin(turn_x), np.cos(turn_x)]])
    turn_y_matrix = np.array([[np.cos(turn_y), 0, np.sin(turn_y)],
                              [0, 1, 0],
                              [-np.sin(turn_y), 0, np.cos(turn_y)]])
    turn_z_matrix = np.array([[np.cos(turn_z), -np.sin(turn_z), 0],
                              [np.sin(turn_z), np.cos(turn_z), 0],
                              [0, 0, 1]])
    turned_points = points.dot(turn_x_matrix).dot(turn_y_matrix).dot(turn_z_matrix)
    max_coord = max(np.amax(points), np.amax(turned_points))

    # plotting again
    plot3d_contour(turned_points, ax)
    plt.title("Поворот фигуры")
    ax.legend(['Исходная фигура', 'Повёрнутая фигура'])
    ax.set_xlim3d([-max_coord, max_coord])
    ax.set_ylim3d([-max_coord, max_coord])
    ax.set_zlim3d([-max_coord, max_coord])
    plt.show()


if __name__ == "__main__":
    main()
