import pandas as pd
import networkx as nx

# Charger le DataFrame
explorer_df = pd.read_csv("./parcours_explorateurs.csv")

# Initialiser les listes à l'extérieur de la boucle
array_starting_node = explorer_df[explorer_df["type_aretes"] == "depart"]["noeud_amont"].values
array_arrival_node = explorer_df[explorer_df["type_aretes"] == "arrivee"]["noeud_aval"].values
dict_upstream_downstream = {row["noeud_amont"]: row["noeud_aval"] for _, row in explorer_df.iterrows()}

# Créer un graphe dirigé à partir du DataFrame
G = nx.from_pandas_edgelist(explorer_df, 'noeud_amont', 'noeud_aval', create_using=nx.DiGraph())

# a) Trouver le chemin le plus long et calculer sa longueur
longest_path = nx.dag_longest_path(G)
longest_path_length = nx.dag_longest_path_length(G)
print("Chemin le plus long:", longest_path)
print("Longueur du chemin le plus long:", longest_path_length)

# b) Trouver le chemin le plus court et calculer sa longueur
shortest_path = nx.shortest_path(G, source='sommet_68', target='sommet_6')
shortest_path_length = len(shortest_path) - 1  # Longueur du chemin est le nombre d'arêtes entre les nœuds
print("Chemin le plus court:", shortest_path)
print("Longueur du chemin le plus court:", shortest_path_length)

# c) Calculer des métriques pour les différents chemins : moyenne / médiane / écart-type / écart-interquartile
all_paths = [longest_path, shortest_path]

# Calculer les longueurs des chemins
path_lengths = [len(path) - 1 for path in all_paths]

# Calculer les métriques
mean_length = pd.Series(path_lengths).mean()
median_length = pd.Series(path_lengths).median()
std_dev_length = pd.Series(path_lengths).std()
iqr_length = pd.Series(path_lengths).quantile(0.75) - pd.Series(path_lengths).quantile(0.25)

# Afficher les métriques pour les chemins les plus long et court
print("Moyenne des longueurs du chemin le plus long et du chemin le plus court:", mean_length)
print("Médiane des longueurs du chemin le plus long et du chemin le plus court:", median_length)
print("Écart-type des longueurs du chemin le plus long et du chemin le plus court:", std_dev_length)
print("Écart interquartile des longueurs du chemin le plus long et du chemin le plus court:", iqr_length)
