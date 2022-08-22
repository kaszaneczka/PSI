import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(555)
def city_generator():
    return [random.randint(-100, 100), random.randint(-100, 100), random.randint(0, 50)]

def city_distance(pkt1, pkt2, asym=False):
    raw_dist = (((pkt2[0] - pkt1[0]) ** 2 + (pkt2[1] - pkt1[1]) ** 2 + (pkt2[2] - pkt1[2]) ** 2) ** (1 / 2))

    if asym:
        if pkt1[2] == pkt2[2]:
            return raw_dist
        else:
            if pkt1[2] < pkt2[2]:
                return raw_dist * 0.9

            return raw_dist * 1.1
    else:
        return raw_dist

def koszt_sciezek(sciezki, miasta):
    lista_sum = list()
    for x in sciezki:
        koszt = 0
        for y in range(len(x) - 1):
            koszt += city_distance(miasta[x[y]],miasta[x[y + 1]]) #(miasta[x[y]],miasta[x[y + 1]])
        lista_sum.append(koszt)
    return lista_sum


def delete_percent(macierz, percent):
    count = int((len(macierz) * (len(macierz[0]) - 1)) * percent)
    i = 0
    while i < count:
        n = random.randint(0, len(macierz) - 1)
        m = random.randint(0, len(macierz) - 1)
        if macierz[n][m] == 1:
            macierz[n][m] = 0
            i = i + 1

def matrix(vertices_list, percent):
    adjacency_matrix = list()
    for i in vertices_list:
        matrix_row = list()
        for j in vertices_list:
            if i == j:
                matrix_row.append(0)
            else:
                matrix_row.append(1)
        adjacency_matrix.append(matrix_row)
    delete_percent(adjacency_matrix, (percent * 0.01))
    return adjacency_matrix

# def koszt(drogi):
#     listaa = list()
#     for y in range(len(drogi)):
#         suma = [0,0]
#         for x in range(len(drogi[y]) - 1):
#             suma[0] = suma[0] + city_distance(drogi[y][x], drogi[y][x + 1])
#             suma[1] =suma.append(city_distance(drogi[y][x], drogi[y][x + 1]))
#         listaa.append(suma)
#     return listaa

def wybor(opcje:list,feromony:list,aktualny:int):
    wybrane_feromony = []
    tablica_wyborow = []
    procenty = []

    for a in opcje:
        wybrane_feromony.append(feromony[aktualny][a])

    suma_feromonow = sum(wybrane_feromony)

    for a in wybrane_feromony:
        procenty.append(int(round((a/suma_feromonow)*100)))

    for a,b in enumerate(procenty):
        for i in range(b):
            tablica_wyborow.append(opcje[a])


    return random.choice(tablica_wyborow)


def ant(miasta: list,polaczenia:list,l_mrowek: int)->list:
    spis_miast = list()
    kk = 0
    for a in range(l_mrowek*len(miasta)):
        if a % l_mrowek == 0 and a != 0 :
            kk += 1
        spis_miast.append([kk])

    feromony = []
    for a in polaczenia:
        feromony1 = []
        for b in a:
            feromony1.append(0)
        feromony.append(feromony1)

    for k in range(len(miasta)-1):

        for a in spis_miast:
            opcje = []
            for j , x in enumerate(miasta):
                if j not in a and polaczenia[a[-1]][j] == 1:
                    opcje.append(j)


            if len(a) == 1 :
                a.append(random.choice(opcje))
                feromony[a[-2]][a[-1]] += (1/city_distance(miasta[a[-2]],miasta[a[-1]]))


            elif len(a) > 1:
                feromony[a[-2]][a[-1]] = feromony[a[-2]][a[-1]] * 0.8 # evaporate
                # print(opcje)

                try:
                    xx = wybor(opcje, feromony, a[-1])
                    # print('tutu',xx)
                    a.append(xx) # pass from city to city
                    feromony[a[-2]][a[-1]] += (1 / city_distance(miasta[a[-2]], miasta[a[-1]])) # putting new pheromone
                except:
                    pass

                if len(a) == len(miasta) and polaczenia[a[-1]][a[0]] == 1:
                    a.append(a[0])

    #
    # for y in spis_miast:
    #     if len(y) == 5:
    #         print('tutaj',y)




    return  spis_miast, feromony

    #na start spis_miast startuja z losowych miast
        # w danej iteracji spis_miast przechodza scieżke,
        # nastepnie dodajemy feromony ,
        # potam parowanie feromonow
        # i wracamy na poczatek

if __name__ == '__main__':
    cities = list()
    for i in range(0,4):
        cities.append(city_generator())

    all_pathes = list()
    g = matrix(cities,20)
    print(g)
    print(g[0])
    print(g[1])
    print(g[2])
    print(g[3])
    wyswietl, feromony =ant(cities,g,l_mrowek = 50)
    print('z maina :',wyswietl)

    koszty = koszt_sciezek(wyswietl, cities)

    poczatek = 0 # wybór miasta startowego
    minn = 0
    min_ind = 0
    for i, x in enumerate(koszty):
        if len(wyswietl[i]) == (len(cities)+1) and wyswietl[i][0] == poczatek :
            if minn == 0:
                minn = x
                min_ind = i
            else:
                if minn > x:
                    minn = x
                    min_ind = i
    print('the best :',minn, wyswietl[min_ind])


    #print('długosci :',koszt_sciezek(wyswietl, cities))

    for a in feromony:
        print(a)

