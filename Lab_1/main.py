import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg


def plot_contour(points, ax, params=None):
    if params is None:
        params = {}
    ax.plot(np.append(points[:, 0], [points[0, 0]]),
            np.append(points[:, 1], [points[0, 1]]),
            **params)


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
    x_mirror = bool(input('Отразить относительно оси X? (1 - Да/ 0 - нет)'))
    y_mirror = bool(input('Отразить относительно оси Y? (1 - Да/ 0 - нет)'))
    T = np.array([[scale*int(-1 if x_mirror else 1), 0], [0, scale*int(-1 if y_mirror else 1)]])
    points = np.dot(points, T)
    
    # plotting again
    plot_contour(points, ax)
    plt.title("Отражение фигуры")
    ax.legend(['Исходная фигура','Отраженная фигура'])
    plt.axis('equal')
    plt.show()
    
    print("__________________пункт второй__________________")
    line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
                       for i in range(1, 3)])
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]+[1]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    while(True):
        # plotting original figure
        fig, ax = plt.subplots()
        
        plot_contour(line, ax)
        plot_contour(points[:, 0:2], ax)

        # transformation matrixes
        try:
            turn_value = -np.arctan((line[0][1] - line[1][1])/(line[0][0] - line[1][0])) 
        except:
            turn_value = -np.arctan(inf)
        move_matrix = np.array([[1, 0, 0], [0, 1, 0], [-line[0][0], -line[0][1], 1]])
        turn_matrix = np.array([[np.cos(turn_value), np.sin(turn_value), 0],
                                [-np.sin(turn_value), np.cos(turn_value), 0],
                                [0, 0, 1]])
        mirror_matrix = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        mirrored_points = points.dot(move_matrix).dot(turn_matrix).dot(mirror_matrix).\
                                 dot(linalg.inv(turn_matrix)).dot(linalg.inv(move_matrix))
    
        # plotting mirrored figure
        plot_contour(mirrored_points[:,0:2], ax)
        plt.title('Отражение фигуры относительно прямой')
        ax.legend(['Линия', 'Исходная фигура','Отраженная фигура'])
        plt.axis('equal')
        plt.show()
        print('Выберите действие: \n1 - изменить прямую \n2 - перейти к третьему пункту \n> ', end='')
        ch = int(input());
        if ch == 1:
            line = np.array([[float(elem) for elem in input(f'Введите точку прямой {i}: ').split(',')]
                       for i in range(1, 3)])
        elif ch == 2:
            break

    print('__________________пункт третий__________________')
    turning_point = np.array([[float(elem) for elem in input(f'Введите координаты точки: ').split(',')]])
    points = np.array([[float(elem) for elem in input(f'Введите точку фигуры {i}: ').split(',')]+[1]
                       for i in range(1, int(input('Введите количество точек: ')) + 1)])
    turn_value = np.radians(float(input('Введите угол в градусах: ')))
    while(True):
        # plotting original figure
        fig, ax = plt.subplots()
        
        plot_contour(turning_point, ax)
        plot_contour(points[:, 0:2], ax)

        # transformation matrixes
        move_matrix = np.array([[1, 0, 0], [0, 1, 0], [-turning_point[0][0], -turning_point[0][1], 1]])
        turn_matrix = np.array([[np.cos(turn_value), np.sin(turn_value), 0],
                                [-np.sin(turn_value), np.cos(turn_value), 0],
                                [0, 0, 1]])
        turned_points = points.dot(move_matrix).dot(turn_matrix).dot(linalg.inv(move_matrix))
    
        # plotting turned figure
        plot_contour(turned_points[:,0:2], ax)
        plt.title('Отражение фигуры относительно прямой')
        ax.legend(['Точка', 'Исходная фигура','Повернутая фигура'])
        plt.axis('equal')
        plt.show()
        print('Выберите действие: \n1 - изменить точку \n2 - перейти к четвертому пункту \n> ', end='')
        ch = int(input());
        if ch == 1:
            turning_point = np.array([[float(elem) for elem in input(f'Введите координаты точки: ').split(',')]])
        elif ch == 2:
            break
        
if __name__ == "__main__":
    main()
    
