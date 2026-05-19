import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import os

#charger les données 
base_path = os.path.join(os.path.dirname(__file__), ".")

df_freq = pd.read_csv(os.path.join(base_path, "frequentation-gares-clean.csv"), sep=';')

df_prop_22 = pd.read_csv(os.path.join(base_path, "proprete-en-gare-22-clean.csv"), sep=';')
df_prop_23 = pd.read_csv(os.path.join(base_path, "proprete-en-gare-23-clean.csv"), sep=';')
df_prop_24 = pd.read_csv(os.path.join(base_path, "proprete-en-gare-24-clean.csv"), sep=';')

#préparer les données 

df_prop_22["Année"] = 2022
df_prop_23["Année"] = 2023
df_prop_24["Année"] = 2024

df_prop = pd.concat([df_prop_22, df_prop_23, df_prop_24])

df_freq = df_freq.rename(columns={ #on renomme pour harmoniser les noms
    "Code UIC": "UIC",
    "Nom de la gare": "Nom gare"
})

df_freq["Département"] = df_freq["Code postal"].astype(str).str[:2] #création du département à partir du code postal 

df = df_freq.merge(df_prop, on=["UIC", "Nom gare"])

def get_freq(row):
    return pd.to_numeric(row[f"Total Voyageurs {int(row['Année'])}"], errors='coerce')

df["Frequentation"] = df.apply(get_freq, axis=1)
initial = len(df)
df = df.dropna(subset=["Frequentation", "Taux de conformité moyen"])
print(f"Avant nettoyage : {len(df)} lignes")
print(f"Après dropna : {len(df)} lignes ({(1 - len(df)/initial)*100:.1f}% perte)")

#etudier la corrélation par année 

print("\n-corrélation par année -\n")

for annee in [2022, 2023, 2024]:
    df_an = df[df["Année"] == annee]
    n = len(df_an)

    r, p_pearson = stats.pearsonr(df_an["Frequentation"], df_an["Taux de conformité moyen"]) #corrélation de Pearson
    rho, p_spearman = stats.spearmanr(df_an["Frequentation"], df_an["Taux de conformité moyen"]) #corrélation de Spearman

    print(f"Année {annee} (N={n})")
    print(f"  Pearson  r   = {r:.4f}  (p = {p_pearson:.4f}) {'significatif' if p_pearson < 0.05 else 'non significatif'}")
    print(f"  Spearman rho = {rho:.4f}  (p = {p_spearman:.4f}) {'significatif' if p_spearman < 0.05 else 'non significatif'}")
    print()

#corrélation globale (toutes années confondues)

r_g, p_g = stats.pearsonr(df["Frequentation"], df["Taux de conformité moyen"])
rho_g, p_sg = stats.spearmanr(df["Frequentation"], df["Taux de conformité moyen"])

print(f"Toutes années confondues (N={len(df)})")
print(f"  Pearson  r   = {r_g:.4f}  (p = {p_g:.4f}) {'significatif' if p_g < 0.05 else 'non significatif'}")
print(f"  Spearman rho = {rho_g:.4f}  (p = {p_sg:.4f}) {'significatif' if p_sg < 0.05 else 'non significatif'}")

#top 2024

df24 = df[df["Année"] == 2024].copy()

print("\n top 5 des gares les plus propres (2024) :\n")
print(
    df24[["Nom gare", "Département", "Taux de conformité moyen", "Frequentation"]]
    .sort_values("Taux de conformité moyen", ascending=False)
    .head(5)
    .to_string(index=False)
)

print("\n top 5 des gares les moins propres (2024) :\n")
print(
    df24[["Nom gare", "Département", "Taux de conformité moyen", "Frequentation"]]
    .sort_values("Taux de conformité moyen", ascending=True)
    .head(5)
    .to_string(index=False)
)

print("\n gare la plus fréquentée (2024) :\n")
print(
    df24.sort_values("Frequentation", ascending=False)
    .head(1)[["Nom gare", "Département", "Frequentation", "Taux de conformité moyen"]]
    .to_string(index=False)
)

# moyenne proprété par département 
moyenne_dep = (
    df24.groupby("Département")["Taux de conformité moyen"]
    .mean()
    .reset_index()
    .sort_values("Taux de conformité moyen", ascending=False)
)

print("\n moyenne de propreté par département (Top 10, 2024) :\n")
print(moyenne_dep.head(10).to_string(index=False))




# calcule des seuils pour la carte 

# Seuils propreté

seuils_proprete = df24[ #on utilise ici les quartiles pour créer des catégories 
    "Taux de conformité moyen"
].quantile([0.33, 0.66])

seuil_proprete_bas = seuils_proprete.iloc[0]
seuil_proprete_haut = seuils_proprete.iloc[1]

print("\nseuils propreté (2024)")
print(f"Faible : < {seuil_proprete_bas:.2f}")
print(f"Moyen  : entre {seuil_proprete_bas:.2f} et {seuil_proprete_haut:.2f}")
print(f"Élevé  : > {seuil_proprete_haut:.2f}")

# Fonction catégorie propreté

def categorie_proprete(taux):
    if taux < seuil_proprete_bas:
        return "Rouge"
    elif taux < seuil_proprete_haut:
        return "Orange"
    else:
        return "Vert"

df24["Couleur proprete"] = df24[
    "Taux de conformité moyen"
].apply(categorie_proprete)

#seuil fréquentation

seuils_freq = df24[
    "Frequentation"
].quantile([0.33, 0.66])

seuil_freq_bas = seuils_freq.iloc[0]
seuil_freq_haut = seuils_freq.iloc[1]

print("\nseuils fréquentation")
print(f"Faible : < {seuil_freq_bas:.0f}")
print(f"Moyenne : entre {seuil_freq_bas:.0f} et {seuil_freq_haut:.0f}")
print(f"Élevée : > {seuil_freq_haut:.0f}")

# fonction catégorie fréquentation

def categorie_frequentation(freq):
    if freq < seuil_freq_bas:
        return "Faible"
    elif freq < seuil_freq_haut:
        return "Moyenne"
    else:
        return "Élevée"

df24["Niveau frequentation"] = df24[
    "Frequentation"
].apply(categorie_frequentation)

#moyenne par département 

carte_departements = (
    df24.groupby("Département")
    .agg({
        "Taux de conformité moyen": "mean",
        "Frequentation": "mean"
    })
    .reset_index()
)


# Graphiques

colors = {2022: '#4C72B0', 2023: '#DD8452', 2024: '#55A868'}

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 2, figure=fig)

for i, annee in enumerate([2022, 2023, 2024]):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    df_an = df[df["Année"] == annee]
    r, _ = stats.pearsonr(df_an["Frequentation"], df_an["Taux de conformité moyen"])
    rho, _ = stats.spearmanr(df_an["Frequentation"], df_an["Taux de conformité moyen"])
    ax.scatter(df_an["Frequentation"], df_an["Taux de conformité moyen"],
               alpha=0.4, s=15, color=colors[annee])
    ax.set_xlabel("Fréquentation")
    ax.set_ylabel("Taux de conformité moyen (%)")
    ax.set_title(f"{annee} (N={len(df_an)})\nPearson r={r:.3f} | Spearman ρ={rho:.3f}")
    ax.grid(True, alpha=0.3)

ax4 = fig.add_subplot(gs[1, 1])
for annee in [2022, 2023, 2024]:
    df_an = df[df["Année"] == annee]
    ax4.scatter(df_an["Frequentation"], df_an["Taux de conformité moyen"],
                alpha=0.3, s=10, color=colors[annee], label=str(annee))
ax4.set_xlabel("Fréquentation")
ax4.set_ylabel("Taux de conformité moyen (%)")
ax4.set_title(f"Toutes années (N={len(df)})\nPearson r={r_g:.3f} | Spearman ρ={rho_g:.3f}")
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle("Fréquentation des gares vs Propreté — SNCF", fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig("graphique_correlation.png", dpi=150, bbox_inches='tight')
plt.close()

print("\nGraphique sauvegardé : graphique_correlation.png")

