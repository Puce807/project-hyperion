import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import config
from src.database import fetch_stars_batch

def hr_diagram(limit=5000, style="density"):
    fields = ["colour_index", "luminosity"]

    x = []
    y = []
    stars = fetch_stars_batch(fields=fields, limit=limit)
    x, y = np.array(list(zip(*stars)))

    if x.size == 0:
        print("No valid stellar data points found within filter bounds.")
        return

    x = np.array(x)
    y = np.array(y)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(9, 11), dpi=120)
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#121212')

    if style == "density":
        xy = np.vstack([x, np.log10(y)])
        z = gaussian_kde(xy)(xy)

        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        sc = ax.scatter(x, y, c=z, cmap='inferno', s=1.5, alpha=0.7, edgecolors='none')

        ax.set_yscale('log')
        ax.set_ylim(10 ** -5, 10 ** 5)
        ax.set_xlim(0.5, 3)

        ax.set_title("Hertzsprung-Russell Diagram", fontsize=16, fontweight='bold', pad=20, color='#66fcf1')
        ax.set_xlabel(r"Colour Index $(G_{BP} - G_{RP})$", fontsize=12, labelpad=10, color='#c5c6c7')
        ax.set_ylabel(r"Luminosity $(L / L_{\odot})$", fontsize=12, labelpad=10, color='#c5c6c7')

        ax.grid(True, which="both", ls=":", lw=0.5, color='#45f3ff', alpha=0.15)
        ax.tick_params(colors='#c5c6c7', labelsize=10)

        cbar = fig.colorbar(sc, ax=ax, pad=0.02, shrink=0.8)
        cbar.set_label('Relative Stellar Density', color='#c5c6c7', fontsize=10, labelpad=10)
        cbar.ax.tick_params(labelsize=8, colors='#c5c6c7')

        plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    hr_diagram(200000)