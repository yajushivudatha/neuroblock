import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Import artists for creating the custom legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# --- 1. DATA GENERATION (Identical to before) ---

def generate_trajectories():
    """Generates all the necessary trajectory paths for the visualization."""
    time_steps = 15
    t = np.linspace(0, 14, time_steps)
    # EGO-AGENT (BLUE)
    ego_initial_x = np.linspace(10, 0, time_steps)
    ego_initial_y = np.linspace(10, 0, time_steps)
    ego_initial_path = np.vstack([ego_initial_x, ego_initial_y, t])
    ego_final_x = 10 * np.cos(np.linspace(np.pi/2, np.pi/4, time_steps))
    ego_final_y = 10 * np.sin(np.linspace(np.pi/2, np.pi/4, time_steps))
    ego_final_path = np.vstack([ego_final_x, ego_final_y, t])
    # OTHER AGENT (RED)
    start_t_idx = 5
    red_start_x = np.linspace(0, 5, start_t_idx)
    red_start_y = np.full(start_t_idx, 5)
    red_start_path = np.vstack([red_start_x, red_start_y, t[:start_t_idx]])
    # Modal Paths
    red_straight_x = np.linspace(5, 10, time_steps - start_t_idx)
    red_straight_y = np.full(time_steps - start_t_idx, 5)
    red_straight_path = np.vstack([red_straight_x, red_straight_y, t[start_t_idx:]])
    angle_left = np.linspace(0, np.pi/2, time_steps - start_t_idx)
    radius = 5
    red_left_x = 5 - radius * np.sin(angle_left)
    red_left_y = 5 + radius * (np.cos(angle_left) - 1)
    red_left_path = np.vstack([red_left_x, red_left_y, t[start_t_idx:]])
    angle_right = np.linspace(0, -np.pi/2, time_steps - start_t_idx)
    red_right_x = 5 + radius * np.sin(angle_right)
    red_right_y = 5 + radius * (1 - np.cos(angle_right))
    red_right_path = np.vstack([red_right_x, red_right_y, t[start_t_idx:]])

    return {
        "ego_initial": ego_initial_path, "ego_final": ego_final_path,
        "red_start": red_start_path, "red_straight": np.hstack([red_start_path, red_straight_path]),
        "red_left": np.hstack([red_start_path, red_left_path]),
        "red_right": np.hstack([red_start_path, red_right_path]),
    }

def plot_sphere_envelope(ax, center, radius, color):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=0.25, rstride=3, cstride=3, linewidth=0)

# --- 2. PLOTTING THE FIGURE ---

paths = generate_trajectories()

# Create a 1x4 subplot grid for a horizontal layout
fig, axes = plt.subplots(1, 4, figsize=(22, 6.5), subplot_kw={'projection': '3d'})
fig.suptitle('Adaptive Multi-Modal Trajectory Synthesis with Morphing Envelopes', fontsize=18, y=0.92)

# Common settings
view_angle = (25, -65)
axis_limits = {'x': (0, 11), 'y': (0, 11), 'z': (0, 15)}
titles = ["(a) Multi-Modal Prediction", "(b) Mode Adaptation", "(c) Trajectory Re-synthesis", "(d) Final Solution"]

# --- Panel (a) ---
ax = axes[0]
ax.scatter(*paths['ego_initial'], c='blue', s=60)
ax.scatter(*paths['red_straight'], c='red', s=40, alpha=0.3)
ax.scatter(*paths['red_left'], c='red', s=40, alpha=0.3)
ax.scatter(*paths['red_right'], c='red', s=40, alpha=0.3)
plot_sphere_envelope(ax, center=[4.5, 4.5, 7], radius=5, color='orange')

# --- Panel (b) ---
ax = axes[1]
ax.scatter(*paths['ego_initial'], c='blue', s=60)
ax.scatter(*paths['red_left'], c='red', s=60)
for i in range(paths['red_left'].shape[1]):
    plot_sphere_envelope(ax, center=paths['red_left'][:, i], radius=1.0, color='cyan')

# --- Panel (c) ---
ax = axes[2]
ax.scatter(*paths['ego_initial'], c='grey', s=40, alpha=0.5)
ax.scatter(*paths['ego_final'], c='blue', s=60)
ax.scatter(*paths['red_left'], c='red', s=60)

# --- Panel (d) ---
ax = axes[3]
ax.scatter(*paths['ego_final'], c='blue', s=60)
ax.scatter(*paths['red_left'], c='red', s=60)
for i in range(paths['red_left'].shape[1]):
    plot_sphere_envelope(ax, center=paths['red_left'][:, i], radius=1.0, color='cyan')
for i in range(paths['ego_final'].shape[1]):
    plot_sphere_envelope(ax, center=paths['ego_final'][:, i], radius=1.0, color='magenta')

# --- 3. STYLING AND LEGEND ---

def style_axis(ax, title, view, limits):
    """Applies consistent styling to a 3D axis."""
    ax.set_title(title, fontsize=14, y=0.98)
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_xlim(limits['x']); ax.set_ylim(limits['y']); ax.set_zlim(limits['z'])
    ax.set_xlabel(r'$\hat{x}$', fontsize=12); ax.set_ylabel(r'$\hat{y}$', fontsize=12); ax.set_zlabel(r'$\hat{t}$', fontsize=12)
    ax.set_xticklabels([]); ax.set_yticklabels([]); ax.set_zticklabels([])
    # Make panes and grid transparent for a cleaner look
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

for i, ax in enumerate(axes):
    style_axis(ax, titles[i], view_angle, axis_limits)
    
# Create custom legend artists (handles)
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Ego Agent Path', markerfacecolor='blue', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Other Agent Path', markerfacecolor='red', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Initial / Discarded Path', markerfacecolor='grey', markersize=12, alpha=0.7),
    Patch(facecolor='orange', alpha=0.4, edgecolor='k', label='Uncertainty Envelope'),
    Patch(facecolor='cyan', alpha=0.4, edgecolor='k', label='Morphed Safety Envelope')
]

# Add the legend to the figure, placed at the bottom center
# *** THIS IS THE MODIFIED LINE ***
fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=12, bbox_to_anchor=(0.5, 0.18))

# Adjust layout to make room for the suptitle and legend
fig.tight_layout(rect=[0, 0.1, 1, 0.9])

# Save the final, high-quality figure
plt.savefig("adaptive_synthesis_final.pdf", dpi=300)
plt.savefig("adaptive_synthesis_final.png", dpi=300, facecolor='white')

plt.show()