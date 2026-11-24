import math
import random


def generer_villes(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]


def matrice_distances(villes):
    n = len(villes)
    d = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            d[i][j] = math.dist(villes[i], villes[j])
    return d


def decoder(position):
    return sorted(range(len(position)), key=lambda i: position[i])


def longueur(tour, d):
    total = 0
    for i in range(len(tour)):
        total += d[tour[i]][tour[(i + 1) % len(tour)]]
    return total


def pso(d, nb_particules=60, iterations=400, w=0.7, c1=1.5, c2=1.5):
    n = len(d)
    positions = [[random.random() for _ in range(n)] for _ in range(nb_particules)]
    vitesses = [[0.0] * n for _ in range(nb_particules)]
    pbest = [p[:] for p in positions]
    pbest_val = [longueur(decoder(p), d) for p in positions]
    i_best = pbest_val.index(min(pbest_val))
    gbest = pbest[i_best][:]
    gbest_val = pbest_val[i_best]

    for it in range(iterations):
        for i in range(nb_particules):
            for k in range(n):
                r1, r2 = random.random(), random.random()
                vitesses[i][k] = (w * vitesses[i][k]
                                  + c1 * r1 * (pbest[i][k] - positions[i][k])
                                  + c2 * r2 * (gbest[k] - positions[i][k]))
                positions[i][k] += vitesses[i][k]
            val = longueur(decoder(positions[i]), d)
            if val < pbest_val[i]:
                pbest_val[i] = val
                pbest[i] = positions[i][:]
                if val < gbest_val:
                    gbest_val = val
                    gbest = positions[i][:]
        if it % 50 == 0:
            print("iteration", it, "distance", round(gbest_val, 2))
    return decoder(gbest), gbest_val


if __name__ == "__main__":
    n = int(input("Nombre de villes : "))
    while n < 3:
        n = int(input("Il faut au moins 3 villes : "))
    villes = generer_villes(n)
    d = matrice_distances(villes)
    tour, distance = pso(d)
    chemin = [v + 1 for v in tour] + [tour[0] + 1]
    print()
    print("meilleur circuit :", " -> ".join(map(str, chemin)))
    print("distance totale :", round(distance, 2))