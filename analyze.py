import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from algorithm import run_ga

def _ga(dist_matrix, n_cities, seed, **kw):
    return run_ga(dist_matrix, n_cities, seed=seed, verbose=False, **kw)

def conf_interval(data, conf=0.95):
    n = len(data)
    m = np.mean(data)
    se = np.std(data, ddof=1) / np.sqrt(n)
    h = se * stats.t.ppf((1 + conf) / 2., n - 1)
    return m, h

def param_tuning(dist_matrix, n_cities, out_dir):
    configs = [
        ("pop=100",   dict(pop_size=100, max_gens=500, inv_rate=0.05)),
        ("pop=200",   dict(pop_size=200, max_gens=500, inv_rate=0.05)),
        ("pop=400",   dict(pop_size=400, max_gens=500, inv_rate=0.05)),
        ("mut=0.02",  dict(pop_size=200, max_gens=500, inv_rate=0.02)),
        ("mut=0.15",  dict(pop_size=200, max_gens=500, inv_rate=0.15)),
    ]

    print("\n parameter tuning:")
    results = {}
    for label, cfg in configs:
        _, dist, hist, _ = _ga(dist_matrix, n_cities, seed=0, **cfg)
        results[label] = hist
        print(f"  {label}: {dist:.2f}")

    fig, ax = plt.subplots(figsize=(10, 5))
    for idx, (label, hist) in enumerate(results.items()):
        ax.plot(hist, label=label, color=plt.cm.tab10.colors[idx], linewidth=1.8)
    ax.set_title("Parameter Tuning – Convergence", fontsize=14, fontweight='bold')
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Tour Distance")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, 'parameter_tuning.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"saved: {path}")
    return results

def multi_run_stats(dist_matrix, n_cities, out_dir, n_runs=10,
                    pop_size=400, max_gens=2000,
                    inv_rate=0.03, elite=10, tourn_size=5):

    print("\n multi run statistics:")

    kw = dict(pop_size=pop_size, max_gens=max_gens, tourn_size=tourn_size,
              inv_rate=inv_rate, elite=elite)

    distances, histories = [], []
    for seed in range(n_runs):
        _, d, hist, _ = _ga(dist_matrix, n_cities, seed=seed, **kw)
        distances.append(d)
        histories.append(hist)
        print(f"  run {seed+1}/{n_runs}: {d:.2f}")

    mean, h = conf_interval(distances)
    std = np.std(distances)
    lo, hi = mean - h, mean + h
    best_run = int(np.argmin(distances))

    print(f"\n  mean: {mean:.2f}  std: {std:.2f}  95% CI: [{lo:.2f}, {hi:.2f}]")
    print(f"  best: {min(distances):.2f} (run {best_run+1})  worst: {max(distances):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for i, hist in enumerate(histories):
        ax1.plot(hist, color=plt.cm.tab10.colors[i % 10], linewidth=1.2, alpha=0.7,
                 label=f'run {i+1} ({distances[i]:.0f})')
    ax1.set_title('Convergence – All Runs', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Best Tour Distance')
    ax1.legend(fontsize=7, ncol=2)
    ax1.grid(True, alpha=0.3)

    colors = ['#e63946' if d == min(distances) else '#1a73e8' for d in distances]
    ax2.bar([f'R{i+1}' for i in range(n_runs)], distances, color=colors, alpha=0.8, edgecolor='white')
    ax2.axhline(mean,     color='black',  linewidth=2,   linestyle='--', label=f'mean: {mean:.2f}')
    ax2.axhline(mean+std, color='orange', linewidth=1.5, linestyle=':',  label='±1 std')
    ax2.axhline(mean-std, color='orange', linewidth=1.5, linestyle=':')
    ax2.axhline(hi,       color='green',  linewidth=1.5, linestyle='-',  label=f'95% CI: [{lo:.2f}, {hi:.2f}]')
    ax2.axhline(lo,       color='green',  linewidth=1.5, linestyle='-')
    ax2.set_title('Distance per Run (red = best)', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Run')
    ax2.set_ylabel('Best Tour Distance')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.suptitle(f'Multi Run  |  mean: {mean:.2f} ± {std:.2f}  |  95% CI: [{lo:.2f}, {hi:.2f}]',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(out_dir, 'multi_run_stats.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"saved: {path}")

    stats_path = os.path.join(out_dir, 'multi_run_stats.txt')
    with open(stats_path, 'w') as f:
        f.write(f"runs={n_runs}  pop={pop_size}  gens={max_gens}  mut={inv_rate}\n\n")
        f.write(f"mean: {mean:.2f}  std: {std:.2f}  95% CI: [{lo:.2f}, {hi:.2f}]\n")
        f.write(f"best: {min(distances):.2f} (run {best_run+1})  worst: {max(distances):.2f}\n\n")
        for i, d in enumerate(distances):
            f.write(f"  run {i+1:>2} (seed={i}): {d:.2f}\n")
    print(f"saved: {stats_path}")

    return distances, mean, std, lo, hi
