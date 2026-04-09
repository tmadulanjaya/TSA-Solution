import os
import time
import argparse
import dataload
import algorithm
import analyze
import visual
import utils

def get_out_dir():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(path, exist_ok=True)
    return path

def main():
    parser = argparse.ArgumentParser(description="TSP solver using GA")
    parser.add_argument("--file",       type=str,   default=None)
    parser.add_argument("--pop",        type=int,   default=400)
    parser.add_argument("--gens",       type=int,   default=2000)
    parser.add_argument("--mut",        type=float, default=0.03)
    parser.add_argument("--elite",      type=int,   default=10)
    parser.add_argument("--tourn",      type=int,   default=5)
    parser.add_argument("--patience",   type=int,   default=300)
    parser.add_argument("--runs",       type=int,   default=10)
    args = parser.parse_args()

    csv_path = args.file or dataload.find_csv()
    if not csv_path:
        print("no CSV file found. use --file to specify one.")
        return 1

    out = get_out_dir()
    dist_matrix, city_names, n_cities, dist_np = dataload.load(csv_path)

    print(f"cities     : {n_cities}")
    print(f"population : {args.pop}")
    print(f"generations: {args.gens}")
    print(f"mutation   : {args.mut}")
    print(f"elitism    : {args.elite}")
    print(f"tournament : {args.tourn}")
    print(f"patience   : {args.patience}")
    print(f"stat runs  : {args.runs}")

    best_route, best_dist, hist_best, hist_avg = algorithm.run_ga(
        dist_matrix, n_cities,
        pop_size=args.pop, max_gens=args.gens,
        tourn_size=args.tourn, cx_rate=0.9,
        swap_rate=0.01, inv_rate=args.mut,
        elite=args.elite, seed=42,
        patience=args.patience, verbose=True,
    )

    print("\nrunning 2-opt...")
    improved_route, improved_dist = algorithm.two_opt(best_route, dist_matrix)
    print(f"2-opt: {best_dist:.2f} -> {improved_dist:.2f}")
    if improved_dist < best_dist:
        best_route, best_dist = improved_route, improved_dist
        utils.print_summary(best_route, best_dist, city_names, dist_matrix)

    opt_dist, gap = utils.check_optimal(best_route, dist_matrix, n_cities)
    if opt_dist:
        print(f"\noptimal: {opt_dist:.2f} | GA: {best_dist:.2f} | gap: {gap:.2f}%")

    RAND_ITERS = 5000
    print("\nrandom search comparison")
    _, rand_dist = algorithm.random_search(dist_matrix, n_cities, iters=RAND_ITERS)
    improvement = (rand_dist - best_dist) / rand_dist * 100
    print(f"random: {rand_dist:.2f} | GA: {best_dist:.2f} | improvement: {improvement:.1f}%")
    with open(os.path.join(out, "comparison_random.txt"), "w") as f:
        f.write(f"GA best: {best_dist:.2f}\nRandom best: {rand_dist:.2f}\n"
                f"Improvement: {improvement:.1f}%\nRandom iters: {RAND_ITERS}\n")

    utils.print_summary(best_route, best_dist, city_names, dist_matrix, opt_dist, gap)
    utils.save_solution(best_route, best_dist, city_names, dist_matrix, out, opt_dist, gap)
    visual.plot_convergence(hist_best, hist_avg, out)
    visual.plot_tour(best_route, best_dist, dist_np, city_names, out)
    analyze.param_tuning(dist_matrix, n_cities, out)
    analyze.multi_run_stats(
        dist_matrix, n_cities, out,
        n_runs=args.runs, pop_size=args.pop, max_gens=args.gens,
        inv_rate=args.mut, elite=args.elite, tourn_size=args.tourn,
    )

    print(f"\ndone. results in: {out}")
    return 0

if __name__ == "__main__":
    t = time.time()
    exit(main())
    print(f"total time: {time.time() - t:.2f}s")
