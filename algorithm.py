import random
import time
import numpy as np
from operators import make_chromosome, select, crossover, swap_mut, inversion_mut

def calc_dist(route, dist_matrix):
    r = np.array(route)
    return float(np.sum(dist_matrix[r, np.roll(r, -1)]))


def run_ga(dist_matrix, n_cities,
           pop_size=400, max_gens=2000, tourn_size=5,
           cx_rate=0.9, swap_rate=0.01, inv_rate=0.03,
           elite=10, seed=42, patience=300, verbose=True):

    random.seed(seed)
    pop = [make_chromosome(n_cities) for _ in range(pop_size)]
    fits = [calc_dist(ind, dist_matrix) for ind in pop]

    best_idx = min(range(pop_size), key=lambda i: fits[i])
    best = pop[best_idx][:]
    best_dist = fits[best_idx]
    hist_best, hist_avg = [], []
    no_improve = 0

    if verbose:
        print(f"\n{'Gen':>6}  {'Best':>12}  {'Avg':>12}  {'Time':>7}")

    t0 = time.time()

    for gen in range(max_gens):
        ranked = sorted(range(pop_size), key=lambda i: fits[i])
        new_pop = [pop[k][:] for k in ranked[:elite]]  # keep elites

        while len(new_pop) < pop_size:
            p1 = select(pop, fits, tourn_size)
            p2 = select(pop, fits, tourn_size)
            child = crossover(p1, p2) if random.random() < cx_rate else p1[:]
            child = swap_mut(child, swap_rate)
            child = inversion_mut(child, inv_rate)
            new_pop.append(child)

        pop = new_pop
        fits = [calc_dist(ind, dist_matrix) for ind in pop]

        gen_best = min(range(pop_size), key=lambda i: fits[i])
        gen_best_dist = fits[gen_best]
        gen_avg = sum(fits) / pop_size
        hist_best.append(gen_best_dist)
        hist_avg.append(gen_avg)

        if gen_best_dist < best_dist:
            best_dist = gen_best_dist
            best = pop[gen_best][:]
            no_improve = 0
        else:
            no_improve += 1

        if verbose and (gen % 100 == 0 or gen == max_gens - 1):
            print(f"{gen:>6}  {gen_best_dist:>12.2f}  {gen_avg:>12.2f}  {time.time()-t0:>7.2f}")

        if no_improve >= patience:
            if verbose:
                print(f"stopping early at gen {gen}, no improvement in {patience} gens")
            break

    if verbose:
        print(f"done - best: {best_dist:.2f}, took {time.time()-t0:.1f}s")

    return best, best_dist, hist_best, hist_avg

def two_opt(route, dist_matrix):
    best = route[:]
    best_dist = calc_dist(best, dist_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 2, len(best)):
                candidate = best[:]
                candidate[i:j+1] = best[i:j+1][::-1]
                d = calc_dist(candidate, dist_matrix)
                if d < best_dist:
                    best, best_dist, improved = candidate, d, True
    return best, best_dist

def random_search(dist_matrix, n_cities, iters=5000):
    best_route, best_dist = None, float('inf')
    for i in range(iters):
        route = make_chromosome(n_cities)
        d = calc_dist(route, dist_matrix)
        if d < best_dist:
            best_route, best_dist = route, d
        if i % 1000 == 0 and i > 0:
            print(f"  random search {i}: {best_dist:.2f}")
    return best_route, best_dist
