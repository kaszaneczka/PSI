import random
import itertools


def generate(n):
    osobnik = ''
    lista = []
    for i in range(n):
        for j in range(8):
            osobnik += str(random.randint(0, 1))
        lista.append(osobnik)
        osobnik = ''
    return lista


def decode(bounds, n_bits, bitstring):
    decoded = list()
    largest = 2 ** n_bits
    for i in range(len(bounds)):
        chars = bitstring
        integer = int(chars, 2)
        value = bounds[i][0] + (integer / largest) * (bounds[i][1] - bounds[i][0])
        decoded.append(value)
    return decoded


def mutation(osobniki, pm):
    osobniki_pomutacji = []
    for osobnik in osobniki:
        wyznacznik = random.uniform(0, 1)
        if wyznacznik <= pm:
            gen = random.randint(0, 7)
            for i in range(len(osobnik)):
                if i == gen:
                    if osobnik[gen] == '0':
                        osobnik_new = osobnik[:gen] + '1' + osobnik[gen + 1:]
                        osobniki_pomutacji.append(osobnik_new)
                    else:
                        osobnik_new = osobnik[:gen] + '0' + osobnik[gen + 1:]
                        osobniki_pomutacji.append(osobnik_new)
        else:
            osobniki_pomutacji.append(osobnik)

    return osobniki_pomutacji


def crossing(osobniki, pm):
    osobniki_pokrzyzowaniu = []
    pomoc = []

    for i in range(0, len(osobniki), 2):
        poz = random.randint(1, 6)
        a = random.choice(osobniki)
        osobniki.remove(a)
        b = random.choice(osobniki)
        osobniki.remove(b)
        pomoc.append(a)
        pomoc.append(b)

        szansa_na_krzyzowanie = random.uniform(0, 1)
        if szansa_na_krzyzowanie < pm:
            osobnik_new0 = pomoc[0][:poz] + pomoc[1][poz:]
            osobnik_new1 = pomoc[1][:poz] + pomoc[0][poz:]
            osobniki_pokrzyzowaniu.append(osobnik_new0)
            osobniki_pokrzyzowaniu.append(osobnik_new1)
            pomoc = []

        else:
            osobniki_pokrzyzowaniu.append(pomoc[0])
            osobniki_pokrzyzowaniu.append(pomoc[1])
            pomoc = []

    return osobniki_pokrzyzowaniu


def fitness(osobniki):
    fitness = []
    for i in range(len(osobniki)):
        a = decode([[-5.0, 5.0]], 8, osobniki[i])[0]

        ocena = 10 * (a ** 2) + (50 * a) - 5
        fitness.append(ocena)
    fitness, osobniki = zip(*sorted(zip(fitness, osobniki), reverse=False))
    osobniki = list(osobniki)
    return osobniki


def select(osobniki, pm):
    usunac = round(len(osobniki) * pm)
    # print(usunac)
    osobniki_new = []
    for i in range(len(osobniki) - usunac):
        osobniki_new.append(osobniki[i])
    for j in range(usunac):
        new = osobniki[j]
        osobniki_new.append(new)

    return osobniki_new

gen = generate(20)
mut = mutation(gen, 0.2)
cros = crossing(mut, 0.8)
oc = fitness(cros)
selection = select(oc, 0.1)
print([decode([[-5.0, 5.0]],8,p) for p in selection])

licznik = 0
population = gen
for a in range(100):
    a = mutation(population, 0.2)
    b = crossing(a, 0.8)
    c = fitness(b)
    d = select(c, 0.1)
    population = d

print(population)
q = [decode([[-5.0, 5.0]],8,p) for p in population]
print(q)
wart = []
for a in q:
    wart.append(10 * (a[0]**2) + (50 *a[0]) - 5)
print(wart)