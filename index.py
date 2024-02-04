import pandas as pd

# Lire les données depuis le fichier CSV dans un DataFrame
explorer_df = pd.read_csv("./parcours_explorateurs.csv")

# Extraire les noeuds de départ, les noeuds d'arrivée et créer un dictionnaire associant les noeuds amonts aux noeuds aval
array_starting_node = explorer_df[explorer_df["type_aretes"] == "depart"]["noeud_amont"].values
array_arrival_node = explorer_df[explorer_df["type_aretes"] == "arrivee"]["noeud_aval"].values
dict_upstream_downstream = {row["noeud_amont"]: row["noeud_aval"] for _, row in explorer_df.iterrows()}

# Initialiser des variables pour suivre le chemin le plus long et le plus court
longest_path = []
shortest_path = []
max_length = 0
min_length = float('inf')

# Calculer des métriques pour tous les chemins
all_paths = []
for starting_node in array_starting_node:
    current_path = [starting_node]
    while current_path[-1] not in array_arrival_node:
        current_node = current_path[-1]
        next_node = dict_upstream_downstream[current_node]
        current_path.append(next_node)

    # Mettre à jour les chemins le plus long et le plus court ainsi que leurs longueurs
    length_path = len(current_path)
    if length_path > max_length:
        longest_path = current_path
        max_length = length_path
    if length_path < min_length:
        shortest_path = current_path
        min_length = length_path
    
    all_paths.append(current_path)

# Calculer des métriques pour tous les chemins
lengths = [len(path) for path in all_paths]
average_length = sum(lengths) / len(lengths)
median_length = sorted(lengths)[len(lengths) // 2]
std_deviation = pd.Series(lengths).std()
iqr = pd.Series(lengths).quantile(0.75) - pd.Series(lengths).quantile(0.25)

print("Chemin le plus long :", longest_path)
print("Longueur du chemin le plus long :", max_length)
print("\nChemin le plus court :", shortest_path)
print("Longueur du chemin le plus court :", min_length)
print("\nMétriques pour tous les chemins :")
print("Longueur moyenne :", average_length)
print("Longueur médiane :", median_length)
print("Écart-type :", std_deviation)
print("Écart interquartile :", iqr)
