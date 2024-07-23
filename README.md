# Moniteur de Vitesse de Frappe

Ce projet est une application Tkinter permettant de surveiller et d'afficher la vitesse de frappe en mots par minute (WPM). Elle inclut un graphique en temps réel, un mode overlay et des options de personnalisation.

## Fonctionnalités

- Affichage de la vitesse de frappe en WPM
- Graphique en temps réel de l'évolution de la vitesse de frappe
- Mode overlay avec options de personnalisation (taille de la police, couleur du texte, position)
- Sauvegarde et chargement des paramètres de l'utilisateur
- Profil de l'utilisateur affichant les statistiques de vitesse moyenne et maximale

## Prérequis

- Python 3.x
- Bibliothèques Python : `tkinter`, `PIL` (Pillow), `matplotlib`, `numpy`, `keyboard`

## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/jeandemalet/WPM-Float-Count-Graph
    ```

2. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Lancez l'application :
    ```bash
    python moniteur_vitesse_frappe.py
    ```

## Utilisation

### Interface Principale

- **Vitesse de frappe** : La vitesse de frappe actuelle en WPM est affichée en haut à gauche.
- **Bouton Overlay** : Active ou désactive le mode overlay.
- **Bouton Paramètres** : Ouvre la fenêtre de paramètres pour personnaliser l'affichage.
- **Bouton Profil** : Ouvre la fenêtre de profil pour afficher les statistiques de vitesse moyenne et maximale.

### Paramètres

La fenêtre des paramètres permet de personnaliser :
- La taille de la police du texte overlay.
- La couleur du texte overlay.
- La couleur du graphique.
- La position de l'overlay sur l'écran.

### Profil

La fenêtre de profil affiche les statistiques suivantes :
- Vitesse moyenne en WPM.
- Vitesse maximale en WPM.

## Sauvegarde des Paramètres

Les paramètres personnalisés sont sauvegardés dans un fichier `settings.json` dans le répertoire de l'application. Lors du lancement, ces paramètres sont automatiquement chargés pour restaurer la configuration précédente.

## Dépendances

Assurez-vous d'avoir les bibliothèques suivantes installées :

```python
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
```

## Contribuer

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations ou des bugs à signaler, veuillez ouvrir une issue ou soumettre une pull request.

## License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

---

## Contact

Pour toute question ou commentaire, veuillez contacter jeandemalet@gmail.com