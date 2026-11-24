import math
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


def sigmoide(x):
    x = max(-30, min(30, x))
    return 1 / (1 + math.exp(-x))


def pso_binaire(nb_particules=30, iterations=100, w=0.8, c1=2.0, c2=2.0, vmax=4.0):
    positions = [reparer([random.randint(0, 1) for _ in range(n)]) for _ in range(nb_particules)]
    vitesses = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(nb_particules)]
    pbest = [p[:] for p in positions]
    pbest_val = [valeur_totale(p) for p in positions]
    i_best = pbest_val.index(max(pbest_val))
    gbest = pbest[i_best][:]
    gbest_val = pbest_val[i_best]

    for it in range(iterations):
        for i in range(nb_particules):
            for d in range(n):
                r1, r2 = random.random(), random.random()
                v = (w * vitesses[i][d]
                     + c1 * r1 * (pbest[i][d] - positions[i][d])
                     + c2 * r2 * (gbest[d] - positions[i][d]))
                vitesses[i][d] = max(-vmax, min(vmax, v))
                positions[i][d] = 1 if random.random() < sigmoide(vitesses[i][d]) else 0
            positions[i] = reparer(positions[i])
            val = valeur_totale(positions[i])
            if val > pbest_val[i]:
                pbest_val[i] = val
                pbest[i] = positions[i][:]
                if val > gbest_val:
                    gbest_val = val
                    gbest = positions[i][:]
        if it % 10 == 0:
            print("iteration", it, "meilleure valeur", gbest_val)
    return gbest


if __name__ == "__main__":
    sol = pso_binaire()
    print()
    print("objets choisis :", [i + 1 for i in range(n) if sol[i]])
    print("poids :", poids_total(sol), "/", capacite)
    print("valeur :", valeur_totale(sol))