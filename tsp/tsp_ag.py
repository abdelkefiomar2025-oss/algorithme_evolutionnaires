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


def longueur(tour, d):
    total = 0
    for i in range(len(tour)):
        total += d[tour[i]][tour[(i + 1) % len(tour)]]
    return total


def roulette(population, scores):
    total_scores = sum(scores)
    if total_scores == 0:
        return random.choice(population)
    seuil = random.uniform(0, total_scores)
    cumul = 0
    for individu, s in zip(population, scores):
        cumul += s
        if cumul >= seuil:
            return individu
    return population[-1]


def croisement_ox(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    enfant = [None] * n
    enfant[a:b + 1] = p1[a:b + 1]
    reste = [v for v in p2 if v not in enfant]
    k = 0
    for i in range(n):
        if enfant[i] is None:
            enfant[i] = reste[k]
            k += 1
    return enfant


def mutation(tour, pm):
    if random.random() < pm:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour


def algorithme_genetique(d, taille_pop=100, generations=300, pc=0.9, pm=0.2):
    n = len(d)
    population = []
    for _ in range(taille_pop):
        t = list(range(n))
        random.shuffle(t)
        population.append(t)
    meilleur = min(population, key=lambda t: longueur(t, d))

    for g in range(generations):
        population.sort(key=lambda t: longueur(t, d))
        scores = [1 / longueur(t, d) for t in population]
        nouvelle = [population[0][:], population[1][:]]
        while len(nouvelle) < taille_pop:
            p1 = roulette(population, scores)
            p2 = roulette(population, scores)
            if random.random() < pc:
                enfant = croisement_ox(p1, p2)
            else:
                enfant = p1[:]
            nouvelle.append(mutation(enfant, pm))
        population = nouvelle
        courant = min(population, key=lambda t: longueur(t, d))
        if longueur(courant, d) < longueur(meilleur, d):
            meilleur = courant[:]
        if g % 50 == 0:
            print("generation", g, "distance", round(longueur(meilleur, d), 2))
    return meilleur


if __name__ == "__main__":
    n = int(input("Nombre de villes : "))
    while n < 3:
        n = int(input("Il faut au moins 3 villes : "))
    villes = generer_villes(n)
    d = matrice_distances(villes)
    tour = algorithme_genetique(d)
    chemin = [v + 1 for v in tour] + [tour[0] + 1]
    print()
    print("meilleur circuit :", " -> ".join(map(str, chemin)))
    print("distance totale :", round(longueur(tour, d), 2))