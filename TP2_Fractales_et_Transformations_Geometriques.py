import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------
# QUESTION 1.a : Homothétie
# ----------------

# Fonction qui renvoie la matrice projective d'une homothétie de centre O
# et de rapport k (k ≠ 0)
def homothetie(k):
    H = np.array([
        [k, 0, 0],
        [0, k, 0],
        [0, 0, 1]
    ])
    return H

# ---------------
# QUESTION 1.b : Rotation
# ---------------

# Fonction qui renvoie la matrice projective d'une rotation de centre O
# et d'angle alpha (en radians)
def rotation(alpha):
    cos = np.cos(alpha)
    sin = np.sin(alpha)
    
    R = np.array([
        [cos, -sin, 0],
        [sin,  cos, 0],
        [  0,    0, 1]
    ])
    return R

# --------------
# QUESTION 1.c : Translation
# --------------

# Fonction qui renvoie la matrice projective d'une translation
# de vecteur allant de O vers a = (ax, ay)
def translation(a):
    ax, ay = a  # coordonnées du point a
    T = np.array([
        [1, 0, ax],
        [0, 1, ay],
        [0, 0,  1 ]
    ])
    return T

# ---------------------
# TESTS
# ---------------------

print("Homothétie de rapport 0.5 :")
print(homothetie(0.5))

print("\nRotation d’angle pi/4 :")
print(rotation(np.pi/4))

print("\nTranslation selon le vecteur (1, 2) :")
print(translation((1, 2)))



# ------------------
# EXERCICE 2.b : génération de la fractale
# -------------------

# fct qui applique une transfo affine à une liste de points en coord homogènes
def appliquer_transfo(M, T):
     return np.dot(T, M)   # pas sûr que ce soit dans le bon sens, mais ça marche

# fct fract2 : construit les différentes itérations à partir de M0
def fract2(M0, a, affiche=True):

    alpha = np.pi / 4   #45°

    k = 0.5   # homothetie (demi taille)


    # matrices de base
    h = homothetie(k)
    r1 = rotation(alpha)
    r2 = rotation(-alpha)
    t = translation(a)

    # composition des opérations : t o r o h
    g1 = t @ r1 @ h
    g2 = t @ r2 @ h

    # passage en coord homogène (faut rajouter une ligne de 1 en bas)
    M0_h = np.vstack((M0.T, np.ones(M0.shape[0])))  # (3 x 2)

    # étape M1 = g0 + g1 + g2 appliqués sur M0
    M1 = np.hstack([
        M0_h,
        appliquer_transfo(M0_h, g1),
        appliquer_transfo(M0_h, g2)
    ])

    # étape M2 = on applique g1 et g2 à chaque segment de M1
    M2 = np.empty((3,0))  # on part d’un tableau vide

    for i in range(0, M1.shape[1], 2):
        seg = M1[:, i:i+2]

        M2 = np.hstack([
            M2,
            seg,
            appliquer_transfo(seg, g1),
            appliquer_transfo(seg, g2)
        ])

    # AFFICHAGE du tout
    for i in range(0, M2.shape[1], 2):
        x = M2[0, i:i+2]
        y = M2[1, i:i+2]
        plt.plot(x, y, 'k-')  # trait noir

    plt.axis('equal')  # sinon c’est écrasé
    plt.title("Fractale construite à partir de M0")
    
    if affiche:
        plt.show() #nécessaire pour la question c


# ---------------
# TEST
# ---------------

# M0 : segment vertical [O,a] avec O=(0,0) et a=(0,1)
M0 = np.array([[0, 0], [0, 1]])
fract2(M0, (0, 1))  # translation vers le haut

# ----------------
# EXERCICE 2.c : motif de base = carré
# ----------------

# cette fois au lieu d’un segment, on veut partir d’un carré centré en (0,0)
# on va considérer les 4 côtés comme des segments

# on donne les sommets du carré (côté = 1)
# les points sont ordonnés dans le sens trigonométrique
points = [
    [(-0.5, -0.5), (0.5, -0.5)],   # bas
    [(0.5, -0.5), (0.5, 0.5)],     # droite
    [(0.5, 0.5), (-0.5, 0.5)],     # haut
    [(-0.5, 0.5), (-0.5, -0.5)]    # gauche
]

plt.figure()  # très important sinon ça ouvre 4 fenêtres

# pour chaque côté du carré, on applique fract2
# on construit le segment en colonne, puis on calcule le vecteur associé
for p1, p2 in points:
    seg = np.array([p1, p2]).T  # 2x2, chaque colonne = un point
    vecteur = (p2[0] - p1[0], p2[1] - p1[1])  # translation = direction du segment
    fract2(seg, vecteur, affiche=False)  # on n'affiche qu'à la fin

# affichage final
plt.title("Fractale construite à partir d’un carré")
plt.axis('equal')  # sinon c’est pas beau
plt.show()



# ---------------
# EXERCICE 2.d : fractale 3D
# ---------------

# homothétie en 3D de centre O, rapport k
def homothetie3d(k):
    return np.array([
        [k, 0, 0, 0],
        [0, k, 0, 0],
        [0, 0, k, 0],
        [0, 0, 0, 1]
    ])

# rotation autour de l’axe X (angle alpha en radians)
def rotation_x(alpha):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha), 0],
        [0, np.sin(alpha),  np.cos(alpha), 0],
        [0, 0, 0, 1]
    ])

# translation 3D selon un vecteur (ax, ay, az)
def translation3d(a):
    ax, ay, az = a
    return np.array([
        [1, 0, 0, ax],
        [0, 1, 0, ay],
        [0, 0, 1, az],
        [0, 0, 0, 1]
    ])

# applique une transfo 4x4 sur des points homogènes 4xN
def appliquer_transfo3d(M, T):
    return T @ M

# fonction récursive pour dessiner la fractale
def fractale3d(ax, M0, depth):
    if depth == 0:
        return
    alpha = np.pi / 4
    k = 0.5
    trans = translation3d((0, 0, 1))  # on monte en Z
    h = homothetie3d(k)
    r1 = rotation_x(alpha)
    r2 = rotation_x(-alpha)
    g1 = trans @ r1 @ h
    g2 = trans @ r2 @ h
    M0_h = np.vstack((M0, np.ones((1, M0.shape[1]))))  # 4x2
    # On dessine le segment de base
    ax.plot(M0[0], M0[1], M0[2], 'k-')
    # On applique les deux transformations
    M1 = appliquer_transfo3d(M0_h, g1)
    M2 = appliquer_transfo3d(M0_h, g2)
    # On appelle récursivement sur les deux nouveaux segments
    fractale3d(ax, M1[:3], depth-1)
    fractale3d(ax, M2[:3], depth-1)

# ----------------------
# TESTS 3D
# ----------------------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# segment de base : vertical en Z
M0 = np.array([
    [0, 0],
    [0, 0],
    [0, 1]
])

# profondeur de récursion (on modifie ici la profondeur)
fractale3d(ax, M0, depth=6)

ax.set_title("Fractale 3D récursive (axe X)")
plt.show()
