from itertools import combinations
def construire_liste_adjacence_nonoriente(elements,edges):
    liste = {i: [] for i in elements}#initialisation d'un dictionaire
    for u, v in edges:
        #ajouter la liste des successeurs pour chaque nœud
        liste[u].append(v)
        liste[v].append(u)
        
    return liste


#liste graphe oriente
def construire_liste_adjacence_oriente(elements,edges):
    liste = {i: [] for i in elements}#initialisation d'un dictionaire
    for u, v in edges:
        #ajouter la liste des successeurs pour chaque nœud
        liste[u].append(v) 
    return liste
  
#affichage liste oriente
def affichage_liste_oriente(elements,edges):
    liste = construire_liste_adjacence_oriente(elements,edges)
    print("\nReprésentation par liste d'adjacence de G3:")
    for noeud, voisins in liste.items():
        print(f"{noeud}: {voisins}")
        
#affichage liste non oriente
def affichage_liste_nonoriente(elements,edges):
    liste = construire_liste_adjacence_nonoriente(elements,edges)
    print("\nReprésentation par liste d'adjacence de G3:")
    for noeud, voisins in liste.items():
        print(f"{noeud}: {voisins}")

# Calculer la densité du graphe
# La densité est le rapport entre le nombre d'arêtes existantes et le nombre maximal d'arêtes possibles.
def densite_graphe_non_oriente(elements, edges):
    n = len(elements)
    m = len(edges)
    if n > 1:
        return 2 * m / (n * (n - 1))  # Pour les graphes non orientés
    return 0

def densite_graphe_oriente(elements, edges):
    n = len(elements)
    m = len(edges)
    if n > 1:
        return m / (n * (n - 1))  # Pour les graphes orientés
    return 0

# Calculer le degré du graphe
# Le degré d'un nœud est le nombre de voisins pour un graphe non orienté.
# Pour un graphe orienté, on distingue le degré entrant et le degré sortant.
def degre_graphe(liste):
    """
    Calculer le degré de chaque nœud (nombre de voisins).
    Pour un graphe orienté, adapter pour les degrés entrants et sortants.
    """
    return {noeud: len(voisins) for noeud, voisins in liste.items()}

# Vérifier si le graphe est eulérien
# Un graphe est eulérien si tous ses nœuds ont un degré pair.
def est_eulerien(liste):
    """
    Vérifie si le graphe est eulérien.
    Applicable uniquement aux graphes non orientés.
    """
    degres = degre_graphe(liste)
    return all(degre % 2 == 0 for degre in degres.values())

def est_complet(liste):
    """
    Vérifie si le graphe est complet.
    Applicable aux graphes orientés et non orientés.
    """
    n = len(liste)
    return all(len(voisins) == n - 1 for voisins in liste.values())

# Trouver un sous-graphe complet maximal
# Cherche la plus grande "clique" (sous-ensemble de nœuds complètement connectés).
def sous_graphe_complet_maximal(liste):
    """
    Trouve un sous-graphe complet maximal (clique).
    Applicable aux graphes non orientés.
    """
    
    sous_graphes = []
    for k in range(len(liste), 0, -1):
        for combinaison in combinations(liste.keys(), k):
            print("combinaison",combinaison)
            sous_graphe = {noeud: [v for v in liste[noeud] if v in combinaison] for noeud in combinaison}
            print(sous_graphe)
            if est_complet(sous_graphe):
                sous_graphes.append(combinaison)
        if sous_graphes:
            return sous_graphes[0]
    return []

# Recherche de tous les chemins entre deux nœuds
def tous_les_chemins(liste, a, b, chemin=[]):
    """
    Trouve tous les chemins entre deux nœuds a et b.
    Applicable aux graphes orientés et non orientés.
    """
    chemin = chemin + [a]
    if a == b:
        return [chemin]
    if a not in liste:
        return []
    chemins = []
    for voisin in liste[a]:
        if voisin not in chemin:
            chemins += tous_les_chemins(liste, voisin, b, chemin)
    return chemins

def chemin_le_plus_court(liste, a, b):
    """
    Trouve le chemin le plus court entre deux nœuds en utilisant la fonction recherche_chemins.

    Arguments :
    liste -- Liste d'adjacence représentant le graphe.
    a -- Nœud de départ.
    b -- Nœud d'arrivée.

    Retourne :
    Le chemin le plus court sous forme de liste ou None si aucun chemin n'existe.
    """
    # Obtenir tous les chemins possibles entre `start` et `end`
    les_chemins = tous_les_chemins(liste, a, b)
    
    if not les_chemins:
        return None  # Aucun chemin n'existe

    # Trouver le chemin avec la longueur minimale
    chemin_court = min(les_chemins, key=len)
    return chemin_court

def trouver_tous_les_cycles(liste):
    """ Trouve tous les cycles dans un graphe. Applicable aux graphes orientés et non orientés. """
    
    def dfs(noeud, debut, visite, chemin):
        visite.add(noeud)
        chemin.append(noeud)

        for voisin in liste[noeud]:
            # Si le voisin est le nœud de départ et que le chemin est plus long que 2 (pour éviter un aller-retour)
            if voisin == debut and len(chemin) > 2:
                cycles.append(list(chemin))
            elif voisin not in visite:
                # Appel récursif pour explorer le voisin
                dfs(voisin, debut, visite, chemin)

        chemin.pop()  # Retirer le nœud actuel du chemin
        visite.remove(noeud)  # Marquer le nœud comme non visité après exploration

    cycles = []
    
    # Lancer la DFS pour chaque nœud
    for noeud in liste:
        dfs(noeud, noeud, set(), [])

    return cycles

def composantes_connexes(liste):
    """
    Trouve les composantes connexes dans un graphe non orienté.
    """
    def explorer(noeud, visite, composante):
        visite.add(noeud)
        composante.append(noeud)
        for voisin in liste[noeud]:
            if voisin not in visite:
                explorer(voisin, visite, composante)
    visite = set()
    composantes = []
    for noeud in liste:
        if noeud not in visite:
            composante = []
            explorer(noeud, visite, composante)
            composantes.append(composante)
    return composantes


def cycle_hamiltonien(graphe, chemin=None):
    """
    Vérifie et retourne un cycle hamiltonien dans un graphe si présent.

    Arguments :
    - graphe : dict, liste d'adjacence représentant un graphe non orienté.
    - chemin : list, le chemin courant (par défaut None).

    Retourne :
    - list : Un cycle hamiltonien s'il existe, sinon une liste vide.
    """
    if chemin is None:
        chemin = [list(graphe.keys())[0]]  # Commence par un nœud arbitraire

    # Si le chemin contient tous les sommets et revient au point de départ
    if len(chemin) == len(graphe) and chemin[0] in graphe[chemin[-1]]:
        return chemin

    # Exploration des voisins
    for voisin in graphe[chemin[-1]]:
        if voisin not in chemin:  # Éviter de revisiter les sommets
            cycle = cycle_hamiltonien(graphe, chemin + [voisin])
            if cycle:
                return cycle

    return []  # Aucun cycle trouvé




def contient_k_crique(liste, k):
    """
    Vérifie si le graphe contient une k-crique.
    Applicable aux graphes non orientés.
    """
    for combinaison in combinations(liste.keys(), k):
        sous_graphe = {noeud: [v for v in liste[noeud] if v in combinaison] for noeud in combinaison}
        if est_complet(sous_graphe):
            return True
    return False

import random
import time
from itertools import combinations

# Générer un graphe aléatoire
def generer_graphe_aleatoire(n, densite):
    """
    Génère un graphe non orienté avec `n` nœuds et une densité donnée.
    """
    elements = list(range(1, n + 1))
    edges = []
    max_edges = n * (n - 1) // 2  # Nombre maximal d'arêtes
    nb_edges = int(max_edges * densite)  # Nombre d'arêtes selon la densité
    while len(edges) < nb_edges:
        u, v = random.sample(elements, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return elements, edges

# Mesurer le temps pour vérifier un cycle hamiltonien
def mesure_temps_cycle_hamiltonien(elements, edges):
    liste = construire_liste_adjacence_nonoriente(elements, edges)
    debut = time.time()
    cycle_hamiltonien(liste)
    return time.time() - debut

# Mesurer le temps pour vérifier une k-clique
def mesure_temps_k_clique(elements, edges, k):
    liste = construire_liste_adjacence_nonoriente(elements, edges)
    debut = time.time()
    contient_k_crique(liste, k)
    return time.time() - debut

# Effectuer l'évaluation
def evaluation_experimentale():
    resultats = []
    tailles = [10, 20]  # Différentes tailles de graphe
    densites = [0.1, 0.25, 0.5, 0.75, 1.0]  # Différentes densités
    for n in tailles:
        for densite in densites:
            elements, edges = generer_graphe_aleatoire(n, densite)
            temps_hamiltonien = mesure_temps_cycle_hamiltonien(elements, edges)
            temps_k_clique = mesure_temps_k_clique(elements, edges, k=5)  # Exemple avec k=5
            resultats.append((n, densite, temps_hamiltonien, temps_k_clique))
    return resultats

# Afficher les résultats
def afficher_tableau(resultats):
    print(f"{'Nœuds':<10}{'Densité':<10}{'Temps Hamiltonien (s)':<25}{'Temps k-clique (s)':<20}")
    print("=" * 65)
    for n, densite, temps_hamiltonien, temps_k_clique in resultats:
        print(f"{n:<10}{densite:<10.2f}{temps_hamiltonien:<25.4f}{temps_k_clique:<20.4f}")

# Lancer l'évaluation et afficher les résultats
resultats = evaluation_experimentale()
afficher_tableau(resultats)




