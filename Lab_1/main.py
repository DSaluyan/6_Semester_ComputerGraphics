import matplotlib.pyplot as plt
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


def plot3d_contour(points, ax, contour=True, **params):
    if params is None:
        params = {}
    x = [points[i][0] for i in range(0, len(points))]
    y = [points[i][1] for i in range(0, len(points))]
    z = [points[i][2] for i in range(0, len(points))]
    if contour:
        ax.plot3D([*x, points[0][0]],
                  [*y, points[0][1]],
                  [*z, points[0][2]],
                  **params)
    else:
        ax.plot3D(x, y, z, **params)


def main():
    print("__________________пункт пятый__________________")
    # input points
    points = [[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]
              for i in range(1, int(input('Введите количество точек: ')) + 1)]
    # plotting
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plot3d_contour(points, ax)

    # transformation matrix
    turn_x = radians(float(input('Введите угол поворота относительно оси Х в градусах: ')))
    turn_y = radians(float(input('Введите угол поворота относительно оси Y в градусах: ')))
    turn_z = radians(float(input('Введите угол поворота относительно оси Z в градусах: ')))
    turn_x_matrix = [[1, 0, 0],
                     [0, cos(turn_x), -sin(turn_x)],
                     [0, sin(turn_x), cos(turn_x)]]
    turn_y_matrix = [[cos(turn_y), 0, sin(turn_y)],
                     [0, 1, 0],
                     [-sin(turn_y), 0, cos(turn_y)]]
    turn_z_matrix = [[cos(turn_z), -sin(turn_z), 0],
                     [sin(turn_z), cos(turn_z), 0],
                     [0, 0, 1]]
    turned_points = my_dot(my_dot(my_dot(points, turn_x_matrix), turn_y_matrix), turn_z_matrix)
    max_coord = amax([points, turned_points])

    # plotting again
    plot3d_contour(turned_points, ax)
    plot3d_contour([[0, 0, 0], [max_coord, 0, 0]], ax, False)
    plot3d_contour([[0, 0, 0], [0, max_coord, 0]], ax, False)
    plot3d_contour([[0, 0, 0], [0, 0, max_coord]], ax, False)
    plt.title("Поворот фигуры")
    ax.legend(['Исходная фигура', 'Повёрнутая фигура', 'Ось X', 'Ось Y', 'Ось Z'])
    ax.set_xlim3d([-max_coord, max_coord])
    ax.set_ylim3d([-max_coord, max_coord])
    ax.set_zlim3d([-max_coord, max_coord])
    ax.set_box_aspect([1, 1, 1])
    plt.show()


if __name__ == "__main__":
    main()
