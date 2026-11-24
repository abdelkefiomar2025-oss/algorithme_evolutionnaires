import random

valeurs = [60, 100, 120, 80, 30, 90, 45, 70, 55, 40]
poids = [10, 20, 30, 15, 5, 25, 12, 18, 14, 8]
capacite = 70
n = len(valeurs)


def poids_total(sol):
    return sum(poids[i] for i in range(n) if sol[i])


def valeur_totale(sol):
    return sum(valeurs[i] for i in range(n) if sol[i])


def reparer(sol):
    while poids_total(sol) > capacite:
        pris = [i for i in range(n) if sol[i]]
        pire = min(pris, key=lambda i: valeurs[i] / poids[i])
        sol[pire] = 0
    return sol


def individu_aleatoire():
    sol = [random.randint(0, 1) for _ in range(n)]
    return reparer(sol)


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


def croisement(p1, p2):
    point = random.randint(1, n - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def mutation(sol, pm):
    for i in range(n):
        if random.random() < pm:
            sol[i] = 1 - sol[i]
    return sol


def algorithme_genetique(taille_pop=50, generations=100, pc=0.8, pm=0.05):
    population = [individu_aleatoire() for _ in range(taille_pop)]
    meilleur = max(population, key=valeur_totale)
    for g in range(generations):
        population.sort(key=valeur_totale, reverse=True)
        scores = [valeur_totale(s) for s in population]
        nouvelle = [population[0][:], population[1][:]]
        while len(nouvelle) < taille_pop:
            p1 = roulette(population, scores)
            p2 = roulette(population, scores)
            if random.random() < pc:
                e1, e2 = croisement(p1, p2)
            else:
                e1, e2 = p1[:], p2[:]
            nouvelle.append(reparer(mutation(e1, pm)))
            if len(nouvelle) < taille_pop:
                nouvelle.append(reparer(mutation(e2, pm)))
        population = nouvelle
        courant = max(population, key=valeur_totale)
        if valeur_totale(courant) > valeur_totale(meilleur):
            meilleur = courant[:]
        if g % 10 == 0:
            print("generation", g, "meilleure valeur", valeur_totale(meilleur))
    return meilleur


if __name__ == "__main__":
    sol = algorithme_genetique()
    print()
    print("objets choisis :", [i + 1 for i in range(n) if sol[i]])
    print("poids :", poids_total(sol), "/", capacite)
    print("valeur :", valeur_totale(sol))