import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle

# --- Helper Functions for Drawing ---
# These functions make the code reusable and clean.

def draw_agent(ax, x, y, angle=0, width=1.0, height=0.5):
    """Draws a blue morphing envelope (ellipse) with a black direction arrow."""
    # The ellipse represents the morphing safety envelope
    ellipse = Ellipse(xy=(x, y), width=width, height=height, angle=angle, 
                      facecolor='royalblue', alpha=0.7, zorder=10)
    ax.add_patch(ellipse)
    
    # The arrow shows the intended direction of travel
    dx = 0.6 * np.cos(np.deg2rad(angle))
    dy = 0.6 * np.sin(np.deg2rad(angle))
    ax.arrow(x - dx/3, y - dy/3, dx*0.9, dy*0.9, 
             head_width=0.15, head_length=0.2, fc='black', ec='black', zorder=11)

def draw_static_obstacle(ax, x, y, size=10):
    """Draws a solid red dot representing a static obstacle."""
    ax.plot(x, y, 'o', color='red', markersize=size, zorder=5)

def draw_dynamic_obstacle(ax, x, y, angle):
    """Draws a solid red arrow representing a moving obstacle."""
    dx = 1.0 * np.cos(np.deg2rad(angle))
    dy = 1.0 * np.sin(np.deg2rad(angle))
    ax.arrow(x - dx/2, y - dy/2, dx, dy, 
             head_width=0.2, head_length=0.25, fc='red', ec='red', 
             length_includes_head=True, zorder=5)

def draw_non_connected(ax, x, y, angle):
    """Draws a grey rectangle with a black arrow for a non-connected vehicle."""
    # The grey rectangle represents the vehicle body
    rect = Rectangle(xy=(x - 0.5, y - 0.25), width=1.0, height=0.5, angle=angle, 
                     rotation_point='center', facecolor='grey', alpha=0.8, zorder=8)
    ax.add_patch(rect)
    
    # The arrow shows its direction
    dx = 0.6 * np.cos(np.deg2rad(angle))
    dy = 0.6 * np.sin(np.deg2rad(angle))
    ax.arrow(x - dx/3, y - dy/3, dx*0.9, dy*0.9, 
             head_width=0.15, head_length=0.2, fc='black', ec='black', zorder=9)


# --- Main Plotting Logic ---
# Create a 3x4 grid of subplots
fig, axes = plt.subplots(3, 4, figsize=(12, 9))

# --- Define Scenarios for each cell in the grid ---

# Column 1: Obstacle-Free (F1, F2, F3)
ax = axes[0, 0]; ax.set_title('F1') # Four-way stop
draw_agent(ax, 0, 1.5, -90); draw_agent(ax, 0, -1.5, 90)
draw_agent(ax, -1.5, 0, 0); draw_agent(ax, 1.5, 0, 180)

ax = axes[1, 0]; ax.set_title('F2') # Roundabout
draw_agent(ax, -1.5, 0, 20); draw_agent(ax, 1.5, 1, 160); draw_agent(ax, 0, -1.5, 90)

ax = axes[2, 0]; ax.set_title('F3') # Offset Intersection
draw_agent(ax, -1.5, 0.5, 0); draw_agent(ax, 1.5, -0.5, 180)

# Column 2: Static (S1, S2, S3)
ax = axes[0, 1]; ax.set_title('S1') # Narrow Gate
draw_agent(ax, -1.5, 0, 0, width=1.5, height=0.3)
draw_static_obstacle(ax, 0, 0.4); draw_static_obstacle(ax, 0, -0.4)

ax = axes[1, 1]; ax.set_title('S2') # Cluttered Field
draw_agent(ax, -1.5, 1, 0); draw_agent(ax, -1.5, -1, 0)
draw_static_obstacle(ax, 0, 0); draw_static_obstacle(ax, 0.5, 1.2)
draw_static_obstacle(ax, -0.3, -0.8); draw_static_obstacle(ax, 1, -0.5)

ax = axes[2, 1]; ax.set_title('S3') # Parking Lot Egress
draw_agent(ax, 0, 0, -90)
draw_static_obstacle(ax, -0.7, 0, size=20); draw_static_obstacle(ax, 0.7, 0, size=20)
draw_static_obstacle(ax, 0, -1.5, size=20)

# Column 3: Dynamic (D1, D2, D3)
ax = axes[0, 2]; ax.set_title('D1') # Lane Intrusion
draw_agent(ax, -1, 0, 0)
draw_dynamic_obstacle(ax, 0.8, 0.8, -135)

ax = axes[1, 2]; ax.set_title('D2') # Pedestrian Crossing
draw_agent(ax, -1.5, 0, 0)
draw_dynamic_obstacle(ax, 0.2, 1.5, -90)

ax = axes[2, 2]; ax.set_title('D3') # Highway Merge
draw_agent(ax, -1, -0.8, 20)
draw_dynamic_obstacle(ax, -1.5, 0.5, 0); draw_dynamic_obstacle(ax, 1.5, 0.5, 0)

# Column 4: Non-connected (N1, N2, N3)
ax = axes[0, 3]; ax.set_title('N1') # Aggressive Cut-off
draw_agent(ax, -1, 0, 0)
draw_non_connected(ax, 0.5, 0.4, -15)

ax = axes[1, 3]; ax.set_title('N2') # Sudden Braking
draw_agent(ax, 0, -0.8, 90)
draw_non_connected(ax, 0, 0.8, 90)

ax = axes[2, 3]; ax.set_title('N3') # Protocol Violation
draw_agent(ax, 0, 1.5, -90); draw_agent(ax, -1.5, 0, 0)
draw_non_connected(ax, 1.5, -1, 135)

# --- Final Formatting for all subplots ---
# Set titles for categories below each column
category_labels = ["(a) Obstacle-Free", "(b) Static", "(c) Dynamic", "(d) Non-connected"]
for i, ax in enumerate(axes[2, :]):
    ax.set_xlabel(category_labels[i], fontsize=14, labelpad=10)

# Clean up axes for a professional look
for ax in axes.flatten():
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Add the main title and final caption
fig.suptitle("Fig. 3. Simulated motion planning tasks.", fontsize=18, y=0.98)
fig.text(0.5, 0.02, 
         "Agents are depicted by blue morphing safety envelopes. Static obstacles are red dots, dynamic obstacles are red arrows,\nand non-connected vehicles are grey rectangles.", 
         ha='center', fontsize=12, style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 0.96]) # Adjust layout to make space for caption
plt.show()

# To save the figure for your paper:
# fig.savefig("figure3_scenarios.png", dpi=300, bbox_inches='tight')
# fig.savefig("figure3_scenarios.pdf", bbox_inches='tight')