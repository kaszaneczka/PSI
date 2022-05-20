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
import numpy as np

#random.seed(1235)

punkty = [[100, 100, 50]]


def city_generator():
    return [random.randint(-100, 100), random.randint(-100, 100), random.randint(0, 50)]

# def city_distance(x, y):
#     return ((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2 + (y[2] - x[2]) ** 2) ** (1 / 2)

def city_distance(pkt1, pkt2, asym=False):
    odleglosc_raw = (((pkt2[0] - pkt1[0]) ** 2 + (pkt2[1] - pkt1[1]) ** 2 + (pkt2[2] - pkt1[2]) ** 2) ** (1 / 2))

    if asym:
        if pkt1[2] == pkt2[2]:
            return odleglosc_raw
        else:
            if pkt1[2] < pkt2[2]:
                return odleglosc_raw * 0.9

            return odleglosc_raw * 1.1
    else:
        return odleglosc_raw

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

    visited.append(start)

    possible_next = list()
    for x in vertices:
        if x is not start and x not in visited:
            possible_next.append(x)

    #possible_next.append(visited[0])


    for x in possible_next:
        if polaczenia[vertices.index(start)][vertices.index(x)] == 1 and len(vertices) > len(visited):
            dfs_alghoritm(paths, vertices, x, polaczenia, list(visited))

    if len(vertices) == len(visited) and polaczenia[vertices.index(start)][vertices.index(visited[0])] == 1:
        visited.append(visited[0])
        dfs_alghoritm(paths, vertices, visited[len(visited) - 2], polaczenia, list(visited))

    if len(vertices) + 1 == len(visited):
        if visited not in paths:
            paths.append(visited)

    return visited


def bfs_alghoritm(vertices, start, polaczenia):

    visited = list()
    paths = list()
    queue = list()

    queue.append([start])

    while queue:  # queue = A ||| [[A,B], [A,C], [A,D]] ||| [[A,C], [A,D] [A,B,C], [A,B,D]]

        current_path = queue.pop(0)  # A | [A,B] | [A,C]
        s = current_path[len(current_path) - 1]  # A | B | C



        to_check = list()

        for x in vertices:
            if x is not s and x not in current_path and polaczenia[vertices.index(s)][vertices.index(x)] == 1 and len(vertices) > len(to_check):
                to_check.append(x)

        # if len(to_check) == 1 and polaczenia[vertices.index(s)][vertices.index(vertices[0])] == 1:
        #     to_check.append(vertices[0])
        #     print('asdasdasd')




        for x in to_check:  # to_check = B,C,D | to_check = C,D | to_check = B,D

            y = list(current_path)  # y = A || y = A,B
            y.append(x)  # y = A, B | y = A, C | y = A, D ||| y = A,B,C | y = A,B,D |||

            if len(y) is len(vertices) and y not in paths and polaczenia[vertices.index(y[-1])][0] == 1:
                y.append(y[0])
                paths.append(y)
            elif y not in queue:
                queue.append(y)  # queue jest puste wiec queue = [[A, B]] | queue = [[A,B], [A,C]] | queue = [[A,B], [A,C], [A,D]]

    return paths


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
        suma = [0,0]
        for x in range(len(drogi[y]) - 1):
            suma[0] = suma[0] + city_distance(drogi[y][x], drogi[y][x + 1])
            suma[1] =suma.append(city_distance(drogi[y][x], drogi[y][x + 1]))
        listaa.append(suma)
    return listaa


def wez_drugi_elem(elem):
    return elem[1]

def wez_czwarty_elem(elem):
    return elem[3]

def greedy_1(wierzcholki, wezel_aktualny,polaczenia):
    sciezki = list()
    odwiedzone = list()
    odwiedzone.append(wezel_aktualny)

    while len(sciezki) != 1:
        opcje = []
        for j, x in enumerate(wierzcholki):
            if x not in odwiedzone and polaczenia[wierzcholki.index(odwiedzone[-1])][wierzcholki.index(x)] == 1 :
                ff = city_distance(odwiedzone[-1], x)
                opcje.append([j, ff])

        xd = sorted(opcje, key=wez_drugi_elem)
        odwiedzone.append(wierzcholki[(xd[0][0])])

        if len(wierzcholki) == len(odwiedzone):
            odwiedzone.append(odwiedzone[0])
            sciezki.append(odwiedzone)

    return sciezki


def heurystyka(wierzcholki : list,odwiedzone: list,polaczenia: list,ost_elem: list)->list: # obrócona macierz połaczen?
    dist = []
    visited = odwiedzone
    #visited.append(ost_elem)

    #print(odwiedzone)
    for x in wierzcholki:
        if x not in visited:
            for y in wierzcholki:
                if y not in visited and polaczenia[wierzcholki.index(x)][wierzcholki.index(y)] == 1:
                    dist.append([city_distance(y, x),wierzcholki.index(x),wierzcholki.index(y) ])
        elif polaczenia[wierzcholki.index(ost_elem)][wierzcholki.index(x)] == 0:
            dist.append([10000000000000000000000000000.0,wierzcholki.index(x),wierzcholki.index(ost_elem)])
    for x in wierzcholki:
        if x not in visited and polaczenia[wierzcholki.index(ost_elem)][wierzcholki.index(x)] == 1:
            dist.append([city_distance(ost_elem, x), wierzcholki.index(x), wierzcholki.index(ost_elem)])
        elif polaczenia[wierzcholki.index(ost_elem)][wierzcholki.index(x)] == 0:
            dist.append([10000000000000000000000000000.0,wierzcholki.index(x),wierzcholki.index(ost_elem)])

    for x in wierzcholki:
        if x not in visited and polaczenia[wierzcholki.index(visited[0])][wierzcholki.index(x)] == 1:
            dist.append([city_distance(x,visited[0]), wierzcholki.index(visited[0]), wierzcholki.index(x)])
        elif polaczenia[wierzcholki.index(visited[0])][wierzcholki.index(x)] == 0:
            dist.append([10000000000000000000000000000.0,wierzcholki.index(visited[0]),wierzcholki.index(x)])

#FUNKCJA PEŁNYM PRZEBIEGOM DAJE HEURYSTYKE 10E28, TRZEBA TO ZMIENIC

    dist = sorted(dist)
    print(dist)

    return dist[0]


def a_gwiazdka(wierzcholki: list, wezel_aktualny: list, polaczenia: list, odwiedzone : list= None, rodzic : list = [], opcje : list = None)->list:

    if odwiedzone is None:
        odwiedzone = []
        opcje = []
        odwiedzone.append(wezel_aktualny)

    else:
        odwiedzone = []
        for i in rodzic:
            odwiedzone.append(wierzcholki[i])

    for j, x in enumerate(wierzcholki):
        if x not in odwiedzone and polaczenia[wierzcholki.index(odwiedzone[-1])][wierzcholki.index(x)] == 1 and odwiedzone[-1] != x:
            print('skad,dokad',wierzcholki.index(odwiedzone[-1]),wierzcholki.index(x))
            heurystyka1 = heurystyka(wierzcholki, odwiedzone, polaczenia,ost_elem = x)[0] * (len(wierzcholki)-(len(odwiedzone))) #tutaj inne  wejscia trzeba dac bo w odwiedzonych nie ma aktualnego x'sa!!!

            u = []
            for s in odwiedzone:
                u.append(wierzcholki.index(s))
            ff = 0
            u.append(j)

            print('odwiedzone',odwiedzone)
            print('u', u)

            for q in range(len(u)-1):
                print('odleglosc z',wierzcholki.index(wierzcholki[u[q]]),'do',wierzcholki.index(wierzcholki[u[q+1]]),'wynosi',city_distance(wierzcholki[u[q]],wierzcholki[u[q+1]]))
                ff += city_distance(wierzcholki[u[q]],wierzcholki[u[q+1]])

            opcje.append([u, ff,heurystyka1,ff+heurystyka1])

    # if len(odwiedzone) == len(wierzcholki):


    if len(odwiedzone) == len(wierzcholki):
        return 0

    opcje = sorted(opcje,key=wez_czwarty_elem)
    print('-++--+-+', opcje)
    rodzic = (opcje.pop(0))[0]

    print('----',odwiedzone,len(odwiedzone),len(wierzcholki))
    print('rodzic',rodzic)

    a_gwiazdka(wierzcholki, wierzcholki[rodzic[-1]], polaczenia, odwiedzone = odwiedzone,rodzic = rodzic,opcje = opcje)



# ----zalozmy przyklad z czterema miastami A,B,C,D----
# 1) tworzymy liste dostepnych opcji nastepnego przejscia tzn. B,C,D
# 2) nastepnie dla kazdej opcji obliczamy koszt wybrania tej opcji, ktory sklada sie z dwoch komponentow:
# dlugosc tej konkretnej trasy + heurystyka
# 3) tworzymy liste kosztow danych opcji i ja sortujemy po najnizszej wartosci
# 4) i teraz, dla wybranej opcji, zastepujemy ja dziecmi tej opcji:
# pierwotnie lista opcji wyglada tak [AB,AC,AD], potem, jezeli zalozmy wygrala opcja 'C', aktualizujemy te liste opcji
# i wyglada ona tak [AB,ACB,ACD,AD]
# 5) powtarzamy te procedure, az ktorys z elementow listy nie osiagnie pelnego rozmiaru

# ---obliczenia heurystyki---
# heurystyka bedzie obliczana w taki sposob, ze liczymy zaleznie od heurystyki min/srednia (przyjme min)
# z wszystkich dostepnych sciezek (takich, którymi moge jeszcze przejsc w przyszlosci) wybieram minimalna
# nastepnie mnoze wartosc tej trasy przez taka liczbe, ktora mowi ile jeszcze musze wykonac krokow aby dotrzec do celu
# i to jest wartosc heurystyki w danym stanie - jest to szacunek ile jeszcze kosztow poniesiemy do konca.

# ---uwagi---
# a) w przypadku kiedy nie ma polaczenia, ignorujemy przy wypisywaniu dzieci to znaczy, na tym poprzednim przykladzie:
# mamy 4 miasta, zaczynamy z A, mamy trzy opcje [AB,AC,AD], wygrywa AC, wiec powinno być [AB,ACB,ACD,AD], ale
# jak sie okazalo nie istnieje polaczenie podziedzy C, a D wiec faktycznie jest: [AB,ACB,AD]





if __name__ == '__main__':
    cities = list()
    for i in range(0,4):
        cities.append(city_generator())

    matrix = adjacency_matrix_generator(cities)

    all_pathes = list()
    g = macierz_połączeń(cities)
    print(cities)
    print(g[0])
    print(g[1])
    print(g[2])
    print(g[3])




    #greedy1 = greedy_1(cities,cities[0],g)
    #print('----greedy1-----', greedy1)
    # delete_percent(adjacency_matrix_generator(cities), 20)


    #print(koszt(all_pathes)[0][0])
    #print(koszt(greedy1)[0][0])

    #print(heurystyka(cities,[cities[0],cities[1]],g))



    # bfs = bfs_alghoritm(cities, cities[0], g)
    # print('----bfs-----',bfs)
    #




    # answer = dfs_alghoritm(all_pathes, cities, cities[0], g)
    # print('----dfs-----',all_pathes)
    #
    # for a in range(len(all_pathes)):
    #     all_pathes[a].pop(4)
    #     print(koszt(all_pathes)[a])
    #
    # g = np.array(g)
    # g = g.T
    # g = list(g)
    # print(g)
    #

    print('----',a_gwiazdka(cities,cities[0],g))
    answer = dfs_alghoritm(all_pathes, cities, cities[0], g)
    print('----dfs-----',all_pathes)

    for a in range(len(all_pathes)):
        all_pathes[a].pop(4)
        print(koszt(all_pathes)[a])
