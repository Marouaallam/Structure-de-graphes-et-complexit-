from itertools import combinations

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
    print("\nReprésentation par liste d'adjacence du graphe:")
    for noeud, voisins in liste.items():
        print(f"{noeud}: {voisins}")
        
#affichage liste non oriente
def affichage_liste_nonoriente(elements,edges):
    liste = construire_liste_adjacence_nonoriente(elements,edges)
    print("\nReprésentation par liste d'adjacence du graphe:")
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

# Fonctions prédéfinies pour créer des exemples de graphes
def constGraph1():
    elements = ['A', 'B', 'C', 'D']
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
    return elements, edges

def constGraph2():
    elements = ['1', '2', '3', '4']
    edges = [('1', '2'), ('2', '3'), ('3', '4')]
    return elements, edges

def choix_graphe_type():
    print("\nChoix des graphe  :")
    print("1. ",constGraph1())
    print("2. ",constGraph2())
    choix = input("Choisis l'un des 2 graphe  (1 ou 2) : ")
    if choix == "1":
        return constGraph1()
    elif choix == "2":
        return constGraph2()
    else:
        print("Choix invalide. Veuillez réessayer.")
        return choix_graphe_type()
# Fonction pour choisir une action
def menu_principal():
    print("\nChoix de graphe :")
    print("1. Graphe orienté")
    print("2. Graphe non orienté")
    choix = input("Choisissez le type de graphe (1 ou 2) : ")
    return choix

def menu_fonctions():
    print("\nFonctions disponibles :")
    print("1. Afficher la liste d'adjacence")
    print("2. Calculer la densité du graphe")
    print("3. Vérifier si le graphe est complet")
    print("4. Trouver les chemins entre deux nœuds")
    print("5. Trouver un cycle hamiltonien")
    choix = input("Choisissez une fonction à appliquer (1-5) : ")
    return choix

# Exemple d'utilisation interactive
def main():
    print("\nMenu principal :")
    while True:
        elements, edges = choix_graphe_type()
        while True:
            choix_graphe = menu_principal()  # Appel du menu principal pour choisir le graphe
     
            if choix_graphe == '3':  # Si l'utilisateur choisit de quitter
                print("Au revoir !")
                return  # Quitter l'application

            if choix_graphe == '1':
                liste = construire_liste_adjacence_oriente(elements, edges)
                print("\nVous avez choisi un graphe orienté.")
            elif choix_graphe == '2':
                liste = construire_liste_adjacence_nonoriente(elements, edges)
                print("\nVous avez choisi un graphe non orienté.")

            while True:
                choix_fonction = menu_fonctions()  # Choix des fonctions à appliquer
                if choix_fonction == '1':
                    if choix_graphe == '1':
                        affichage_liste_oriente(elements, edges)
                    else:
                        affichage_liste_nonoriente(elements, edges)
                elif choix_fonction == '2':
                    densite = (
                        densite_graphe_oriente(elements, edges)
                        if choix_graphe == '1'
                        else densite_graphe_non_oriente(elements, edges)
                    )
                    print(f"Densité du graphe : {densite:.2f}")
                elif choix_fonction == '3':
                    if est_complet(liste):
                        print("Le graphe est complet.")
                    else:
                        print("Le graphe n'est pas complet.")
                elif choix_fonction == '4':
                    noeud_a = input("Entrez le nœud de départ : ")
                    noeud_b = input("Entrez le nœud d'arrivée : ")
                    chemins = tous_les_chemins(liste, noeud_a, noeud_b)
                    print(f"Tous les chemins entre {noeud_a} et {noeud_b} : {chemins}")
                elif choix_fonction == '5':
                    cycle = cycle_hamiltonien(liste)
                    if cycle:
                        print(f"Cycle hamiltonien trouvé : {cycle}")
                    else:
                        print("Aucun cycle hamiltonien trouvé.")
                else:
                    print("Choix invalide. Veuillez réessayer.")
                    continue

                continuer = input("Voulez-vous appliquer une autre fonction ? (y/n) : ").lower()
                if continuer == 'n':
                    break
                
            quitter = input("Voulez-vous choisir un autre graphe ? (y/n) : ").lower()
            if quitter != 'y':
                break
        quitter = input("Voulez-vous quitter l'application ? (y/n) : ").lower()
        if quitter == 'y':
            print("Au revoir !")
            break



# Lancer le programme
if __name__ == "__main__":
    main()
