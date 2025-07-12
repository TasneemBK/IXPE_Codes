import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = pd.read_csv('MAXI_lightcurve.csv')

column7 = data[data.columns[7]]  # 10–20 keV
column5 = data[data.columns[5]]  # 4–10 keV
column1 = data[data.columns[3]]  # 2–4 keV
column0 = data[data.columns[0]]  # MJD

# Calculate hardness ratios
hard1 = column5 / column1        # 4–10 keV / 2–4 keV
hard2 = column7 / column1        # 10–20 keV / 2–4 keV

# List of MJD values to mark with stars
mjds = [
    59714.63951, 59748.8626, 60066.95779, 60073.44307,
    60088.82082, 60108.95661, 60115.03936, 60412.0211,
    60593.22448, 60436.37372, 60456.04132, 60475.64771
]
fluorescent_colors = [
    'red', 'orange', 'deeppink', 'fuchsia', 'yellow', 'greenyellow',
    'lime', 'cyan', 'aqua', 'magenta', 'chartreuse', 'gold',
    'hotpink', 'tomato'
]

# Custom distinct non-blue/green/yellow colors
custom_colors = [
    'red', 'yellow', 'maroon', 'darkred', 'black',
    'dimgray', 'brown', 'indigo', 'darkorange',
    'crimson', 'firebrick', 'slategray'
]

# === Plot hardness-intensity diagram ===
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Hard1 vs Intensity
sc1 = ax[0].scatter(hard1, column1, c=column0, cmap = 'viridis',edgecolor='k', s=15 , alpha=0.4)
ax[0].set_xlabel('Hardness (4–10 keV / 2–4 keV)')
ax[0].set_ylabel('Intensity (2–4 keV)')
ax[0].set_title('Hard Color–Intensity Diagram (4–10 keV)')
plt.colorbar(sc1, ax=ax[0], label='MJD')

# Hard2 vs Intensity
sc2 = ax[1].scatter(hard2, column1, c=column0, cmap = 'plasma' ,edgecolor='k', s=15 , alpha=0.4)
ax[1].set_xlabel('Hardness (10–20 keV / 2–4 keV)')
ax[1].set_ylabel('Intensity (2–4 keV)')
ax[1].set_title('Hard Color–Intensity Diagram (10–20 keV)')
plt.colorbar(sc2, ax=ax[1], label='MJD')

# === Overlay stars at selected MJD values ===
for i, mjd_val in enumerate(mjds):
    idx = (np.abs(column0 - mjd_val)).idxmin()
    
    ax[0].scatter(hard1[idx], column1[idx], marker='*', s=200,
                  color=fluorescent_colors[i], edgecolor='black', linewidth=0.7, label=f'{mjd_val:.0f}')
    ax[1].scatter(hard2[idx], column1[idx], marker='*', s=200,
                  color=fluorescent_colors[i], edgecolor='black', linewidth=0.7)

# Optional: Legend for marked MJDs
ax[0].legend(title="Marked MJDs", fontsize=8, loc='best')

plt.tight_layout()
plt.savefig('hardness_color_intensity_plot_with_custom_stars_novir.png')
# plt.show()

#his is plotting in which i want to overlay the two plot.


















