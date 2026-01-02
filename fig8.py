import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import skewnorm

# --- 1. SIMULATE DATA TO MATCH THE PLOT ---
# We simulate 50 data points for each method, as mentioned in the table footnote.
# This data is carefully generated to match the peaks, spread, and
# percentiles (from your table) as closely as possible.
np.random.seed(42)
n_samples = 50

# M-MTS (Blue): Skewed right, median 1.95, 5th/95th: 0.81/3.54
# We use a right-skewed normal distribution.
mmts_data = skewnorm.rvs(a=5, loc=1.6, scale=0.9, size=n_samples)

# FE-CBF (Orange): Skewed right, median 1.22, 5th/95th: 0.45/2.81
fecbf_data = skewnorm.rvs(a=6, loc=0.8, scale=0.8, size=n_samples)

# STCS (Green): Bimodal, median 0.88, 5th/95th: 0.23/2.15
# We create a mix of two normal distributions to get the two-peak shape.
n1 = int(n_samples * 0.55) # 55% of data in the first peak
n2 = n_samples - n1      # 45% in the second peak
stcs_1 = np.random.normal(loc=0.35, scale=0.3, size=n1)
stcs_2 = np.random.normal(loc=1.4, scale=0.5, size=n2)
stcs_data = np.concatenate([stcs_1, stcs_2])

# Ensure all "clearance" data is non-negative
mmts_data = np.clip(mmts_data, 0, None)
fecbf_data = np.clip(fecbf_data, 0, None)
stcs_data = np.clip(stcs_data, 0, None)

# --- 2. FORMAT DATA FOR SEABORN ---
# Create a "long-form" DataFrame, which is the standard input for Seaborn.
data_mmts = pd.DataFrame({'Minimum Clearance (m)': mmts_data, 'Method': 'M-MTS'})
data_fecbf = pd.DataFrame({'Minimum Clearance (m)': fecbf_data, 'Method': 'FE-CBF'})
# Use "STCS" from the plot legend (not "SCS" from the table)
data_stcs = pd.DataFrame({'Minimum Clearance (m)': stcs_data, 'Method': 'STCS'})

df = pd.concat([data_mmts, data_fecbf, data_stcs])

# --- 3. SET UP AND CREATE THE PLOT ---
# Set the plot style to match the image (white grid, large fonts)
sns.set_theme(style="whitegrid")
sns.set_context("talk") # "talk" context increases font sizes to match

# Define the exact colors from the plot (standard seaborn "muted" palette)
palette = {
    "M-MTS": "#4878d0", 
    "FE-CBF": "#ee854a",
    "STCS": "#6acc64"
}

# Create the figure and axes
plt.figure(figsize=(14, 8))

# Create the Kernel Density Plot (KDE)
# This one function creates the layered, filled, and outlined distributions.
g = sns.kdeplot(
    data=df,
    x="Minimum Clearance (m)",
    hue="Method",             # Color by method
    hue_order=['M-MTS', 'FE-CBF', 'STCS'], # Control layering order
    palette=palette,
    multiple="layer",         # Layer them on top of each other
    fill=True,                # Fill the areas
    alpha=0.6,                # Set transparency
    linewidth=2.5,
    bw_adjust=0.9             # Adjust "smoothness" to match plot
)

# --- 4. CUSTOMIZE AXES, TICKS, AND LABELS ---
# Set X and Y axis labels
g.set_xlabel("Minimum Clearance (m)", fontsize=22)
g.set_ylabel("Probability Density", fontsize=22)

# Set axis limits to match the image
g.set_xlim(0, 4.5)
g.set_ylim(0, 0.7)

# Set axis ticks to match the image
g.set_xticks(np.arange(0, 4.51, 0.5))
g.set_yticks(np.arange(0, 0.71, 0.1))

# Customize tick label size
g.tick_params(axis='both', which='major', labelsize=18)

# --- 5. CUSTOMIZE THE LEGEND ---
legend = g.get_legend()
legend.set_title("Method")
plt.setp(legend.get_title(), fontsize='18')
plt.setp(legend.get_texts(), fontsize='18')

# --- 6. SHOW THE FINAL PLOT ---
plt.tight_layout() # Fits the plot neatly in the figure
plt.show()