import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Enhancement #2: Env-based config
# -----------------------------
DATASET_PATH = os.environ.get("DATASET_PATH", "All_Diets.csv")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")

print("Nutrition analysis started...")
print(f"Using dataset: {DATASET_PATH}")
print(f"Saving outputs to: {OUTPUT_DIR}")

# Create output directory (Enhancement #1: persisted artifacts)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATASET_PATH)

nutrition_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']

# Handle missing data (fill missing values with mean)
df[nutrition_cols] = df[nutrition_cols].fillna(df[nutrition_cols].mean())

# Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[nutrition_cols].mean()

# Find the top 5 protein-rich recipes for each diet type
top_protein = (
    df.sort_values('Protein(g)', ascending=False)
      .groupby('Diet_type')
      .head(5)
      .sort_values(['Diet_type', 'Protein(g)'], ascending=[True, False])
)

# Add new metrics
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# -----------------------------
# Enhancement #1: Headless outputs (savefig instead of show)
# -----------------------------

# 1) Bar chart for average protein by diet type
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()

bar_path = os.path.join(OUTPUT_DIR, "avg_protein_by_diet.png")
plt.savefig(bar_path, dpi=200)
plt.close()

# 2) Heatmap for macronutrient content by diet type
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, fmt=".1f")
plt.title('Macronutrient Content by Diet Type')
plt.ylabel('Diet Type')
plt.xlabel('Macronutrients')
plt.tight_layout()

heatmap_path = os.path.join(OUTPUT_DIR, "macros_heatmap.png")
plt.savefig(heatmap_path, dpi=200)
plt.close()

# 3) Scatter plot for top 5 protein-rich recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_protein, x='Protein(g)', y='Recipe_name', hue='Cuisine_type')
plt.title('Top 5 Protein Rich Recipes Across Cuisines')
plt.ylabel('Recipe Name')
plt.xlabel('Protein(g)')
plt.legend(title='Cuisine', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save scatter plot
scatter_path = os.path.join(OUTPUT_DIR, "top5_protein_scatter.png")
plt.savefig(scatter_path, dpi=200)
plt.close()

# Console proof for screenshots
print("Nutrition analysis complete.")
print("Saved charts:")
print(f"- {bar_path}")
print(f"- {heatmap_path}")
print(f"- {scatter_path}")
print("\nAverage macros (preview):")
print(avg_macros.head())
