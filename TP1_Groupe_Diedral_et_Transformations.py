from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import math


# ------------------------
# Question 1 -Transformations de base
# --------------------------

def rote(theta, point):
    # Applique une rotation dangle theta (en rad) au point (x, y)
    x, y = point
    x_rotated = x * math.cos(theta) - y * math.sin(theta)
    y_rotated = x * math.sin(theta) + y * math.cos(theta)
    return (x_rotated, y_rotated)


def syme(point):
    # Renvoie le point symétrique par rapport a l'axe horizontal
    x, y = point
    return (x, -y)

print("Test rotation 90° de (1,1) :", rote(math.pi / 2, (1, 1)))
print("Symétrie de (1,1) :", syme((1, 1)))

# --------------------------
# Question 3 - Structure du groupe diédral D_{2n}
# --------------------------

def trad_dec_qu(k, n):
    #Transforme un entier k en (alpha,beta) avec alpha dans {0,1}
    alpha = k // n
    beta = k % n
    return (alpha, beta)

def trad_qu_dec(t, n):
    # Transforme un couple (alpha, beta) en un entier unique k
    alpha, beta = t
    return alpha * n + beta

def compose(i, j, n):
    # Donne la composition sigma_i o sigma_j dans D_{2n}
    alpha_i, beta_i = trad_dec_qu(i, n)
    alpha_j, beta_j = trad_dec_qu(j, n)

    if alpha_i == 0 and alpha_j == 0:
        alpha_res = 0
        beta_res = (beta_i + beta_j) % n
    elif alpha_i == 0 and alpha_j == 1:
        alpha_res = 1
        beta_res = (beta_j - beta_i) % n
    elif alpha_i == 1 and alpha_j == 0:
        alpha_res = 1
        beta_res = (beta_i + beta_j) % n
    else:
        alpha_res = 0
        beta_res = (beta_j - beta_i) % n

    return trad_qu_dec((alpha_res, beta_res), n)

def inverse(i, n):
    # Renvoie l'inverse de l'élément i dans D_{2n}
    alpha, beta = trad_dec_qu(i, n)
    return trad_qu_dec((alpha, (-beta) % n), n)

def construire_table_groupe(n):
    # Construction de la table de Cayley pour D_{2n}
    taille = 2 * n
    table = [[0] * taille for _ in range(taille)]

    for i in range(taille):
        for j in range(taille):
            table[i][j] = compose(i, j, n)

    # Affichage de la table
    print(f"\nTable du groupe D_{2*n} :")
    print("   | " + " ".join(f"{j:2}" for j in range(taille)))
    print("---+" + "-" * (3 * taille))
    for i in range(taille):
        ligne = f"{i:2} | " + " ".join(f"{table[i][j]:2}" for j in range(taille))
        print(ligne)

    return table

def sous_groupe_engendre(generateurs, n):
    # génère un sous-groupe à partir d'un ensemble de générateurs
    sous_groupe = set(generateurs)
    sous_groupe.add(0)  # ajouter l'identité

    while True:
        taille_avant = len(sous_groupe)
        nouveaux = set(compose(i, j, n) for i in sous_groupe for j in sous_groupe)
        sous_groupe.update(nouveaux)
        if len(sous_groupe) == taille_avant:
            break

    return sorted(sous_groupe)

def trouver_tous_sous_groupes(n):
    # Cherche tout les sous-groupes par génération
    taille = 2 * n
    generateurs = list(range(taille))
    sous_groupes = []

    for r in range(1, 4):
        for combinaison in combinations(generateurs, r):
            sg = sous_groupe_engendre(list(combinaison), n)
            if sg not in sous_groupes:
                sous_groupes.append(sg)

    if [0] not in sous_groupes:
        sous_groupes.insert(0, [0])
    if sorted(generateurs) not in sous_groupes:
        sous_groupes.append(sorted(generateurs))

    return sorted(sous_groupes, key=lambda x: (len(x), x))

def diagramme_hasse(sous_groupes):
    # Affiche les inclusions directes entre sous-groupes
    print("\nDiagramme de Hasse (texte) :")
    for i, sg1 in enumerate(sous_groupes):
        print(f"Sous-groupe {i} : {sg1}")
        parents = []
        for j, sg2 in enumerate(sous_groupes):
            if i != j and set(sg1).issubset(set(sg2)):
                est_direct = True
                for k, sg3 in enumerate(sous_groupes):
                    if k != i and k != j and set(sg1).issubset(set(sg3)) and set(sg3).issubset(set(sg2)):
                        est_direct = False
                        break
                if est_direct:
                    parents.append(j)
        if parents:
            print(f"  Inclus directement dans : {parents}")
        print()

def dessiner_hasse_vertical(sous_groupes):
    # Représente le diagramme de Hasse avec NetworkX
    G = nx.DiGraph()
    niveaux = {}

    for i, sg in enumerate(sous_groupes):
        G.add_node(i, label=f"S{i}: {sg}")
        niveaux[i] = len(sg)

    for i, sg1 in enumerate(sous_groupes):
        for j, sg2 in enumerate(sous_groupes):
            if i != j and set(sg1).issubset(set(sg2)):
                est_direct = True
                for k, sg3 in enumerate(sous_groupes):
                    if k != i and k != j and set(sg1).issubset(set(sg3)) and set(sg3).issubset(set(sg2)):
                        est_direct = False
                        break
                if est_direct:
                    G.add_edge(i, j)

    niveaux_dict = {}
    for node, niveau in niveaux.items():
        niveaux_dict.setdefault(niveau, []).append(node)

    pos = {}
    for y, (niveau, noeuds) in enumerate(sorted(niveaux_dict.items())):
        for x, node in enumerate(noeuds):
            pos[node] = (x, -y)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, arrows=True, node_size=2000,
            node_color='lightblue', edge_color='gray')
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=9)
    plt.title("Diagramme de Hasse des sous-groupes de D_{2n}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# --------------------------
# Question 4a- Applications graphique
# -------------------------

def appliquer_transformation(sigma_index, point, n):
    # Applique une transformation de D_{2n} sur un point
    alpha, beta = trad_dec_qu(sigma_index, n)
    angle = 2 * math.pi * beta / n

    if alpha == 0:
        return rote(angle, point)
    else:
        return syme(rote(angle, point))

def create_motif(H, n, index=None):
    # Génère une figure géométrique obtenue par action de H
    A = (2, 2)
    B = (2, 1)
    O = (0, 0)

    plt.figure(figsize=(6, 6))
    ax = plt.gca()
    ax.set_aspect('equal')

    for sigma in H:
        A_img = appliquer_transformation(sigma, A, n)
        B_img = appliquer_transformation(sigma, B, n)
        plt.plot([O[0], A_img[0]], [O[1], A_img[1]], 'b')
        plt.plot([O[0], B_img[0]], [O[1], B_img[1]], 'r')

    titre = f"Motif pour H = {H} dans D₂ₙ (n = {n})"
    if index is not None:
        titre = f"Sous-groupe {index} : {H}"

    plt.title(titre)
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# --------------------------
# Exemples d'utilisation avec n = 4
# --------------------------

n = 4  

# 1. Table de composition
construire_table_groupe(n)

# 2. Liste des sous-groupes
sous_groupes = trouver_tous_sous_groupes(n)
print("\nListe des sous-groupes :")
for i, sg in enumerate(sous_groupes):
    print(f"Sous-groupe {i}: {sg}")

# 3. Diagramme de Hasse (texte+graphe)
diagramme_hasse(sous_groupes)
dessiner_hasse_vertical(sous_groupes)

# 4. Motifs associés a chaque sous groupe
for i, H in enumerate(sous_groupes):
    create_motif(H, n, index=i)



# --------------------------
# Historique avant généralisation (Question 3) 
# --------------------------

# from itertools import combinations
# import networkx as nx
# import matplotlib.pyplot as plt

# #Question2a
# def trad_dec_qu(k):
#     """
#     Traduit un nombre décimal en représentation en base 4
    
#     Arguments :
#     k (int) : Nombre décimal (de 0 à 7)
    
#     Retourne :
#     tuple : Représentation en base 4 (a, B)
#     """
#     alpha = (k // 4) % 2
#     beta = k % 4
#     return (alpha, beta)

# def trad_qu_dec(base4_tuple):
#     """
#     Traduit une représentation en base 4 en nombre décimal
    
#     Arguments :
#     base4_tuple (tuple) : Représentation en base 4 (a, B)
    
#     Retourne :
#     int : Nombre décimal
#     """
#     alpha, beta = base4_tuple
#     return 4 * alpha + beta

# #Question 2b a partir de la 



# def compose(i, j):
#     """
#     Compose deux transformations σi et σj dans D8 et renvoie l'indice k tel que σi ∘ σj = σk.
    
#     Args:
#         i (int): Indice de la première transformation (0 à 7)
#         j (int): Indice de la deuxième transformation (0 à 7)
    
#     Returns:
#         int: Indice k (0 à 7) de la transformation résultante
#     """
#     # Convertir les indices en paires (α, β)
#     alpha_i, beta_i = trad_dec_qu(i)
#     alpha_j, beta_j = trad_dec_qu(j)
    
#     # Règles de composition du groupe diédral
#     if alpha_i == 0 and alpha_j == 0:
#         # Rotation ∘ Rotation = Rotation
#         alpha_result = 0
#         beta_result = (beta_i + beta_j) % 4
#     elif alpha_i == 0 and alpha_j == 1:
#         # Rotation ∘ Symétrie = Symétrie
#         alpha_result = 1
#         beta_result = (beta_j - beta_i) % 4
#     elif alpha_i == 1 and alpha_j == 0:
#         # Symétrie ∘ Rotation = Symétrie
#         alpha_result = 1
#         beta_result = (beta_i + beta_j) % 4
#     else:  # alpha_i == 1 and alpha_j == 1
#         # Symétrie ∘ Symétrie = Rotation
#         alpha_result = 0
#         beta_result = (beta_j - beta_i) % 4
    
#     # Convertir le résultat en indice k
#     k = trad_qu_dec((alpha_result, beta_result))
#     return k

# # Tests
# print("Tests de composition dans D8 :")
# print("r¹ ∘ r² =", compose(1, 2))  # r¹ ∘ r² = r³ (indice 3)
# print("s ∘ r¹ =", compose(4, 1))  # s ∘ r¹ = s∘r¹ (indice 5)




# #Question 2c 

# def inverse(i):
#     """
#     Trouve l'inverse de la transformation o_i dans le groupe D8
    
#     Args:
#         i (int): Indice de la transformation (0 à 7)
        
#     Returns:
#         int: Indice j de l'inverse de o_i
#     """
#     alpha, beta = trad_dec_qu(i)
    
#     # Pour les rotations (alpha = 0): l'inverse de r^k est r^(4-k) ou r^(-k mod 4)
#     if alpha == 0:
#         inverse_beta = (-beta) % 4
#         return trad_qu_dec((0, inverse_beta))
    
#     # Pour les symétries (alpha = 1): l'inverse de s∘r^k est s∘r^(-k mod 4)
#     # Car (s∘r^k)∘(s∘r^k) = id
#     else:
#         inverse_beta = (-beta) % 4
#         return trad_qu_dec((1, inverse_beta))

# # Tests
# print("Inverses dans D8:")
# for i in range(8):
#     inv = inverse(i)
#     print(f"L'inverse de σ_{i} est σ_{inv}")



# def test_abelien():
#     """Teste si D8 est abélien ou non"""
#     # Prenons deux transformations
#     i, j = 1, 4  # r¹ et s
    
#     # Calculons leur composition dans les deux sens
#     comp_ij = compose(i, j)
#     comp_ji = compose(j, i)
    
#     print(f"σ_{i} ∘ σ_{j} = σ_{comp_ij}")
#     print(f"σ_{j} ∘ σ_{i} = σ_{comp_ji}")
    
#     if comp_ij != comp_ji:
#         print("D8 n'est pas abélien car la composition n'est pas commutative")
#     else:
#         print("Ces éléments commutent")

# test_abelien()



# #Question 2d

# def construire_table_groupe():
#     """Construit et affiche la table du groupe diédral D8"""
#     n = 4  # n=4 pour D8
#     taille = 2*n
    
#     # Initialiser la table
#     table = [[0 for _ in range(taille)] for _ in range(taille)]
    
#     # Remplir la table
#     for i in range(taille):
#         for j in range(taille):
#             table[i][j] = compose(i, j)
    
#     # Afficher la table
#     print("Table du groupe diédral D8:")
#     print("   | " + " ".join(f"σ_{j}" for j in range(taille)))
#     print("---+" + "-"*(3*taille))
    
#     for i in range(taille):
#         ligne = f"σ_{i} | "
#         ligne += " ".join(f"{table[i][j]:2d}" for j in range(taille))
#         print(ligne)
    
#     return table

# table_D8 = construire_table_groupe()





# # Question 2e 
# from itertools import combinations

# def sous_groupe_engendre(generateurs):
#     """
#     Détermine le sous-groupe engendré par un ensemble de générateurs dans D8.
    
#     Args:
#         generateurs (list): Liste des indices des éléments générateurs (0 à 7)
        
#     Returns:
#         list: Liste triée des éléments du sous-groupe (sans doublons)
#     """
#     sous_groupe = set(generateurs)
#     sous_groupe.add(0)  # Ajouter l'identité

#     # Fermeture sous la composition
#     while True:
#         taille_avant = len(sous_groupe)
#         nouveaux = set(compose(i, j) for i in sous_groupe for j in sous_groupe)
#         sous_groupe.update(nouveaux)
#         if len(sous_groupe) == taille_avant:
#             break

#     return sorted(sous_groupe)


# def trouver_tous_sous_groupes():
#     """
#     Trouve tous les sous-groupes de D8 en testant toutes les combinaisons de 1 à 3 générateurs.
    
#     Returns:
#         list: Liste des sous-groupes triés par ordre de taille
#     """
#     generateurs = list(range(8))
#     sous_groupes = []

#     # Générer tous les sous-groupes à partir de 1 à 3 générateurs
#     for r in range(1, 4):
#         for combinaison in combinations(generateurs, r):
#             sg = sous_groupe_engendre(list(combinaison))
#             if sg not in sous_groupes:
#                 sous_groupes.append(sg)

#     # Ajouter le sous-groupe trivial et le groupe complet si oubliés
#     if [0] not in sous_groupes:
#         sous_groupes.insert(0, [0])
#     if sorted(generateurs) not in sous_groupes:
#         sous_groupes.append(sorted(generateurs))

#     # Trier par taille pour une lecture logique
#     return sorted(sous_groupes, key=lambda x: (len(x), x))


# def diagramme_hasse(sous_groupes):
#     """
#     Affiche le diagramme de Hasse des sous-groupes par inclusion directe.
    
#     Args:
#         sous_groupes (list): Liste de sous-groupes (chacun est une liste d'entiers)
#     """
#     print("Diagramme de Hasse des sous-groupes de D8:\n")

#     for i, sg1 in enumerate(sous_groupes):
#         print(f"Sous-groupe {i}: {sg1}")
#         parents = []

#         for j, sg2 in enumerate(sous_groupes):
#             if i != j and set(sg1).issubset(set(sg2)):
#                 # Vérifie si aucune inclusion intermédiaire
#                 est_direct = True
#                 for k, sg3 in enumerate(sous_groupes):
#                     if k != i and k != j and set(sg1).issubset(set(sg3)) and set(sg3).issubset(set(sg2)):
#                         est_direct = False
#                         break
#                 if est_direct:
#                     parents.append(f"Sous-groupe {j}: {sg2}")
#         if parents:
#             print("  Inclus directement dans:", ", ".join(parents))
#         print()

# sous_groupes = trouver_tous_sous_groupes()

# print("Liste des sous-groupes de D8:")
# for i, sg in enumerate(sous_groupes):
#     print(f"Sous-groupe {i}: {sg}")

# print("\nDiagramme de Hasse:")
# diagramme_hasse(sous_groupes)



# def dessiner_hasse_vertical(sous_groupes):
#     G = nx.DiGraph()

#     # Ajout des nœuds avec leur niveau (hauteur = taille du sous-groupe)
#     niveaux = {}
#     for i, sg in enumerate(sous_groupes):
#         G.add_node(i, label=f"S{i}: {sg}")
#         niveaux[i] = len(sg)

#     # Ajout des arêtes pour inclusions directes
#     for i, sg1 in enumerate(sous_groupes):
#         for j, sg2 in enumerate(sous_groupes):
#             if i != j and set(sg1).issubset(set(sg2)):
#                 est_direct = True
#                 for k, sg3 in enumerate(sous_groupes):
#                     if k != i and k != j and set(sg1).issubset(set(sg3)) and set(sg3).issubset(set(sg2)):
#                         est_direct = False
#                         break
#                 if est_direct:
#                     G.add_edge(i, j)

#     # Position verticale : y = -taille, x = index dans le niveau
#     niveaux_dict = {}
#     for node, niveau in niveaux.items():
#         niveaux_dict.setdefault(niveau, []).append(node)

#     pos = {}
#     for y, (niveau, noeuds) in enumerate(sorted(niveaux_dict.items())):
#         for x, node in enumerate(noeuds):
#             pos[node] = (x, -y)  # x = horizontal, y = vertical (inversé pour Hasse)

#     # Tracé
#     plt.figure(figsize=(12, 8))
#     nx.draw(G, pos, with_labels=False, arrows=True, node_size=2000,
#             node_color='lightblue', edge_color='gray')
#     labels = nx.get_node_attributes(G, 'label')
#     nx.draw_networkx_labels(G, pos, labels, font_size=9)
#     plt.title("Diagramme de Hasse des sous-groupes de D8 (version claire)")
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()

# # Utilisation
# sous_groupes = trouver_tous_sous_groupes()
# dessiner_hasse_vertical(sous_groupes)