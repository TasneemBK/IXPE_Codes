
'''
#plot_pha.py
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

# Load the FITS file
filename = "ixpe03010101_det3_evt2_v01.pha"
hdul = fits.open(filename)
data = hdul[1].data

# Extract data
channel = data["CHANNEL"]
rate = data["RATE"]
error = data["STAT_ERR"]  # Use STAT_ERR if ERROR doesn't exist

# Plot as histogram-style line
plt.figure(figsize=(10, 6))
plt.plot(channel, rate, color='darkblue', linewidth=2, label='PHA Spectrum')
plt.fill_between(channel, rate - error, rate + error, color='lightblue', alpha=0.3)


# Labels and styling
plt.xlabel("PHA Channel", fontsize=14)
plt.ylabel("Count Rate (cts/s)", fontsize=14)
plt.title("IXPE PHA1 Spectrum", fontsize=16)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("pha_spectrum_step.png", dpi=300)
plt.show()

hdul.close()
'''

#pcube plot:
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from astropy.io import fits

# === Load FITS file ===
filename = "ixpe03010101_det3_evt2_v01_select_pcube.fits"
hdul = fits.open(filename)
data = hdul[1].data

# === Extract polarization values ===
PA = data['PA']          # in degrees
PA_ERR = data['PA_ERR']  # in degrees
PD = data['PD'] * 100    # convert to percent
PD_ERR = data['PD_ERR'] * 100

# === Define sector/wedge parameters (in degrees) ===
wedge_min = 0 # start angle (relative to 0° at 3 o'clock)
wedge_max = -60   # end angle

# === Setup polar plot with custom orientation ===
fig, ax = plt.subplots(
    subplot_kw={
        'projection': 'polar',
        'theta_offset': np.deg2rad(0),  # 0° at 3 o'clock (east)
        'theta_direction': -1            # clockwise angle increase
    },
    figsize=(8, 8)
)

# === Restrict to a sector ===
ax.set_thetamin(wedge_min)
ax.set_thetamax(wedge_max)

# === Plot each measurement ===
for i in range(len(PA)):
    if np.any(np.isnan([PA[i], PA_ERR[i], PD[i], PD_ERR[i]])):
        continue  # skip invalid values

    pa_rad = np.deg2rad(PA[i])
    pa_err_rad = np.deg2rad(PA_ERR[i])
    pd = PD[i]
    pd_err = PD_ERR[i]

    # Plot point
    ax.plot(pa_rad, pd, 'o', color='darkblue', markersize=5)

    # Plot uncertainty ellipse
    ellipse = Ellipse(
        (pa_rad, pd),
        width=2 * pa_err_rad,
        height=2 * pd_err,
        angle=0,
        facecolor='skyblue',
        edgecolor='navy',
        alpha=0.5
    )
    ax.add_patch(ellipse)

# === Format plot ===
ax.set_rlabel_position(wedge_max + 5)  # Place radial labels just outside the sector
ax.set_rlim(0, np.nanmax(PD + PD_ERR) + 2)
ax.set_title("IXPE Polarization (0° at East)\n(PA ± σ, PD ± σ)", fontsize=14, pad=20)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig("ixpe_polarization_sector.png", dpi=300, bbox_inches='tight')
plt.show()
hdul.close()








