import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

edges = [
    ("A", "B", 1),
    ("A", "C", 2),
    ("B", "D", 2),
    ("B", "F", 3),
    ("C", "D", 3),
    ("C", "E", 4),
    ("D", "F", 3),
    ("D", "E", 2),
    ("D", "G", 3),
    ("F", "G", 4),
    ("E", "G", 5),
]

G.add_weighted_edges_from(edges)

# Position des noeuds (pour garder une forme jolie)
pos = {
    "A": (0, 1),
    "B": (1, 2),
    "C": (1, 0),
    "D": (3, 1),
    "F": (5, 2),
    "E": (5, 0),
    "G": (7, 1),
}


def afficher_etape(G, pos, distances, visites, courant):
    plt.figure(figsize=(10, 5))

    couleurs = []

    for node in G.nodes():
        if node == courant:
            # noeud actuel
            couleurs.append("orange")      
        elif node in visites:
             # déjà visité
            couleurs.append("lightgreen") 
        else:
            # pas encore visité
            couleurs.append("lightblue")   

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=couleurs,
        node_size=2000,
        font_size=14
    )

    # poids des arêtes
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # affichage des distances
    texte = "Distances depuis A :\n"
    for node, dist in distances.items():
        texte += f"{node} : {dist}\n"

    plt.text(
        8,
        1,
        texte,
        fontsize=12,
        bbox=dict(facecolor="white")
    )

    plt.title(f"Noeud courant : {courant}")
    plt.axis("off")
    plt.show()


def dijkstra(G, depart):

    # distances initiales
    distances = {node: float("inf") for node in G.nodes()}
    distances[depart] = 0

    visites = set()

    while len(visites) < len(G.nodes()):

        # choisir le noeud non visité le plus proche
        courant = None
        distance_min = float("inf")

        for node in G.nodes():
            if node not in visites and distances[node] < distance_min:
                distance_min = distances[node]
                courant = node

        # affichage
        afficher_etape(G, pos, distances, visites, courant)

        # marquer comme visité
        visites.add(courant)

        # mise à jour des voisins
        for voisin in G.neighbors(courant):

            poids = G[courant][voisin]["weight"]

            nouvelle_distance = distances[courant] + poids

            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance

    return distances


resultat = dijkstra(G, "A")

print("\nDistances finales :")
for node, dist in resultat.items():
    print(f"A -> {node} = {dist}")