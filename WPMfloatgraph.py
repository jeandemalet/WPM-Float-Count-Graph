import tkinter as tk
from tkinter import ttk, colorchooser
from PIL import Image, ImageDraw, ImageTk, ImageFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import keyboard
import time
import json
import os
from PIL import ImageGrab

class TypingSpeedMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Moniteur de vitesse de frappe")
        self.root.geometry("800x600")
        self.root.attributes('-topmost', True)

        self.words = 0
        self.last_key_press_time = time.time()
        self.start_time = time.time()
        self.speeds = deque(maxlen=60)
        self.overlay_mode = True
        self.overlay_font_size = 24
        self.overlay_font_color = "black"
        self.graph_color = "blue"
        self.data_duration = 60

        self.avg_speed = 0
        self.max_speed = 0
        self.overlay_position = [10, 10]  # Position par défaut en haut à gauche

        self.load_settings()

        # Frame for WPM and buttons
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.speed_label = ttk.Label(self.top_frame, text="0 WPM", font=("Arial", 24))
        self.speed_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.overlay_button = ttk.Button(self.top_frame, text="Désactiver l'overlay", command=self.toggle_overlay, style='Large.TButton')
        self.overlay_button.pack(side=tk.LEFT, padx=10)

        self.settings_button = ttk.Button(self.top_frame, text="Paramètres", command=self.open_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        self.profile_button = ttk.Button(self.top_frame, text="Profil", command=self.open_profile)
        self.profile_button.pack(side=tk.LEFT, padx=10)

        # Graph area
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 14))

        keyboard.on_press(self.key_press)

        self.create_overlay()

        self.update_speed()
        self.root.mainloop()

    def key_press(self, event):
        if event.name == 'space':
            self.words += 1
        self.last_key_press_time = time.time()

    def create_overlay(self):
        if hasattr(self, 'overlay'):
            self.overlay.destroy()
        
        self.overlay = tk.Toplevel(self.root)
        self.overlay.geometry(f"+{self.overlay_position[0]}+{self.overlay_position[1]}")
        self.overlay.overrideredirect(True)
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-transparentcolor', 'gray')
        self.overlay_label = tk.Label(self.overlay, bg='gray')
        self.overlay_label.pack()

    def toggle_overlay(self):
        self.overlay_mode = not self.overlay_mode
        if self.overlay_mode:
            self.overlay_button.config(text="Désactiver l'overlay")
            self.create_overlay()
        else:
            self.overlay_button.config(text="Activer l'overlay")
            if hasattr(self, 'overlay'):
                self.overlay.destroy()

    def update_speed(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        time_since_last_key = current_time - self.last_key_press_time
        
        if time_since_last_key > 3:
            self.words = 0
            self.start_time = current_time

        minutes = elapsed_time / 60
        wpm = int(self.words / minutes) if minutes > 0 else 0

        if time_since_last_key > 3:
            wpm = 0

        self.speeds.append(wpm)
        
        if self.overlay_mode:
            self.update_overlay(wpm)
        self.speed_label.config(text=f"{wpm} WPM")
        self.ax.clear()
        self.ax.plot(list(self.speeds), linestyle='-', marker='o', color=self.graph_color, label='Vitesse de frappe')
        self.ax.fill_between(range(len(self.speeds)), list(self.speeds), color=self.graph_color, alpha=0.3)
        
        self.ax.set_title("Évolution de la vitesse de frappe")
        self.ax.set_xlabel("Temps (secondes)")
        self.ax.set_ylabel("Mots par minute")
        self.ax.set_ylim(bottom=0)
        self.ax.set_xlim(0, self.data_duration)
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

        # Update profile statistics
        self.avg_speed = sum(self.speeds) / len(self.speeds) if self.speeds else 0
        self.max_speed = max(self.max_speed, wpm)

        self.root.after(1000, self.update_speed)

    def update_overlay(self, wpm):
        overlay_width = 250
        overlay_height = 130

        screen = Image.new('RGBA', (overlay_width, overlay_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(screen)
        
        # Dessiner le graphique superposé
        graph_width = 180
        graph_height = 40
        graph_x = 20
        graph_y = overlay_height - graph_height - 20

        max_wpm = max(self.speeds) if self.speeds else 1
        min_wpm = min(self.speeds) if self.speeds else 0

        points = []
        for i, speed in enumerate(self.speeds):
            x = graph_x + int(i * (graph_width / len(self.speeds)))
            y = graph_y + graph_height - int((speed - min_wpm) / (max_wpm - min_wpm + 1) * graph_height)
            points.append((x, y))

        if points:
            points = [(graph_x, graph_y + graph_height)] + points + [(graph_x + graph_width, graph_y + graph_height)]
            draw.polygon(points, fill=self.graph_color, outline=self.graph_color)
        
        # Dessiner le texte avec un contour blanc
        text = f"{wpm} WPM"
        font_size = self.overlay_font_size
        font = ImageFont.truetype("arialbd.ttf", font_size)
        
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_position = (overlay_width // 2 - text_width // 2, (overlay_height - graph_height) // 2 - text_height // 2)
        
        # Contour blanc pour une meilleure lisibilité
        draw.text((text_position[0] - 1, text_position[1] - 1), text, fill='white', font=font)
        draw.text((text_position[0] + 1, text_position[1] - 1), text, fill='white', font=font)
        draw.text((text_position[0] - 1, text_position[1] + 1), text, fill='white', font=font)
        draw.text((text_position[0] + 1, text_position[1] + 1), text, fill='white', font=font)
        
        draw.text(text_position, text, fill=self.overlay_font_color, font=font)
        
        # Convertir l'image en format PhotoImage pour Tkinter
        tk_image = ImageTk.PhotoImage(screen)
        self.overlay_label.config(image=tk_image)
        self.overlay_label.image = tk_image

    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Paramètres")
        
        # Utilisation des valeurs entières pour éviter les erreurs de géométrie
        width = int(self.root.winfo_screenwidth() * 0.9)
        height = int(self.root.winfo_screenheight() * 0.9)
        self.settings_window.geometry(f"{width}x{height}+50+50")
        self.settings_window.attributes('-topmost', True)
        self.settings_window.configure(bg='#f0f0f0')  # Fond gris clair

        self.settings_frame = ttk.Frame(self.settings_window, padding=20, style='TFrame')
        self.settings_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.settings_frame, text="Taille de la police:", font=("Arial", 16)).pack(pady=10)
        font_size_spinbox = tk.Spinbox(self.settings_frame, from_=10, to_=72, command=self.update_font_size, font=("Arial", 14))
        font_size_spinbox.pack(pady=10)
        font_size_spinbox.delete(0, tk.END)
        font_size_spinbox.insert(0, self.overlay_font_size)
        
        ttk.Label(self.settings_frame, text="Couleur du texte:", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.settings_frame, text="Choisir la couleur du texte", command=self.choose_color).pack(pady=10)
        
        ttk.Label(self.settings_frame, text="Couleur du graphique:", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self.settings_frame, text="Choisir la couleur du graphique", command=self.choose_graph_color).pack(pady=10)
        
        ttk.Label(self.settings_frame, text="Position de l'overlay:", font=("Arial", 16)).pack(pady=10)
        self.position_label = ttk.Label(self.settings_frame, text=f"Haut: {self.overlay_position[1]}px, Gauche: {self.overlay_position[0]}px", font=("Arial", 14))
        self.position_label.pack(pady=10)

        ttk.Button(self.settings_frame, text="Repositionner l'overlay", command=self.reposition_overlay).pack(pady=10)

    def update_font_size(self):
        self.overlay_font_size = int(self.settings_window.winfo_children()[1].get())

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choisir la couleur du texte")
        if color_code:
            self.overlay_font_color = color_code[1]

    def choose_graph_color(self):
        color_code = colorchooser.askcolor(title="Choisir la couleur du graphique")
        if color_code:
            self.graph_color = color_code[1]

    def reposition_overlay(self):
        self.reposition_window = tk.Toplevel(self.root)
        self.reposition_window.title("Repositionner l'overlay")
        self.reposition_window.attributes('-topmost', True)
        self.reposition_window.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.reposition_window.configure(bg='gray')
        
        # Capture d'écran pour l'aperçu
        screen_capture = ImageGrab.grab()
        screen_photo = ImageTk.PhotoImage(screen_capture)
        tk.Label(self.reposition_window, image=screen_photo).pack(fill=tk.BOTH, expand=True)
        self.reposition_window.image = screen_photo
        
        # Aperçu de l'overlay
        overlay_preview = tk.Toplevel(self.reposition_window)
        overlay_preview.title("Aperçu de l'Overlay")
        overlay_preview.geometry(f"300x150+{self.overlay_position[0]}+{self.overlay_position[1]}")
        overlay_preview.configure(bg='gray')
        
        preview_canvas = tk.Canvas(overlay_preview, width=300, height=150, bg='gray')
        preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        preview_img = Image.new('RGBA', (300, 150), (255, 255, 255, 0))
        draw = ImageDraw.Draw(preview_img)
        text = f"{self.speed_label.cget('text')}"
        font = ImageFont.truetype("arialbd.ttf", 24)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = (150 - text_width // 2, 75 - text_height // 2)
        
        draw.text(text_position, text, fill=self.overlay_font_color, font=font)
        preview_photo = ImageTk.PhotoImage(preview_img)
        preview_canvas.create_image(150, 75, image=preview_photo)
        overlay_preview.image = preview_photo
        
        # Déplacement du cadre
        reposition_frame = ttk.Frame(self.reposition_window, width=200, height=100, relief='solid', style='TFrame')
        reposition_frame.place(x=self.overlay_position[0], y=self.overlay_position[1])
        
        reposition_frame.bind('<B1-Motion>', self.on_reposition_drag)
        reposition_frame.bind('<ButtonRelease-1>', self.on_reposition_drop)

    def on_reposition_drag(self, event):
        x = self.reposition_window.winfo_pointerx() - self.reposition_window.winfo_rootx()
        y = self.reposition_window.winfo_pointery() - self.reposition_window.winfo_rooty()
        self.reposition_window.geometry(f"+{x}+{y}")

    def on_reposition_drop(self, event):
        new_x = self.reposition_window.winfo_x()
        new_y = self.reposition_window.winfo_y()
        self.overlay_position = [new_x, new_y]
        self.overlay.geometry(f"+{new_x}+{new_y}")

        self.reposition_window.destroy()

    def open_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Profil")
        profile_window.geometry("400x300")

        ttk.Label(profile_window, text=f"Vitesse moyenne: {self.avg_speed:.2f} WPM", font=("Arial", 16)).pack(pady=10)
        ttk.Label(profile_window, text=f"Vitesse maximale: {self.max_speed} WPM", font=("Arial", 16)).pack(pady=10)

    def load_settings(self):
        settings_file = 'settings.json'
        if os.path.isfile(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                self.overlay_font_size = settings.get('overlay_font_size', 24)
                self.overlay_font_color = settings.get('overlay_font_color', 'black')
                self.graph_color = settings.get('graph_color', 'blue')

if __name__ == "__main__":
    TypingSpeedMonitor()
