import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# --- Helper function to plot an ellipsoid (a) ---
def plot_ellipsoid(ax, center, radii, color):
    """Plots a 3D ellipsoid surface."""
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    
    x = center[0] + radii[0] * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radii[1] * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radii[2] * np.outer(np.ones_like(u), np.cos(v))
    
    ax.plot_surface(x, y, z, color=color, alpha=0.3, rstride=4, cstride=4, linewidth=0)

# --- Helper function to plot a tube around a path (b, d) ---
def plot_tube(ax, path_x, path_y, path_z, radius, color):
    """
    Plots a 3D tube surface around a given path.
    This is a simplified approach; a more complex one would use a mesh.
    """
    # Create points for the tube surface
    u = np.linspace(0, 2 * np.pi, 30) # Angle around the path
    
    # This is a 'hacky' but effective way to build the tube
    # It creates circles at each point along the path oriented perpendicular to the path
    for i in range(len(path_x) - 1):
        # Vector along the path
        v_path = np.array([path_x[i+1] - path_x[i],
                           path_y[i+1] - path_y[i],
                           path_z[i+1] - path_z[i]])
        v_path = v_path / np.linalg.norm(v_path)
        
        # Find two orthogonal vectors
        v_1 = np.cross(v_path, [0, 0, 1])
        if np.linalg.norm(v_1) < 1e-6:
             v_1 = np.cross(v_path, [0, 1, 0])
        v_1 = v_1 / np.linalg.norm(v_1)
        v_2 = np.cross(v_path, v_1)
        v_2 = v_2 / np.linalg.norm(v_2)
        
        # Generate circle points
        circle_x = path_x[i] + radius * (v_1[0] * np.cos(u) + v_2[0] * np.sin(u))
        circle_y = path_y[i] + radius * (v_1[1] * np.cos(u) + v_2[1] * np.sin(u))
        circle_z = path_z[i] + radius * (v_1[2] * np.cos(u) + v_2[2] * np.sin(u))
        
        # Plot this segment as a surface (we need 2 circles to make a segment)
        if i > 0:
            seg_x = np.array([prev_circle_x, circle_x])
            seg_y = np.array([prev_circle_y, circle_y])
            seg_z = np.array([prev_circle_z, circle_z])
            ax.plot_surface(seg_x, seg_y, seg_z, color=color, alpha=0.15, linewidth=0)

        prev_circle_x, prev_circle_y, prev_circle_z = circle_x, circle_y, circle_z


# --- 1. Define Colors ---
colors = {
    'ego_blue': '#0000FF',
    'other_red': '#FF0000',
    'discarded_gray': '#AAAAAA',
    'uncertainty_env': '#D2B48C', # Tan/Gold
    'morphed_env': '#AFEEEE',     # Pale turquoise
    'final_magenta': '#FF00FF'
}

# --- 2. Create Figure and 3D Axes ---
fig, axes = plt.subplots(1, 4, figsize=(20, 7), subplot_kw={'projection': '3d'})
plt.subplots_adjust(bottom=0.25, wspace=0.1) # Make room for legend

# --- 3. MOCK DATA: You MUST replace this with your own data ---
n_points = 20
t = np.linspace(0, 10, n_points)
alpha_fade = np.linspace(1, 0.1, n_points) # For fading paths

# (a) Multi-Modal Prediction Data
path_a_ego = np.array([t * 0.1, t * 0.8, t])
path_a_other1 = np.array([t * 0.8, t * 0.1, t])
path_a_other2 = np.array([t, t * 0.5, t * 0.8])
env_a_center = [5, 5, 6]
env_a_radii = [3, 3, 2]

# (b) Mode Adaptation Data
path_b_ego = np.array([t * 0.1, t * 0.8, t])
path_b_other = np.array([t * 0.8, t * 0.1, t])

# (c) Trajectory Re-synthesis Data
path_c_ego = np.array([t * 0.1, t * 0.8, t])
path_c_other = np.array([t * 0.8, t * 0.1, t])
path_c_discarded = np.array([t, t * 0.5, t * 0.8])

# (d) Final Solution Data
path_d_ego = np.array([t * 0.1, t * 0.8, t])
path_d_other = np.array([t * 0.8, t * 0.1, t])
# The "final" paths are slightly different, as shown in magenta
path_d_final_ego = np.array([t * 0.15, t * 0.75, t])
path_d_final_other = np.array([t * 0.75, t * 0.15, t])


# --- 4. Plot each subplot ---

# (a) Multi-Modal Prediction
ax = axes[0]
ax.set_title("(a) Multi-Modal Prediction", y=1.05)
ax.scatter(path_a_ego[0], path_a_ego[1], path_a_ego[2], c=colors['ego_blue'], s=50, alpha=alpha_fade, depthshade=False)
ax.scatter(path_a_other1[0], path_a_other1[1], path_a_other1[2], c=colors['other_red'], s=50, alpha=alpha_fade, depthshade=False)
ax.scatter(path_a_other2[0], path_a_other2[1], path_a_other2[2], c=colors['other_red'], s=50, alpha=alpha_fade, depthshade=False)
plot_ellipsoid(ax, env_a_center, env_a_radii, colors['uncertainty_env'])

# (b) Mode Adaptation
ax = axes[1]
ax.set_title("(b) Mode Adaptation", y=1.05)
ax.scatter(path_b_ego[0], path_b_ego[1], path_b_ego[2], c=colors['ego_blue'], s=50, alpha=1, depthshade=False)
ax.scatter(path_b_other[0], path_b_other[1], path_b_other[2], c=colors['other_red'], s=50, alpha=1, depthshade=False)
# Plot tubes around the paths
plot_tube(ax, path_b_ego[0], path_b_ego[1], path_b_ego[2], radius=1.0, color=colors['morphed_env'])
plot_tube(ax, path_b_other[0], path_b_other[1], path_b_other[2], radius=1.0, color=colors['morphed_env'])

# (c) Trajectory Re-synthesis
ax = axes[2]
ax.set_title("(c) Trajectory Re-synthesis", y=1.05)
ax.scatter(path_c_ego[0], path_c_ego[1], path_c_ego[2], c=colors['ego_blue'], s=50, alpha=1, depthshade=False)
ax.scatter(path_c_other[0], path_c_other[1], path_c_other[2], c=colors['other_red'], s=50, alpha=1, depthshade=False)
ax.scatter(path_c_discarded[0], path_c_discarded[1], path_c_discarded[2], c=colors['discarded_gray'], s=50, alpha=alpha_fade, depthshade=False)

# (d) Final Solution
ax = axes[3]
ax.set_title("(d) Final Solution", y=1.05)
# Plot the cyan "morphed" paths from (b)
ax.scatter(path_d_ego[0], path_d_ego[1], path_d_ego[2], c=colors['morphed_env'], s=150, alpha=0.4, depthshade=False)
ax.scatter(path_d_other[0], path_d_other[1], path_d_other[2], c=colors['morphed_env'], s=150, alpha=0.4, depthshade=False)
# Plot the final "chosen" paths over top
ax.scatter(path_d_final_ego[0], path_d_final_ego[1], path_d_final_ego[2], c=colors['final_magenta'], s=50, alpha=1, depthshade=False)
ax.scatter(path_d_final_other[0], path_d_final_other[1], path_d_final_other[2], c=colors['final_magenta'], s=50, alpha=1, depthshade=False)

# --- 5. Style all axes ---
for ax in axes.flat:
    ax.set_xlabel('$\hat{x}$', fontsize=12)
    ax.set_ylabel('$\hat{y}$', fontsize=12)
    ax.set_zlabel('$\hat{t}$', fontsize=12)
    
    # Set a consistent view angle
    ax.view_init(elev=20, azim=-60)
    
    # Set grid
    ax.grid(True, linestyle=':', alpha=0.7)
    
    # Set aspect ratio to be more cube-like
    ax.set_box_aspect([1, 1, 1])
    
    # Set consistent axis limits (YOU MUST CHANGE THIS TO FIT YOUR DATA)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 10)
    
    # Remove axis pane fill
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))


# --- 6. Create Custom Legend ---
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Ego Agent Path',
           markerfacecolor=colors['ego_blue'], markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Other Agent Path',
           markerfacecolor=colors['other_red'], markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Initial / Discarded Path',
           markerfacecolor=colors['discarded_gray'], markersize=12),
    Patch(facecolor=colors['uncertainty_env'], alpha=0.6, label='Uncertainty Envelope'),
    Patch(facecolor=colors['morphed_env'], alpha=0.6, label='Morphed Safety Envelope')
]

fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=5, fontsize=14, frameon=False)

# --- 7. Show Plot ---
plt.show()