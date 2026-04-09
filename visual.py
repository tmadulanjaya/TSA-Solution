import os
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

def plot_convergence(hist_best, hist_avg, out_dir):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hist_best, label='best',    color='#1a73e8', linewidth=2)
    ax.plot(hist_avg,  label='average', color='#e8710a', linewidth=1.5, alpha=0.7)
    ax.set_title('GA Convergence', fontsize=14, fontweight='bold')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Tour Distance')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(out_dir, 'convergence.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved: {path}")

def plot_tour(route, dist, dist_matrix, city_names, out_dir):
    print("computing MDS layout...")
    coords = MDS(n_components=2, metric='precomputed', init='classical_mds',
                 random_state=42, n_init=1).fit_transform(dist_matrix)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_facecolor('#f0f4f8')

    n = len(route)
    for k in range(n):
        c1, c2 = route[k], route[(k+1) % n]
        ax.plot([coords[c1, 0], coords[c2, 0]],
                [coords[c1, 1], coords[c2, 1]],
                '-', color='#1a73e8', linewidth=0.8, alpha=0.6)

    ax.scatter(coords[:, 0], coords[:, 1], s=40, c='#e63946', zorder=3, label='cities')

    start = route[0]
    ax.scatter(coords[start, 0], coords[start, 1],
               s=200, c='gold', zorder=5, marker='*', label=f'start ({city_names[start]})')

    for i in range(0, len(city_names), 10):
        ax.annotate(city_names[route[i]],
                    (coords[route[i], 0], coords[route[i], 1]),
                    fontsize=6, alpha=0.7)

    ax.set_title(f'Best Tour – {len(city_names)} cities (MDS)\nDistance: {dist:.2f}',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper right')
    ax.axis('off')
    plt.tight_layout()
    path = os.path.join(out_dir, 'best_tour.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved: {path}")
