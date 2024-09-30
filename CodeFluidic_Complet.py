#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 19:11:58 2024

@author: maximepoinsot
"""
import tkinter as tk
from queue import PriorityQueue
from PIL import Image
import time

class GridInterfaceTkinter:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = 30
        self.selected_points_green = []  # Points verts sélectionnés
        self.selected_points_red = []    # Points rouges sélectionnés
        self.obstacles = set()  # Obstacles infranchissables
        self.selecting_green = True  # Indique si l'utilisateur sélectionne des points verts ou rouges

        # Créer la fenêtre Tkinter
        self.root = tk.Tk()
        self.root.title("Grille interactive : Sélection et chemins fluidiques")

        # Créer le canvas pour la grille
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="white")
        self.canvas.pack()

        # Dessiner la grille
        self.draw_grid()

        # Créer les boutons
        selection_button = tk.Button(self.root, text="Sélection", command=self.toggle_selection_mode)
        selection_button.pack()

        validate_button = tk.Button(self.root, text="Valider", command=self.validate_selection)
        validate_button.pack()

        finish_button = tk.Button(self.root, text="Terminer", command=self.finish_and_save)
        finish_button.pack()

        reset_button = tk.Button(self.root, text="Réinitialiser", command=self.reset_grid)
        reset_button.pack()

        obstacle_button = tk.Button(self.root, text="Mode Obstacle", command=self.set_obstacle_mode)
        obstacle_button.pack()

        clear_obstacle_button = tk.Button(self.root, text="Effacer Obstacles", command=self.clear_obstacles)
        clear_obstacle_button.pack()

        self.root.mainloop()

    def draw_grid(self):
        # Dessiner la grille avec des carrés
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="white")

        # Ajouter des cercles gris dans les cellules (X, 2) à (X, 29) sur les lignes X = 5 à 11
        for x in range(5, 12):
            for y in range(2, min(30, self.cols)):
                x1 = y * self.cell_size + self.cell_size // 4
                y1 = x * self.cell_size + self.cell_size // 4
                x2 = x1 + self.cell_size // 2
                y2 = y1 + self.cell_size // 2
                self.canvas.create_oval(x1, y1, x2, y2, outline="gray", width=2, tags=f"circle_{x}_{y}")

                # Associer un clic à chaque cercle
                self.canvas.tag_bind(f"circle_{x}_{y}", "<Button-1>", lambda event, row=x, col=y: self.on_click(row, col))

    def toggle_selection_mode(self):
        # Activer le mode de sélection (vert d'abord)
        self.selecting_green = True
        print("Mode de sélection activé : vert d'abord")

    def set_obstacle_mode(self):
        self.selecting_green = None  # Désactiver la sélection de points
        print("Mode obstacle activé")

    def on_click(self, row, col):
        if self.selecting_green is None:
            # Ajouter un obstacle
            self.add_obstacle(row, col)
        else:
            if self.selecting_green:
                # Sélectionner un point vert
                self.add_green_point(row, col)
            else:
                # Sélectionner un point rouge
                self.add_red_point(row, col)

    def add_green_point(self, row, col):
        if (row, col) in self.selected_points_green or (row, col) in self.selected_points_red or (row, col) in self.obstacles:
            print(f"Impossible de sélectionner ce point vert : ({row}, {col})")
            return
        x1 = col * self.cell_size + self.cell_size // 4
        y1 = row * self.cell_size + self.cell_size // 4
        x2 = x1 + self.cell_size // 2
        y2 = y1 + self.cell_size // 2
        self.canvas.create_oval(x1, y1, x2, y2, outline="green", width=2)

        # Dessiner une demi-ligne verte vers la gauche
        x1_line = col * self.cell_size + self.cell_size // 2
        y1_line = row * self.cell_size + self.cell_size // 2
        x2_line = (col - 1) * self.cell_size + self.cell_size // 2
        self.canvas.create_line(x1_line, y1_line, x2_line, y1_line, fill="green", width=2)

        self.selected_points_green.append((row, col))
        print(f"Point vert sélectionné : ({row}, {col})")

        # Basculer vers la sélection de points rouges
        self.selecting_green = False

    def add_red_point(self, row, col):
        if (row, col) in self.selected_points_red or (row, col) in self.selected_points_green or (row, col) in self.obstacles:
            print(f"Impossible de sélectionner ce point rouge : ({row}, {col})")
            return
        x1 = col * self.cell_size + self.cell_size // 4
        y1 = row * self.cell_size + self.cell_size // 4
        x2 = x1 + self.cell_size // 2
        y2 = y1 + self.cell_size // 2
        self.canvas.create_oval(x1, y1, x2, y2, outline="red", width=2)

        # Dessiner une demi-ligne rouge vers la droite
        x1_line = col * self.cell_size + self.cell_size // 2
        y1_line = row * self.cell_size + self.cell_size // 2
        x2_line = (col + 1) * self.cell_size + self.cell_size // 2
        self.canvas.create_line(x1_line, y1_line, x2_line, y1_line, fill="red", width=2)

        self.selected_points_red.append((row, col))
        print(f"Point rouge sélectionné : ({row}, {col})")

        # Basculer vers la sélection de points verts
        self.selecting_green = True

    def add_obstacle(self, row, col):
        # Vérifier que l'obstacle n'est pas déjà un point sélectionné
        if (row, col) in self.selected_points_green or (row, col) in self.selected_points_red:
            print(f"Impossible d'ajouter un obstacle sur un point sélectionné : ({row}, {col})")
            return

        # Ajouter l'obstacle
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Dessiner une croix rouge pour l'obstacle
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags=f"obstacle_{row}_{col}")
        self.canvas.create_line(x1, y2, x2, y1, fill="red", width=2, tags=f"obstacle_{row}_{col}")

        # Ajouter l'obstacle à la liste
        self.obstacles.add((row, col))
        print(f"Obstacle ajouté : ({row}, {col})")

    def clear_obstacles(self):
        # Effacer les obstacles de la grille
        self.canvas.delete("all")
        self.obstacles.clear()
        self.draw_grid()
        print("Tous les obstacles ont été effacés")

    def validate_selection(self):
        if len(self.selected_points_green) != len(self.selected_points_red):
            print("Le nombre de points verts doit être égal au nombre de points rouges !")
            return

        # Tracer les chemins verts en direct, priorité à la ligne 4
        self.draw_paths_live(self.selected_points_green, "green", (0, 16), (4, 16))

        # Ajouter le chemin vert comme obstacle
        for point in self.selected_points_green:
            self.obstacles.add(point)

        # Tracer les chemins rouges en direct, priorité à la ligne 12
        self.draw_paths_live(self.selected_points_red, "red", (17, 16), (12, 16))

    def draw_paths_live(self, points, color, target, intermediate_point):
        # Tracer le chemin en fonction des points sélectionnés, en direct avec priorité pour la ligne
        grid = self.create_grid(self.rows, self.cols)

        # Ajouter les obstacles comme des cases infranchissables
        for (r, c) in self.obstacles:
            grid[r][c] = 1

        # Ajouter les points sélectionnés comme des obstacles pour éviter le chevauchement
        for (r, c) in self.selected_points_green:
            grid[r][c] = 1
        for (r, c) in self.selected_points_red:
            grid[r][c] = 1

        # Dessiner les chemins pour chaque point avec priorité sur la ligne
        for point in points:
            if color == "green":
                # Priorité pour atteindre la ligne 4 d'abord pour les chemins verts
                path_to_line_4 = self.shortest_path(grid, (point[0], point[1] - 1), (4, point[1]))
                # Ensuite aller de la ligne 4 au point (4, 16)
                path_to_intermediate = self.shortest_path(grid, (4, point[1]), intermediate_point)
                # Finalement aller du point (4, 16) à la cible (0, 16)
                path_to_target = self.shortest_path(grid, intermediate_point, target)

                # Dessiner les chemins verts
                if path_to_line_4:
                    self.animate_path(path_to_line_4, color)
                if path_to_intermediate:
                    self.animate_path(path_to_intermediate, color)
                if path_to_target:
                    self.animate_path(path_to_target, color)

            elif color == "red":
                # Priorité pour atteindre la ligne 12 d'abord pour les chemins rouges
                path_to_line_12 = self.shortest_path(grid, (point[0], point[1] + 1), (12, point[1]))
                # Ensuite aller de la ligne 12 au point (12, 16)
                path_to_intermediate = self.shortest_path(grid, (12, point[1]), intermediate_point)
                # Finalement aller du point (12, 16) à la cible (17, 16)
                path_to_target = self.shortest_path(grid, intermediate_point, target)

                # Dessiner les chemins rouges
                if path_to_line_12:
                    self.animate_path(path_to_line_12, color)
                if path_to_intermediate:
                    self.animate_path(path_to_intermediate, color)
                if path_to_target:
                    self.animate_path(path_to_target, color)

    def animate_path(self, path, color):
        # Animer le tracé du chemin
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            x1 = c1 * self.cell_size + self.cell_size // 2
            y1 = r1 * self.cell_size + self.cell_size // 2
            x2 = c2 * self.cell_size + self.cell_size // 2
            y2 = r2 * self.cell_size + self.cell_size // 2

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
            self.root.update()
            time.sleep(0.05)

    def create_grid(self, rows, cols):
        return [[0] * cols for _ in range(rows)]

    def shortest_path(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])
        queue = PriorityQueue()
        queue.put((0, start, None))  # Ajout d'une direction initiale None
        visited = set()
        parent = {start: (None, None)}  # (parent, direction d'arrivée)

        while not queue.empty():
            current_distance, current, direction_from = queue.get()
            if current == end:
                break
            visited.add(current)

            # Mouvement possible (haut, bas, gauche, droite)
            for dr, dc, direction in [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]:
                r, c = current[0] + dr, current[1] + dc
                if 0 <= r < rows and 0 <= c < cols and (r, c) not in visited and grid[r][c] == 0:
                    # Calculer une pénalité pour les virages
                    turn_penalty = 0
                    if direction_from is not None and direction_from != direction:
                        turn_penalty = 1  # Ajustez cette valeur pour changer la pénalité

                    # Calculer la distance totale avec la pénalité
                    distance = current_distance + 1 + turn_penalty
                    queue.put((distance, (r, c), direction))
                    visited.add((r, c))
                    parent[(r, c)] = (current, direction)

        if end not in parent:
            return None

        # Reconstruire le chemin
        path = []
        step = end
        while step:
            path.append(step)
            step = parent[step][0]
        path.reverse()

        return path

    def finish_and_save(self):
        print("Enregistrement de l'image...")
        self.canvas.postscript(file="grid_paths.ps", colormode='color')
        img = Image.open("grid_paths.ps")
        img.save("grid_paths.png")
        self.root.quit()

    def reset_grid(self):
        self.canvas.delete("all")
        self.selected_points_green = []
        self.selected_points_red = []
        self.obstacles = set()
        self.draw_grid()

# Lancer l'interface interactive Tkinter
GridInterfaceTkinter(18, 33)







