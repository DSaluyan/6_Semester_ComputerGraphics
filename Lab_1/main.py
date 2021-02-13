import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg
from math import inf


def plot_contour(points, ax, contour=True, **params):
    if params is None:
        params = {}
    if contour:
        ax.plot(np.append(points[:, 0], [points[0, 0]]),
                np.append(points[:, 1], [points[0, 1]]),
                **params)
    else:
        ax.plot(points[:, 0], points[:, 1], **params)


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
    print("__________________пункт первый__________________")
    # input points
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    # plotting
    fig, ax = plt.subplots()
    plot_contour(points, ax)

    # transformation matrix
    scale = float(input('Введите масштаб: '))
    x_mirror = bool(input('Отразить относительно оси X? (1 - Да / 0 - нет): '))
    y_mirror = bool(input('Отразить относительно оси Y? (1 - Да / 0 - нет): '))
    T = np.array([[scale * int(-1 if x_mirror else 1), 0], [0, scale * int(-1 if y_mirror else 1)]])
    points = np.dot(points, T)

    # plotting again
    plot_contour(points, ax)
    plt.title("Отражение фигуры")
    ax.legend(['Исходная фигура', 'Отраженная фигура'])
    plt.axis('equal')
    plt.show()

    print("__________________пункт второй__________________")
    while True:
        line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
                         for i in range(1, 3)])
        if line[0] == line[1]:
            print("Точки должны быть разными! Попробуйте ещё раз")
        else:
            break
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')] + [1]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    while True:
        # plotting original figure
        fig, ax = plt.subplots()

        plot_contour(line, ax)
        plot_contour(points[:, 0:2], ax)

        # transformation matrices
        try:
            turn_value = -np.arctan((line[0][1] - line[1][1]) / (line[0][0] - line[1][0]))
        except:
            turn_value = -np.arctan(inf)
        move_matrix = np.array([[1, 0, 0], [0, 1, 0], [-line[0][0], -line[0][1], 1]])
        turn_matrix = np.array([[np.cos(turn_value), np.sin(turn_value), 0],
                                [-np.sin(turn_value), np.cos(turn_value), 0],
                                [0, 0, 1]])
        mirror_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        mirrored_points = points.dot(move_matrix).dot(turn_matrix).dot(mirror_matrix). \
            dot(linalg.inv(turn_matrix)).dot(linalg.inv(move_matrix))

        # plotting mirrored figure
        plot_contour(mirrored_points[:, 0:2], ax)
        plt.title('Отражение фигуры относительно прямой')
        ax.legend(['Линия', 'Исходная фигура', 'Отраженная фигура'])
        plt.axis('equal')
        plt.show()
        print('Выберите действие: \n1 - изменить прямую \n2 - перейти к третьему пункту \n> ', end='')
        ch = int(input())
        if ch == 1:
            line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
                             for i in range(1, 3)])
        elif ch == 2:
            break

    print('__________________пункт третий__________________')
    turning_point = np.array([[float(elem) for elem in input(f'Введите координаты точки: ').split(',')]])
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')] + [1]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    turn_value = np.radians(float(input('Введите угол в градусах: ')))
    while True:
        # plotting original figure
        fig, ax = plt.subplots()

        plot_contour(turning_point, ax)
        plot_contour(points[:, 0:2], ax)

        # transformation matrices
        move_matrix = np.array([[1, 0, 0], [0, 1, 0], [-turning_point[0][0], -turning_point[0][1], 1]])
        turn_matrix = np.array([[np.cos(turn_value), np.sin(turn_value), 0],
                                [-np.sin(turn_value), np.cos(turn_value), 0],
                                [0, 0, 1]])
        turned_points = points.dot(move_matrix).dot(turn_matrix).dot(linalg.inv(move_matrix))

        # plotting turned figure
        plot_contour(turned_points[:, 0:2], ax)
        plt.title('Отражение фигуры относительно прямой')
        ax.legend(['Точка', 'Исходная фигура', 'Повернутая фигура'])
        plt.axis('equal')
        plt.show()
        print('Выберите действие: \n1 - изменить точку \n2 - перейти к четвертому пункту \n> ', end='')
        ch = int(input())
        if ch == 1:
            turning_point = np.array([[float(elem) for elem in input(f'Введите координаты точки: ').split(',')]])
        elif ch == 2:
            break

        print("__________________пункт четвёртый__________________")
        # input points
        points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]
                           for i in range(1, int(input('Введите количество точек: ')) + 1)])
        # plotting
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        plot3d_contour(points, ax)

        # transformation matrix
        xoy_mirror = bool(input('Отразить относительно плоскости XOY? (1 - Да / 0 - нет): '))
        xoz_mirror = bool(input('Отразить относительно плоскости XOZ? (1 - Да / 0 - нет): '))
        yoz_mirror = bool(input('Отразить относительно плоскости YOZ? (1 - Да / 0 - нет): '))
        T = np.array([[int(-1 if yoz_mirror else 1), 0, 0],
                      [0, int(-1 if xoz_mirror else 1), 0],
                      [0, 0, int(-1 if xoy_mirror else 1)]])
        points = np.dot(points, T)

        # plotting again
        plot3d_contour(points, ax)
        plt.title("Отражение фигуры")
        ax.legend(['Исходная фигура', 'Отраженная фигура'])
        plt.show()

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

    # print("__________________пункт шестой__________________")
    # while True:
    #     line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
    #                      for i in range(1, 3)])
    #     if line[0] == line[1]:
    #         print("Точки должны быть разными! Попробуйте ещё раз")
    #     else:
    #         break
    # points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')] + [1]
    #                    for i in range(1, int(input('Введите количество точек: ')) + 1)])
    # while True:
    #     # plotting original figure
    #     fig = plt.figure()
    #     ax = plt.axes(projection='3d')
    #     plot3d_contour(points[:, 0:3], ax)
    #
    #     # transformation matrices
    #     try:
    #         turn_value = -np.arctan((line[0][1] - line[1][1]) / (line[0][0] - line[1][0]))
    #     except:
    #         turn_value = -np.arctan(inf)
    #     move_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-line[0][0], -line[0][1], -line[0][2], 1]])

        # ЗДЕСЬ Я ЗАКОНЧИЛ РАБОАТЬ

        # turn_matrix = np.array([[np.cos(turn_value), np.sin(turn_value), 0],
        #                         [-np.sin(turn_value), np.cos(turn_value), 0],
        #                         [0, 0, 1]])
        # mirror_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        # mirrored_points = points.dot(move_matrix).dot(turn_matrix).dot(mirror_matrix). \
        #     dot(linalg.inv(turn_matrix)).dot(linalg.inv(move_matrix))
        #
        # # plotting mirrored figure
        # plot_contour(mirrored_points[:, 0:2], ax)
        # plt.title('Отражение фигуры относительно прямой')
        # ax.legend(['Линия', 'Исходная фигура', 'Отраженная фигура'])
        # plt.axis('equal')
        # plt.show()
        # print('Выберите действие: \n1 - изменить прямую \n2 - перейти к третьему пункту \n> ', end='')
        # ch = int(input())
        # if ch == 1:
        #     line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
        #                      for i in range(1, 3)])
        # elif ch == 2:
        #     break


if __name__ == "__main__":
    main()
