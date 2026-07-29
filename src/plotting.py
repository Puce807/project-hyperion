import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import config
from src.database import fetch_stars_batch
from matplotlib.patches import Rectangle

def plot_hr_diagram(limit=5000, style="density", filepath="", annotations=False):
    fields = ["colour_index", "luminosity"]
    # TODO: Add an option to create a "processed" diagram that looks more clear and aesthetic. Reduce error, remove outliers, add giants, add white dwarfs

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
    fig, ax = plt.subplots(figsize=(7, 11), dpi=120)
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#121212')

    ax.set_yscale('log')
    ax.set_ylim(10 ** -5, 10 ** 5)
    ax.set_xlim(-0.5, 3.25)

    class_axis_letters = ["O", "B", "A", "F", "G", "K", "M"]
    class_axis_values = [-0.4, -0.15, 0.15, 0.45, 0.82, 1.25, 2.3]
    secax = ax.secondary_xaxis("top")
    secax.set_ticks(class_axis_values)
    secax.set_xticklabels(class_axis_letters)
    secax.set_xlabel("Spectral Class")

    ax.set_title("Gaia Hertzsprung-Russell Diagram", fontsize=16, fontweight='bold', pad=20, color='#66fcf1')
    ax.set_xlabel(r"Colour Index $(G_{BP} - G_{RP})$", fontsize=12, labelpad=10, color='#c5c6c7')
    ax.set_ylabel(r"Luminosity $(L / L_{\odot})$", fontsize=12, labelpad=10, color='#c5c6c7')

    ax.grid(True, which="both", ls=":", lw=0.5, color='#45f3ff', alpha=0.15)
    ax.tick_params(colors='#c5c6c7', labelsize=10)

    if style == "density":
        xy = np.vstack([x, np.log10(y)])
        z = gaussian_kde(xy)(xy)

        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        sc = ax.scatter(x, y, c=z, cmap='inferno', s=1.5, alpha=0.7, edgecolors='none')

        cbar = fig.colorbar(sc, ax=ax, pad=0.02, shrink=0.8)
        cbar.set_label('Relative Stellar Density', color='#c5c6c7', fontsize=10, labelpad=10)
        cbar.ax.tick_params(labelsize=8, colors='#c5c6c7')

    if style == "colour":
        sc = ax.scatter(x, y, s=1, c=x, cmap='RdYlBu_r', vmin=-0.5, vmax=2.25, alpha=0.7)

        cbar = fig.colorbar(sc, ax=ax, pad=0.02, shrink=0.8)
        cbar.set_label('Colour Index', color='#c5c6c7', fontsize=10, labelpad=10)
        cbar.ax.tick_params(labelsize=8, colors='#c5c6c7')

    if annotations:
        log_y = np.log10(y)
        # Main Sequence
        blue_zone = (x >= 0.0) & (x < 1.0) & (log_y >= -1.5) & (log_y <= 3.0)
        red_zone = (x >= 1.0) & (x <= 3.2) & (log_y >= -3.5) & (log_y <= 0.5)
        ms_mask = blue_zone | red_zone
        ms_x = x[ms_mask]
        ms_y = y[ms_mask]

        coefficients = np.polyfit(ms_x, np.log10(ms_y), deg=3)
        poly_func = np.poly1d(coefficients)
        x_smooth = np.linspace(np.min(ms_x), np.max(ms_x), 200)
        log_y_fit = poly_func(x_smooth)
        y_fit = 10 ** log_y_fit
        plt.plot(x_smooth, y_fit, color="red", linewidth=1, linestyle="--")

        text_x = x_smooth[100]
        text_y = y_fit[100]
        plt.text(text_x, text_y, "Main Sequence")

        # White Dwarfs
        ms_mask = (x >= -0.5) & (x < 0.8) & (log_y >= -5) & (log_y <= -2)
        ms_x = x[ms_mask]
        ms_y = y[ms_mask]

        coefficients = np.polyfit(ms_x, np.log10(ms_y), deg=2)
        poly_func = np.poly1d(coefficients)
        x_smooth = np.linspace(np.min(ms_x), np.max(ms_x), 200)
        log_y_fit = poly_func(x_smooth)
        y_fit = 10 ** log_y_fit
        plt.plot(x_smooth, y_fit, color="red", linewidth=1, linestyle="--")

        text_x = x_smooth[100]
        text_y = y_fit[100]
        plt.text(text_x, text_y, "White Dwarfs")

        # Giants
        ms_mask = (x >= 1.0) & (x <= 2.8) & (log_y >= 1.0) & (log_y <= 2.8)
        ms_x = x[ms_mask]
        ms_y = y[ms_mask]

        coefficients = np.polyfit(ms_x, np.log10(ms_y), deg=2)
        poly_func = np.poly1d(coefficients)
        x_smooth = np.linspace(np.min(ms_x), np.max(ms_x), 200)
        log_y_fit = poly_func(x_smooth)
        y_fit = 10 ** log_y_fit
        plt.plot(x_smooth, y_fit, color="red", linewidth=1, linestyle="--")

        text_x = x_smooth[100]
        text_y = y_fit[100]
        plt.text(text_x, text_y, "Giants")


    if filepath:
        plt.savefig(filepath, dpi=300, transparent=True, bbox_inches='tight')

    plt.tight_layout()
    plt.show()


