import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("Nutrition analysis started...")

df = pd.read_csv('All_Diets.csv')
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

# Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# Create output folder for charts
os.makedirs("outputs", exist_ok=True)

# Bar chart for average macronutrients
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/avg_protein_by_diet.png")
plt.show()
plt.close()

# Heatmap showing the relationship between macronutrients and diet types
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, fmt=".1f")
plt.title('Macronutrient Content by Diet Type')
plt.ylabel('Diet Type')
plt.xlabel('Macronutrients')
plt.tight_layout()
plt.savefig("outputs/macros_heatmap.png")
plt.show()
plt.close()

# Scatter plot to display the top 5 protein-rich recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(data=top_protein, x='Protein(g)', y='Recipe_name', hue='Cuisine_type')
plt.title('Top 5 Protein Rich Recipes Across Cuisines')
plt.ylabel('Recipe Name')
plt.xlabel('Protein(g)')
plt.legend(title='Cuisine', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("outputs/top5_protein_scatter.png")
plt.show()
plt.close()

print("Nutrition analysis complete.")
print("Saved charts to outputs/:")
print("- outputs/avg_protein_by_diet.png")
print("- outputs/macros_heatmap.png")
print("- outputs/top5_protein_scatter.png")

print("\nAverage macros (first few rows):")
print(avg_macros.head())

#Comment Code to test Pipeline V5