import matplotlib.pyplot as plt
import numpy as np

# Data for the pie chart
labels = ['Conflict Search', 'Path Gen.', 'Envelope & Mode\nMgmt.']
sizes = [65, 20, 15]  # Percentages
times = [11.8, 3.6, 2.8] # Absolute times in ms
explode = (0.1, 0, 0)  # Explode the first slice ('Conflict Search')
colors = ['#4c72b0', '#dd8452', '#55a868'] # A professional, colorblind-friendly palette

# --- Create the custom labels with percentage and absolute time ---
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        # Find the corresponding absolute time
        time_val = 0
        for i, v in enumerate(values):
            if v == val:
                time_val = times[i]
                break
        return f'{pct:.1f}%\n({time_val:.1f} ms)'
    return my_autopct

# --- Plotting ---
fig, ax = plt.subplots(figsize=(8, 6))

wedges, texts, autotexts = ax.pie(
    sizes,
    explode=explode,
    labels=labels,
    colors=colors,
    autopct=make_autopct(sizes),
    startangle=90,
    shadow=False,
    pctdistance=0.75, # Position of the percentage text
    labeldistance=1.1, # Position of the component labels
    wedgeprops={'edgecolor': 'white'} # Add a white border to slices
)

# Style the text for better readability
plt.setp(autotexts, size=10, weight="bold", color="white")
plt.setp(texts, size=12)

# Set title and ensure the pie is a circle
ax.set_title("Fig. 6. Average computational breakdown for M-MTS (N=8, S1).",
             fontweight='bold', pad=20)
ax.axis('equal')

# Add the caption text below the plot (for context, you will use the caption in LaTeX)
caption_text = "The novel components of the framework constitute a small fraction of the overall computation."
fig.text(0.5, 0.05, caption_text, ha='center', style='italic', wrap=True)

plt.tight_layout(rect=[0, 0.1, 1, 1])

# --- Save the figure for your paper ---
# Saving as PDF is recommended for vector quality
plt.savefig("figure6_computation_breakdown.pdf", bbox_inches='tight')
plt.savefig("figure6_computation_breakdown.png", dpi=300, bbox_inches='tight')

plt.show()