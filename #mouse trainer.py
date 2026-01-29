import tkinter as tk
import random
import math
from tkinter import ttk

fenetre = tk.Tk()
fenetre.title("Mouse Trainer")

def centrer_fenetre(fenetre, largeur_fenetre, hauteur_fenetre):
    screen_width = fenetre.winfo_screenwidth()
    screen_height = fenetre.winfo_screenheight()
    x = (screen_width - largeur_fenetre) // 2
    y = 50
    fenetre.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x}+{y}")

# Frame pour les explications avec ronds
frame_explications = tk.Frame(fenetre)
frame_explications.pack(pady=10)

frame_rouge = tk.Frame(frame_explications)
frame_rouge.pack(side="left", padx=20)
canvas_rouge = tk.Canvas(frame_rouge, width=20, height=20, bg="white", highlightthickness=0)
canvas_rouge.create_oval(3, 3, 17, 17, fill="red", outline="black")
canvas_rouge.pack(side="left")
label_rouge = tk.Label(frame_rouge, text="= clic gauche", font=("Arial", 14))
label_rouge.pack(side="left")

frame_vert = tk.Frame(frame_explications)
frame_vert.pack(side="left", padx=20)
canvas_vert = tk.Canvas(frame_vert, width=20, height=20, bg="white", highlightthickness=0)
canvas_vert.create_oval(3, 3, 17, 17, fill="green", outline="black")
canvas_vert.pack(side="left")
label_vert = tk.Label(frame_vert, text="= clic droit", font=("Arial", 14))
label_vert.pack(side="left")

score = 0
label_score = tk.Label(fenetre, text=f"Score : {score}", font=("Arial", 14))
label_score.pack(pady=10)

label_temps = tk.Label(fenetre, text="Temps restant : -- s", font=("Arial", 14))
label_temps.pack(pady=10)

label_info_score = tk.Label(fenetre,
                            text="Score +1 si clic correct sur le cercle, sinon -1",
                            font=("Arial", 12))
label_info_score.pack(pady=10)

canvas = tk.Canvas(fenetre, width=300, height=300, bg="white")
canvas.pack()

label_choix = tk.Label(fenetre, text="Choisis la durée du jeu (secondes) :", font=("Arial", 12))
label_choix.pack(pady=(10, 0))

temps_choisi = tk.StringVar(value="30")
combo_temps = ttk.Combobox(fenetre, textvariable=temps_choisi, state="readonly",
                           values=["10", "15", "20", "25", "30"])
combo_temps.pack(pady=(0, 10))

bouton_start = tk.Button(fenetre, text="Démarrer", font=("Arial", 14))
bouton_restart = tk.Button(fenetre, text="Recommencer", font=("Arial", 14))
bouton_quitter = tk.Button(fenetre, text="Quitter", font=("Arial", 14))

# Affichage bouton démarrer et choix temps au lancement
bouton_start.pack(pady=10)
combo_temps.pack(pady=(0, 10))
label_choix.pack(pady=(10, 0))

couleur_actuelle = None
cercle_x = 0
cercle_y = 0
rayon = 30
temps_restant = 30

def creer_cercle():
    global couleur_actuelle, cercle_x, cercle_y
    canvas.delete("all")

    cercle_x = random.randint(rayon, 300 - rayon)
    cercle_y = random.randint(rayon, 300 - rayon)

    couleur_actuelle = random.choice(["green", "red"])

    canvas.create_oval(cercle_x - rayon, cercle_y - rayon, cercle_x + rayon, cercle_y + rayon,
                       fill=couleur_actuelle, outline="black")

def verifier_clic(event):
    global couleur_actuelle, score

    if temps_restant <= 0:
        return

    dist = math.sqrt((event.x - cercle_x) ** 2 + (event.y - cercle_y) ** 2)

    if dist <= rayon:
        bouton = event.num
        if (couleur_actuelle == "green" and bouton == 3) or (couleur_actuelle == "red" and bouton == 1):
            score += 1
        else:
            score -= 1
        label_score.config(text=f"Score : {score}")
        creer_cercle()

def decompte():
    global temps_restant
    if temps_restant > 0:
        temps_restant -= 1
        label_temps.config(text=f"Temps restant : {temps_restant} s")
        fenetre.after(1000, decompte)
    else:
        label_temps.config(text="Temps écoulé !")
        canvas.unbind("<Button-1>")
        canvas.unbind("<Button-3>")
        label_info_score.config(text=f"Fin du jeu ! Score final : {score}")

        bouton_restart.pack(pady=5)
        bouton_quitter.pack(pady=5)

        combo_temps.pack(pady=(0, 10))
        label_choix.pack(pady=(10, 0))
        bouton_start.pack(pady=10)

def demarrer_jeu():
    global score, temps_restant
    try:
        temps_restant = int(temps_choisi.get())
    except ValueError:
        temps_restant = 30

    score = 0
    label_score.config(text=f"Score : {score}")
    label_info_score.config(text="Score +1 si clic correct sur le cercle, Sinon -1")
    label_temps.config(text=f"Temps restant : {temps_restant} s")

    bouton_start.pack_forget()
    combo_temps.pack_forget()
    label_choix.pack_forget()

    bouton_restart.pack_forget()
    bouton_quitter.pack_forget()

    creer_cercle()
    canvas.bind("<Button-1>", verifier_clic)
    canvas.bind("<Button-3>", verifier_clic)
    decompte()

def quitter():
    fenetre.destroy()

bouton_start.config(command=demarrer_jeu)
bouton_restart.config(command=demarrer_jeu)
bouton_quitter.config(command=quitter)

fenetre.update()  # Calcul automatique de la taille selon widgets

largeur = fenetre.winfo_width()
hauteur = fenetre.winfo_height()

centrer_fenetre(fenetre, largeur, hauteur)

fenetre.mainloop()
