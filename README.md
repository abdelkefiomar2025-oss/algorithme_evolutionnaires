# Algorithmes évolutionnaires : AG et PSO

Implémentation en Python de l'algorithme génétique (AG) et de l'optimisation par essaim de particules (PSO) sur trois problèmes : le cédule de maintenance, le voyageur de commerce (TSP) et le sac à dos.

Aucune bibliothèque externe, Python 3 suffit.
## Les deux algorithmes

**Algorithme génétique (AG).** On garde une population de solutions. À chaque génération, on sélectionne les meilleurs parents (roulette), on les croise, on applique une petite mutation, et on conserve les 2 meilleurs individus (élitisme). La population s'améliore peu à peu.

**PSO.** Chaque particule est une solution qui se déplace dans l'espace de recherche. Sa vitesse dépend de son inertie, de sa meilleure position personnelle (pbest) et de la meilleure position de tout l'essaim (gbest). Les particules sont attirées vers les bonnes zones.

Paramètres PSO : w = 0.7, c1 = c2 = 1.5 (w = 0.8 et c1 = c2 = 2 pour le sac à dos).

## Les problèmes

### 1. Cédule de maintenance
Planifier la maintenance de 7 centrales (150 MW au total) sur 4 intervalles, en maximisant la plus petite réserve de puissance. Chaque centrale a un motif de maintenance en 4 bits (1100, 0110, 0011...).

- **AG** : le chromosome est la liste des motifs choisis. Croisement et mutation se font par bloc de 4 bits, pour ne jamais créer de cédule invalide.
- **PSO** : chaque position est arrondie vers un motif de maintenance.
- **Résultat** : réserve minimale de 25 MW avec les deux méthodes.

### 2. Voyageur de commerce (TSP)
Trouver le circuit le plus court qui passe une seule fois par chacune des n villes et revient au départ.

- **AG** : le chromosome est une permutation des villes. Croisement OX, mutation par échange de deux villes.
- **PSO** : codage par clés aléatoires, les positions sont triées pour obtenir une permutation.
- **Résultat** : dépend des villes générées. Les deux trouvent de bons circuits, mais sans garantie de l'optimum.

### 3. Sac à dos
Choisir des objets (valeur, poids) pour maximiser la valeur sans dépasser la capacité de 70.

- **AG** : chromosome binaire (1 = objet pris). Une solution trop lourde est réparée en retirant l'objet au pire rapport valeur/poids.
- **PSO** : version binaire avec fonction sigmoïde, même réparation.
- **Résultat** : valeur 355 avec les objets 1, 2, 4, 5, 7 et 10, pour les deux méthodes.

## Comparaison

| Critère | AG | PSO |
|---|---|---|
| Idée | Évolution (sélection, croisement, mutation) | Déplacement d'un essaim vers les meilleures positions |
| Adapté aux problèmes discrets | Très naturel (permutations, bits) | Demande un codage (arrondi, sigmoïde, clés aléatoires) |
| Paramètres | Taux de croisement, taux de mutation, taille de population | Inertie w, coefficients c1 et c2 |
| Cédule de maintenance | 25 MW | 25 MW |
| TSP | Bon, opérateurs adaptés aux permutations | Bon, mais le codage est indirect |
| Sac à dos | 355 | 355 |

**Conclusion.** Sur ces tailles de problèmes, les deux méthodes donnent des résultats très proches. L'AG est plus direct pour les problèmes combinatoires comme le TSP, car ses opérateurs travaillent directement sur les permutations. Le PSO est plus simple à écrire pour des variables continues, mais il demande une adaptation pour les problèmes discrets.