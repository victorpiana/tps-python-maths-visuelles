import numpy as np


# -------------------
# QUESTION 1.a : Affichage conventionnel d’un quaternion
# -------------------

# h est un vecteur de taille 4 représentant un quaternion : h = [t, x, y, z]
def affiche_h(h):
    t, x, y, z = h
    return f"q = {t} + {x}i + {y}j + {z}k"

# ---------------
# TEST
# ---------------

h = [1, 2, 3, 4]
print(affiche_h(h))  # Résultat attendu : "q = 1 + 2i + 3j + 4k"



# -------------------
# QUESTION 1.b : Somme de deux quaternions
# -------------------

# h1 et h2 sont deux quaternions représentés comme des vecteurs [t, x, y, z]
def somme_h(h1, h2):
    return [h1[i] + h2[i] for i in range(4)]

# ---------------
# TEST
# ---------------

h1 = [1, 2, 3, 4]
h2 = [5, 6, 7, 8]
print("Somme des quaternions :", somme_h(h1, h2))  # Résultat attendu : [6, 8, 10, 12]


# -------------------
# QUESTION 1.c : Produit de deux quaternions
# -------------------

# h1 et h2 sont des quaternions représentés comme des vecteurs [t, x, y, z]
def produit_h(h1, h2):
    t1, x1, y1, z1 = h1
    t2, x2, y2, z2 = h2

    # parties vectorielles
    v1 = np.array([x1, y1, z1])
    v2 = np.array([x2, y2, z2])

    # partie scalaire
    t = t1 * t2 - np.dot(v1, v2)

    # partie vectorielle
    v = t1 * v2 + t2 * v1 + np.cross(v1, v2)

    return [t, v[0], v[1], v[2]]

# ---------------
# TEST
# ---------------

h1 = [2, -1, 0, 3]
h2 = [0, 4, 1, -2]
print("Produit des quaternions :", produit_h(h1, h2))


# -------------------------
# QUESTION 1.d : Conjugué, module, inverse
# -------------------------

# renvoie le conjugué : on garde t, on change les signes du vecteur
def conjugue_h(h):
    return [h[0], -h[1], -h[2], -h[3]]

# calcule la norme (racine de la somme des carrés)
def module_h(h):
    return np.sqrt(sum([x**2 for x in h]))

# renvoie l'inverse si la norme n’est pas nulle
def inverse_h(h):
    mod = module_h(h)
    if mod == 0:
        print("Erreur : impossible d’inverser un quaternion nul")
        return None
    conj = conjugue_h(h)
    return [x / mod**2 for x in conj]

# ---------------
# TESTS
# ---------------

h = [1, -2, 1, 0]

print("Conjugué :", conjugue_h(h))
print("Module :", module_h(h))
print("Inverse :", inverse_h(h))

# test avec un quaternion nul
h_zero = [0, 0, 0, 0]
print("Inverse du quaternion nul :", inverse_h(h_zero))




# -------------------------
# QUESTION 2.a : Forme polaire
# -------------------------
# renvoie la forme polaire d’un quaternion non nul
def polaire_h(h):
    r = module_h(h)
    if r == 0:
        print("Erreur : le quaternion est nul")
        return None
    
    t = h[0]
    vec = np.array(h[1:])

    # calcul de l'angle (en radians)
    theta = np.arccos(t / r)

    # vecteur unitaire dans la direction de la partie imaginaire
    if np.linalg.norm(vec) == 0:
        i = [0, 0, 0]  # pas de direction (angle = 0)
    else:
        i = vec / np.linalg.norm(vec)

    return [r, theta, i[0], i[1], i[2]]
# ---------------
# TEST
# ---------------
h = [1, 1, 0, 0]
print("Forme polaire :", polaire_h(h))

# -------------------------
# QUESTION 2.b : Forme algébrique à partir de la forme polaire
# -------------------------

# r : module, theta : angle, i : vecteur unitaire (liste de taille 3)
def algebrique_h(r, theta, i):
    t = r * np.cos(theta)
    vec = r * np.sin(theta) * np.array(i)
    return [t, vec[0], vec[1], vec[2]]

# ---------------
# TEST
# ---------------

polaire = polaire_h([1, 1, 0, 0])  # on récupère r, theta, i, j, k
r = polaire[0]
theta = polaire[1]
vecteur = polaire[2:5]

print("Forme algébrique reconstruite :", algebrique_h(r, theta, vecteur))


# -------------------------
# QUESTION 3 : Vérification de l’associativité
# -------------------------

def verif_associativite(nb_essais=100):
    for _ in range(nb_essais):
        # quaternions générés aléatoirement
        a = np.random.rand(4)
        b = np.random.rand(4)
        c = np.random.rand(4)

        # calcul des deux côtés
        gauche = produit_h(produit_h(a, b), c)
        droite = produit_h(a, produit_h(b, c))

        # test avec une tolérance (pour les arrondis)
        if not np.allclose(gauche, droite, atol=1e-10):
            print("Associativité non vérifiée pour :")
            print("a =", a)
            print("b =", b)
            print("c =", c)
            return False

    print("Associativité vérifiée sur", nb_essais, "essais")
    return True
# ---------------
# TEST
# ---------------
verif_associativite()


# -------------------------
# QUESTION 4.a : Matrice de rotation à partir d’un vecteur unitaire et d’un angle
# -------------------------
# n : vecteur unitaire (axe de rotation), theta : angle en radians
def matrice_rotation(n, theta):
    x, y, z = n
    c = np.cos(theta)
    s = np.sin(theta)
    v = 1 - c

    # matrice de rotation (formule de Rodrigues)
    R = np.array([
        [x*x*v + c,   x*y*v - z*s, x*z*v + y*s],
        [x*y*v + z*s, y*y*v + c,   y*z*v - x*s],
        [x*z*v - y*s, y*z*v + x*s, z*z*v + c]
    ])
    return R

# ---------------
# TEST
# ---------------

n = [0, 0, 1]  # axe Z
theta = np.pi / 3  # 60°
print("Matrice de rotation (cours) :", matrice_rotation(n, theta))


# -------------------------
# QUESTION 4.b  : Matrice de rotation à partir d’un quaternion unitaire
# -------------------------

# h : quaternion unitaire [t, x, y, z]
def h_rot(h):
    t, x, y, z = h

    r00 = 1 - 2*y**2 - 2*z**2
    r01 = 2*x*y - 2*t*z
    r02 = 2*x*z + 2*t*y

    r10 = 2*x*y + 2*t*z
    r11 = 1 - 2*x**2 - 2*z**2
    r12 = 2*y*z - 2*t*x

    r20 = 2*x*z - 2*t*y
    r21 = 2*y*z + 2*t*x
    r22 = 1 - 2*x**2 - 2*y**2

    return np.array([
        [r00, r01, r02],
        [r10, r11, r12],
        [r20, r21, r22]
    ])

# ---------------
# TEST
# ---------------

# angle θ = π/3 → donc θ/2 = π/6
# cos(π/6) ≈ 0.86603, sin(π/6) ≈ 0.5
h = [0.86603, 0, 0, 0.5]

print("Matrice de rotation (à partir du quaternion) :")
print(h_rot(h))


# -------------------------
# QUESTION 4.c : Retrouver le quaternion unitaire à partir d’une matrice de rotation
# -------------------------

# R : matrice de rotation 3x3
def rot_h(R):
    r00, r01, r02 = R[0]
    r10, r11, r12 = R[1]
    r20, r21, r22 = R[2]

    T = r00 + r11 + r22

    if T > 0:
        S = np.sqrt(T + 1.0) * 2
        t = 0.25 * S
        x = (r21 - r12) / S
        y = (r02 - r20) / S
        z = (r10 - r01) / S
    elif r00 > r11 and r00 > r22:
        S = np.sqrt(1.0 + r00 - r11 - r22) * 2
        t = (r21 - r12) / S
        x = 0.25 * S
        y = (r01 + r10) / S
        z = (r02 + r20) / S
    elif r11 > r22:
        S = np.sqrt(1.0 + r11 - r00 - r22) * 2
        t = (r02 - r20) / S
        x = (r01 + r10) / S
        y = 0.25 * S
        z = (r12 + r21) / S
    else:
        S = np.sqrt(1.0 + r22 - r00 - r11) * 2
        t = (r10 - r01) / S
        x = (r02 + r20) / S
        y = (r12 + r21) / S
        z = 0.25 * S

    return [t, x, y, z]

# ---------------
# TEST
# ---------------

# matrice correspondant à une rotation de 60° autour de Z
R = np.array([
    [0.5, -0.86603, 0],
    [0.86603, 0.5, 0],
    [0, 0, 1]
])

print("Quaternion retrouvé à partir de la matrice :")
print(rot_h(R))
