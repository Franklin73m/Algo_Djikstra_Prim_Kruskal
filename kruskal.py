import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# Trier les arêtes par poids croissant
# Ajouter les arêtes à l'ACM si elles ne forment pas de cycle
# Retourner l'ACM


# ─────────────────────────────────────────
# Union-Find
# ─────────────────────────────────────────
parent = []
rang   = []

def init(n):
    global parent, rang
    parent = list(range(n))
    rang   = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry:
        return False
    if rang[rx] < rang[ry]:
        rx, ry = ry, rx
    parent[ry] = rx
    if rang[rx] == rang[ry]:
        rang[rx] += 1
    return True

# ─────────────────────────────────────────
# Kruskal
# ─────────────────────────────────────────
def kruskal(n, aretes):
    init(n)
    aretes_triees = sorted(aretes, key=lambda e: e[2])
    acm           = []
    poids_total   = 0
    etapes        = []   # snapshot à chaque décision

    for u, v, poids in aretes_triees:
        if union(u, v):
            acm.append((u, v, poids))
            poids_total += poids
            decision = "acceptee"
        else:
            decision = "rejetee"

        etapes.append({
            "arete"     : (u, v, poids),
            "decision"  : decision,
            "acm"       : list(acm),
            "poids_total": poids_total,
        })

        if len(acm) == n - 1:
            break

    return acm, poids_total, etapes

# ─────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────
def dessiner(G, pos, etapes, aretes_toutes):

    nb    = len(etapes)
    cols  = 3
    rows  = (nb + cols) // cols   # +1 pour la slide finale ACM complet
    fig, axes = plt.subplots(rows, cols, figsize=(18, rows * 5))
    axes  = axes.flatten()
    fig.patch.set_facecolor("#0D1B2A")

    GRIS    = "#4A5568"
    VERT    = "#38A169"
    ROUGE   = "#E53E3E"
    ORANGE  = "#DD6B20"
    BLANC   = "#F7FAFC"
    JAUNE   = "#ECC94B"
    BG      = "#1A2535"

    def draw_step(ax, etape, titre, acm_aretes):
        ax.set_facecolor(BG)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2D3748")

        arete_courante = (etape["arete"][0], etape["arete"][1])
        est_acceptee   = etape["decision"] == "acceptee"

        # Couleur de chaque arête
        edge_colors = []
        edge_widths = []
        edge_styles = []
        for u, v, w in aretes_toutes:
            if (u, v) in acm_aretes or (v, u) in acm_aretes:
                edge_colors.append(VERT)
                edge_widths.append(3.5)
                edge_styles.append("solid")
            elif (u, v) == arete_courante or (v, u) == arete_courante:
                edge_colors.append(VERT if est_acceptee else ROUGE)
                edge_widths.append(3.0)
                edge_styles.append("solid")
            else:
                edge_colors.append(GRIS)
                edge_widths.append(1.2)
                edge_styles.append("dashed")

        # Sommets dans l'ACM = verts, sinon bleutés
        noeuds_acm = set()
        for u, v in acm_aretes:
            noeuds_acm.add(u); noeuds_acm.add(v)

        node_colors = [VERT if n in noeuds_acm else "#2B4C7E" for n in G.nodes()]

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=700, edgecolors=BLANC, linewidths=1.5)
        nx.draw_networkx_labels(G, pos, ax=ax,
                                font_color=BLANC, font_size=13, font_weight="bold")

        # Arêtes une par une pour gérer les styles différents
        for i, (u, v, w) in enumerate(aretes_toutes):
            style = edge_styles[i]
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax,
                                   edge_color=edge_colors[i],
                                   width=edge_widths[i],
                                   style=style, alpha=0.9)

        # Poids sur les arêtes
        labels_poids = {(u, v): w for u, v, w in aretes_toutes}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_poids, ax=ax,
                                     font_color=JAUNE, font_size=10,
                                     bbox=dict(boxstyle="round,pad=0.2",
                                               fc="#1A2535", ec="none", alpha=0.8))

        ax.set_title(titre, color=BLANC, fontsize=11, fontweight="bold", pad=10)
        ax.axis("off")

    # ── Dessiner chaque étape ──
    for i, etape in enumerate(etapes):
        u, v, w   = etape["arete"]
        decision  = "[OK] Acceptee" if etape["decision"] == "acceptee" else "[X]  Rejetee (cycle)"
        titre     = f"Etape {i+1}  |  ({u}-{v}) poids={w}  {decision}"
        acm_edges = [(a, b) for a, b, _ in etape["acm"]]

        # Arêtes déjà dans l'ACM AVANT cette étape (sauf la courante si rejetée)
        if etape["decision"] == "acceptee":
            acm_avant = acm_edges[:-1]
        else:
            acm_avant = acm_edges

        draw_step(axes[i], etape, titre, acm_avant)

    # ── Dernière case : ACM final ──
    ax_final = axes[len(etapes)]
    ax_final.set_facecolor(BG)
    for spine in ax_final.spines.values():
        spine.set_edgecolor("#2D3748")

    acm_final_edges = [(a, b) for a, b, _ in etapes[-1]["acm"]]
    edge_colors = []
    edge_widths = []
    edge_styles = []
    for u, v, w in aretes_toutes:
        if (u, v) in acm_final_edges or (v, u) in acm_final_edges:
            edge_colors.append(VERT)
            edge_widths.append(4.0)
            edge_styles.append("solid")
        else:
            edge_colors.append(GRIS)
            edge_widths.append(1.0)
            edge_styles.append("dashed")

    nx.draw_networkx_nodes(G, pos, ax=ax_final,
                           node_color=VERT, node_size=750,
                           edgecolors=BLANC, linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax_final,
                            font_color=BLANC, font_size=13, font_weight="bold")
    for i, (u, v, w) in enumerate(aretes_toutes):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax_final,
                               edge_color=edge_colors[i],
                               width=edge_widths[i], style=edge_styles[i], alpha=0.9)

    labels_poids = {(u, v): w for u, v, w in aretes_toutes}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_poids, ax=ax_final,
                                 font_color=JAUNE, font_size=10,
                                 bbox=dict(boxstyle="round,pad=0.2",
                                           fc="#1A2535", ec="none", alpha=0.8))

    poids_final = etapes[-1]["poids_total"]
    ax_final.set_title(f"ACM FINAL  |  Poids total = {poids_final}",
                       color=VERT, fontsize=13, fontweight="bold", pad=10)
    ax_final.axis("off")

    # ── Masquer les cases vides ──
    for j in range(len(etapes) + 1, len(axes)):
        axes[j].set_visible(False)

    # ── Légende ──
    legende = [
        mpatches.Patch(color=VERT,   label="Arête ACM (acceptée)"),
        mpatches.Patch(color=ROUGE,  label="Arête rejetée (cycle)"),
        mpatches.Patch(color=GRIS,   label="Arête non traitée"),
        mpatches.Patch(color=ORANGE, label="Arête courante"),
    ]
    fig.legend(handles=legende, loc="lower center", ncol=4,
               facecolor="#1A2535", edgecolor="#2D3748",
               labelcolor=BLANC, fontsize=11, framealpha=0.9,
               bbox_to_anchor=(0.5, 0.01))

    fig.suptitle("Algorithme de Kruskal — Arbre Couvrant Minimum",
                 color=BLANC, fontsize=16, fontweight="bold", y=1.01)

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig("kruskal_visuel.png",
                dpi=150, bbox_inches="tight", facecolor="#0D1B2A")
    plt.show()
    print("Image sauvegardée : kruskal_visuel.png")


# ─────────────────────────────────────────
# Graphe exemple
# ─────────────────────────────────────────
#
#   0 ──4── 1 ──5── 2
#   |       |       |
#   6       3       8
#   |       |       |
#   3 ──2── 4 ──5── 5
#
aretes = [
    (0, 1, 4),
    (0, 3, 6),
    (1, 2, 5),
    (1, 4, 3),
    (2, 5, 8),
    (3, 4, 2),
    (4, 5, 5),
]

n = 6
acm, total, etapes = kruskal(n, aretes)

print("ACM :", acm)
print("Poids total :", total)

# Construction du graphe NetworkX
G = nx.Graph()
G.add_nodes_from(range(n))
for u, v, w in aretes:
    G.add_edge(u, v, weight=w)

# Positions fixes en grille 2×3
pos = {
    0: (0, 1), 1: (1, 1), 2: (2, 1),
    3: (0, 0), 4: (1, 0), 5: (2, 0),
}

dessiner(G, pos, etapes, aretes)