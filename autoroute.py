from tkinter import *
# On utilise le package Tkinter pour la création d'une GUI.

Fenetre = Tk()

#Déplacement continu de notre voiture
def deplacement():
    """La voiture se déplace. Lorsqu'elle quitte l'écran,
    elle revient par le bord opposé (Tore-like)."""

# On initialise les coordonnées du véhicule

    img_coords = canvas.coords(image)
    img_width = img_2.width()

# Si la voiture est dans le canevas, elle se déplace

    if img_coords[0] + img_width <= 1000:
        canvas.move(image,5,0)
        Fenetre.after(40, deplacement)
    else : # Sinon, on reboot les coordonnées et la fonction
        canvas.coords(image, 0, 50)
        deplacement()

# Image source
imgfile = 'Downloads/voiture.gif'
img = PhotoImage(file = imgfile)

# Le canevas
canvas = Canvas(Fenetre, width = 1000, height = 200, bg ='white')
canvas.pack(padx=10, pady=10)

img_2 = img
image = canvas.create_image(0 , 50,image = img_2)


deplacement()

Fenetre.mainloop()
