import os
from algorithm import calc_dist

def load_optimal(n_cities):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'optimal_solution.txt')
    if not os.path.exists(path):
        return None
    route = [int(x.strip()) for x in open(path) if x.strip()]
    if len(route) != n_cities:
        print(f"warning: optimal file has {len(route)} cities but expected {n_cities}")
        return None
    return route

def check_optimal(route, dist_matrix, n_cities):
    opt = load_optimal(n_cities)
    if not opt:
        return None, None
    opt_dist = calc_dist(opt, dist_matrix)
    gap = (calc_dist(route, dist_matrix) - opt_dist) / opt_dist * 100
    return opt_dist, gap

def save_solution(route, dist, city_names, dist_matrix, out_dir, opt_dist=None, gap=None):
    path = os.path.join(out_dir, 'solution.txt')
    names = [city_names[i] for i in route] + [city_names[route[0]]]

    with open(path, 'w') as f:
        f.write("TSP GA SOLUTION\n")
        f.write(f"total distance : {dist:.2f}\n")
        f.write(f"cities         : {len(route)}\n")
        if opt_dist is not None:
            f.write(f"optimal dist   : {opt_dist:.2f}\n")
            f.write(f"gap            : {gap:.2f}%\n")

        f.write("\nroute:\n")
        for i in range(0, len(names), 10):
            f.write(" -> ".join(names[i:i+10]) + "\n")

        f.write("\nsegment distances:\n")
        for i in range(len(route)):
            a, b = route[i], route[(i+1) % len(route)]
            f.write(f"  {city_names[a]} -> {city_names[b]}: {dist_matrix[a][b]:.2f}\n")

    print(f"saved: {path}")

def print_summary(route, dist, city_names, dist_matrix, opt_dist=None, gap=None):
    names = [city_names[i] for i in route]
    print(f"distance: {dist:.2f}  |  cities: {len(route)}")
    if opt_dist is not None:
        print(f"optimal : {opt_dist:.2f}  |  gap: {gap:.2f}%")
    print("route: " + " -> ".join(names[:10]) + " -> ... -> " + " -> ".join(names[-5:]))
    print("\nfirst 10 segments:")
    for i in range(10):
        a, b = route[i], route[(i+1) % len(route)]
        print(f"  {city_names[a]:>10} -> {city_names[b]:<10}  {dist_matrix[a][b]:.2f}")
    print(f"  ... ({len(route)} total)")
