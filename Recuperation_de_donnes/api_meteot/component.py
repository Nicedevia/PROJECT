import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('datag/data_weth/historical_data.csv')

print(df.describe())
print(df.info())

sns.histplot(df['temp_c'], bins=20, kde=True)
plt.title('Distribution des Températures')
plt.xlabel('Température (°C)')
plt.ylabel('Fréquence')
plt.show()

# Corrn  precipitation vs visibilite
sns.scatterplot(x='precip_mm', y='vis_km', data=df)
plt.title('Précipitation vs Visibilité')
plt.xlabel('Précipitation (mm)')
plt.ylabel('Visibilité (km)')
plt.show()

