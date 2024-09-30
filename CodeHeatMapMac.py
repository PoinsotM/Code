#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 22:33:38 2024

@author: maximepoinsot
"""

import matplotlib.pyplot as plt
import numpy as np

# Chemin vers le fichier texte (modifié pour macOS)
chemin_fichier = '/Users/maximepoinsot/Desktop/Paper/PapierMicroRail/Prisms/ShollMicroRAIL/HeatMap/GFP/DIV21/Overlap.txt'

# Charger la matrice à partir du fichier texte
matrice_valeurs = np.loadtxt(chemin_fichier, dtype=int)

def etaler_valeurs(valeurs, etalement):
    result = np.zeros((valeurs.shape[0], (valeurs.shape[1] - 1) * etalement + 1))

    for i in range(valeurs.shape[0]):
        for j in range(valeurs.shape[1] - 1):
            debut = valeurs[i, j]
            fin = valeurs[i, j + 1]

            # Calculer les valeurs intermédiaires
            intermediaires = np.linspace(debut, fin, etalement + 1, endpoint=True)[:-1]

            # Assigner les valeurs à la matrice résultante
            debut_index = j * etalement
            fin_index = (j + 1) * etalement
            result[i, debut_index:fin_index] = intermediaires

        # Ajouter la dernière valeur de la ligne
        result[i, -1] = valeurs[i, -1]

    return result

# Valeur d'étalement (peut être ajustée)
etalement = 100

# Obtenir la matrice étagée
matrice_etapee = etaler_valeurs(matrice_valeurs, etalement)

# Régler la taille de la figure (20,6)->Cortex, (6,6)->Overlap
plt.figure(figsize=(6, 6))

# Définir les valeurs minimales et maximales pour la colormap
vmin = 0
vmax = 255

# Créer une heatmap avec la nouvelle matrice
plt.imshow(matrice_etapee, cmap='inferno', aspect='auto', vmin=vmin, vmax=vmax)
plt.colorbar(label=f'Valeurs étagées (étalement = {etalement})')

# Afficher la figure
plt.show()
