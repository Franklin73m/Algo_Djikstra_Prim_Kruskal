import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 1. Création du graphe complet
G = nx.Graph()
edges = [
    ("A", "B", 7),
    ("B", "C", 3),
    ("A", "C", 4),
    ("C", "D", 6),
    ("B", "D", 2),
]
G.add_weighted_edges_from(edges)

# Position fixe pour que les sommets ne bougent pas entre les étapes
pos = nx.spring_layout(G, seed=42)


GRIS = "#4A5568"
ROUGE = "#E53E3E"
BLANC = "#F7FAFC"
JAUNE = "#ECC94B"
BG = "#1A2535"


def draw_step(ax, current_edges, title):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2D3748")

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color="#2B4C7E",
        node_size=2000,
        edgecolors=BLANC,
        linewidths=1.5,
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_color=BLANC, font_size=12, font_weight="bold"
    )

    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color=GRIS, width=1.2, style="dashed", alpha=0.85
    )

    if current_edges:
        nx.draw_networkx_edges(
            G,
            pos,
            ax=ax,
            edgelist=current_edges,
            edge_color=ROUGE,
            width=3.5,
        )

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        ax=ax,
        edge_labels=edge_labels,
        font_color=JAUNE,
        font_size=9,
        bbox=dict(boxstyle="round,pad=0.2", fc="#1A2535", ec="none", alpha=0.8),
    )

    ax.set_title(title, color=BLANC, fontsize=10, fontweight="bold", pad=10)
    ax.axis("off")


def dessiner_toutes_les_etapes(etapes):
    nb = len(etapes)
    cols = 2
    rows = (nb + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(14, 5 * rows))
    fig.patch.set_facecolor("#0D1B2A")

    if rows * cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, (current_edges, title) in enumerate(etapes):
        draw_step(axes[i], current_edges, title)

    for j in range(nb, len(axes)):
        axes[j].set_visible(False)

    legende = [
        mpatches.Patch(color=ROUGE, label="Arêtes sélectionnées"),
        mpatches.Patch(color=GRIS, label="Arêtes possibles (non choisies)"),
    ]
    fig.legend(
        handles=legende,
        loc="lower center",
        ncol=2,
        facecolor="#1A2535",
        edgecolor="#2D3748",
        labelcolor=BLANC,
        fontsize=10,
        framealpha=0.9,
        bbox_to_anchor=(0.5, 0.01),
    )

    fig.suptitle(
        "Algorithme de Prim",
        color=BLANC,
        fontsize=14,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.show()


# ÉTAPES
# 1) Choisir un sommet de départ et l'ajouter à l'arbre.
# 2) Examiner toutes les arêtes d'un sommet de l'arbre vers un sommet hors arbre.
# 3) Prendre l'arête de poids minimum.
# 4) Ajouter cette arête et le nouveau sommet à l'arbre.
# 5) Répéter 2–4 jusqu'à inclure tous les sommets.

etapes_prim = [
    ([], "Étape 0 : Graphe initial"),
    (
        [("A", "C")],
        "Étape 1 : Sommet de départ A.\n"
        "Arêtes arbre → hors arbre : A-B(7), A-C(4) → plus petit poids : A-C",
    ),
    (
        [("A", "C"), ("B", "C")],
        "Étape 2 : Arbre = {A, C}.\n"
        "Arêtes arbre → hors arbre : A-B(7), B-C(3), C-D(6) → plus petit poids : B-C",
    ),
    (
        [("A", "C"), ("B", "C"), ("B", "D")],
        "Étape 3 : Arbre = {A, B, C}.\n"
        "Arêtes arbre → hors arbre : B-D(2), C-D(6) → plus petit poids : B-D\n",
    ),
]

dessiner_toutes_les_etapes(etapes_prim)

step3 = [("A", "C"), ("B", "C"), ("B", "D")]
cost = sum(G[u][v]["weight"] for u, v in step3)
print(f"Arbre final : {step3}\nCoût total : {cost}")
