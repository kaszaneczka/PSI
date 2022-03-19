"""
1. Genorowanie miast
2. Obliczanie dystansu pomiedzy miastami
3. Wizualizacja
4. Algorytm DFS
5. Algorytm BFS
1. X, Y, Z
  A B C D
A 0 2 1 3
B 5 0
C    0
D      0
"""
import random
import matplotlib.pyplot as plt

# random.seed(1235)

punkty = [[100, 100, 50]]


def city_generator():
    return [random.randint(-100, 100), random.randint(-100, 100), random.randint(0, 50)]


def city_distance(x, y):
    return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2)


def adjacency_matrix_generator(vertices_list):
    adjacency_matrix = list()
    for i in vertices_list:
        matrix_row = list()
        for j in vertices_list:
            if i == j:
                matrix_row.append(None)
            else:
                matrix_row.append(city_distance(i, j))
        adjacency_matrix.append(matrix_row)
    return adjacency_matrix


def macierz_połączeń(vertices_list):
    adjacency_matrix = list()
    for i in vertices_list:
        matrix_row = list()
        for j in vertices_list:
            if i == j:
                matrix_row.append(0)
            else:
                matrix_row.append(1)
        adjacency_matrix.append(matrix_row)
    delete_percent(adjacency_matrix, 0.2)
    return adjacency_matrix


def visualize_cities(vertices_list, path=None):
    xs, ys, zs = zip(*vertices_list)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs, ys, zs)

    if path is not None:
        for i in range(len(path) - 1):
            plt.plot([path[i][0], path[i + 1][0]],
                     [path[i][1], path[i + 1][1]],
                     [path[i][2], path[i + 1][2]])

    plt.show()


def show_graph_3d_plot(vertices_list, edges=None, path=None):
    xs, ys, zs = zip(*vertices_list)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection='3d')

    ax.scatter(xs, ys, zs, s=100)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if edges and path is None:
        already_connected = list()
        for a in edges:
            for b in edges:
                if a != b and (a, b) not in already_connected:
                    plt.plot([a[0], b[0]],
                             [a[1], b[1]],
                             [a[2], b[2]])
                    already_connected.append((a, b))
                    already_connected.append((b, a))
    elif path is not None:
        for i in range(len(path) - 1):
            plt.plot([path[i][0], path[i + 1][0]],
                     [path[i][1], path[i + 1][1]],
                     [path[i][2], path[i + 1][2]])
        pass

    plt.show()


def dfs_alghoritm(paths, vertices, start, polaczenia=None, visited=None):
    if visited is None:
        visited = list()
    # print("node ", start)
    if start not in visited:
        visited.append(start)

        possible_next = list()
        for x in vertices:
            if x is not start and x not in visited:
                possible_next.append(x)

        for j, x in enumerate(possible_next):
            if polaczenia[vertices.index(start)][j] == 1:
                dfs_alghoritm(paths, vertices, x, polaczenia, list(visited))

    if len(vertices) == len(visited):
        if visited not in paths:
            paths.append(visited)
    return visited


def bfs_alghoritm(paths, vertices, start, visited=None):
    if visited is None:
        visited = list()
    # print("node ", start)
    if start not in visited:
        visited.append(start)

        possible_next = list()
        for x in vertices:
            if x is not start and x not in visited:
                possible_next.append(x)
        visited.append(possible_next)
        print(visited)

        for x in possible_next:
            bfs_alghoritm(paths, vertices, x, list(visited))

    if len(vertices) == len(visited):
        if visited not in paths:
            paths.append(visited)
    return visited


def delete_percent(macierz, percent):
    count = int((len(macierz) * (len(macierz[0]) - 1)) * percent)
    i = 0
    while i < count:
        n = random.randint(0, len(macierz) - 1)
        m = random.randint(0, len(macierz) - 1)
        if macierz[n][m] == 1:
            macierz[n][m] = 0
            i = i + 1


def koszt(drogi):
    listaa = list()
    for y in range(len(drogi)):
        suma = 0
        for x in range(len(drogi[y]) - 1):
            suma = suma + city_distance(drogi[y][x], drogi[y][x + 1])
        listaa.append(suma)
    print(listaa)


if __name__ == '__main__':
    cities = list()
    for i in range(0, 3):
        cities.append(city_generator())

    matrix = adjacency_matrix_generator(cities)

    all_pathes = list()
    print('------ \n', macierz_połączeń(cities))
    answer = dfs_alghoritm(all_pathes, cities, cities[0], macierz_połączeń(cities))
    # delete_percent(adjacency_matrix_generator(cities), 20)
    koszt(all_pathes)
    print('nic')
    print('nic')
    print('nic')
    # show_graph_3d_plot(cities, cities)
