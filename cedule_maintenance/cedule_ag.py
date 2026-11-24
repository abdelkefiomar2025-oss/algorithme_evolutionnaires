import random

capacites = [20, 15, 35, 40, 15, 15, 10]
demande = [80, 90, 65, 70]
options = [
    ["1100", "0110", "0011"],
    ["1100", "0110", "0011"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
    ["1000", "0100", "0010", "0001"],
]
total = sum(capacites)
nb_unites = len(capacites)
nb_intervalles = len(demande)


def reserves(chromosome):
    res = []
    for k in range(nb_intervalles):
        perdue = 0
        for u in range(nb_unites):
            if options[u][chromosome[u]][k] == "1":
                perdue += capacites[u]
        res.append(total - perdue - demande[k])
    return res


def adaptation(chromosome):
    return max(0, min(reserves(chromosome)))


def individu_aleatoire():
    return [random.randrange(len(options[u])) for u in range(nb_unites)]


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
    point = random.randint(1, nb_unites - 1)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def mutation(chromosome, pm):
    for u in range(nb_unites):
        if random.random() < pm:
            chromosome[u] = random.randrange(len(options[u]))
    return chromosome


def algorithme_genetique(taille_pop=40, generations=100, pc=0.8, pm=0.1):
    population = [individu_aleatoire() for _ in range(taille_pop)]
    meilleur = max(population, key=adaptation)
    for g in range(generations):
        population.sort(key=adaptation, reverse=True)
        scores = [adaptation(c) for c in population]
        nouvelle = [population[0][:], population[1][:]]
        while len(nouvelle) < taille_pop:
            p1 = roulette(population, scores)
            p2 = roulette(population, scores)
            if random.random() < pc:
                e1, e2 = croisement(p1, p2)
            else:
                e1, e2 = p1[:], p2[:]
            nouvelle.append(mutation(e1, pm))
            if len(nouvelle) < taille_pop:
                nouvelle.append(mutation(e2, pm))
        population = nouvelle
        courant = max(population, key=adaptation)
        if adaptation(courant) > adaptation(meilleur):
            meilleur = courant[:]
        if g % 10 == 0:
            print("generation", g, "meilleure reserve", adaptation(meilleur))
    return meilleur


if __name__ == "__main__":
    solution = algorithme_genetique()
    print()
    print("chromosome :", " ".join(options[u][solution[u]] for u in range(nb_unites)))
    print("reserves par intervalle :", reserves(solution))
    print("performance :", adaptation(solution))