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


def decoder(position):
    choix = []
    for u in range(nb_unites):
        i = int(position[u])
        i = max(0, min(i, len(options[u]) - 1))
        choix.append(i)
    return choix


def reserves(choix):
    res = []
    for k in range(nb_intervalles):
        perdue = 0
        for u in range(nb_unites):
            if options[u][choix[u]][k] == "1":
                perdue += capacites[u]
        res.append(total - perdue - demande[k])
    return res


def adaptation(position):
    return max(0, min(reserves(decoder(position))))


def pso(nb_particules=30, iterations=100, w=0.7, c1=1.5, c2=1.5):
    bornes = [len(options[u]) - 0.001 for u in range(nb_unites)]
    positions = [[random.uniform(0, bornes[u]) for u in range(nb_unites)] for _ in range(nb_particules)]
    vitesses = [[0.0] * nb_unites for _ in range(nb_particules)]
    pbest = [p[:] for p in positions]
    pbest_val = [adaptation(p) for p in positions]
    i_best = pbest_val.index(max(pbest_val))
    gbest = pbest[i_best][:]
    gbest_val = pbest_val[i_best]

    for it in range(iterations):
        for i in range(nb_particules):
            for d in range(nb_unites):
                r1, r2 = random.random(), random.random()
                vitesses[i][d] = (w * vitesses[i][d]
                                  + c1 * r1 * (pbest[i][d] - positions[i][d])
                                  + c2 * r2 * (gbest[d] - positions[i][d]))
                positions[i][d] += vitesses[i][d]
                positions[i][d] = max(0, min(positions[i][d], bornes[d]))
            val = adaptation(positions[i])
            if val > pbest_val[i]:
                pbest_val[i] = val
                pbest[i] = positions[i][:]
                if val > gbest_val:
                    gbest_val = val
                    gbest = positions[i][:]
        if it % 10 == 0:
            print("iteration", it, "meilleure reserve", gbest_val)
    return gbest, gbest_val


if __name__ == "__main__":
    meilleure, valeur = pso()
    choix = decoder(meilleure)
    print()
    print("planning :", " ".join(options[u][choix[u]] for u in range(nb_unites)))
    print("reserves par intervalle :", reserves(choix))
    print("performance :", valeur)