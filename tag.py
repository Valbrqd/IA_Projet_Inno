import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import json


IMAGE_FOLDER = 'test_images'
ANNOTATION_FILE = 'annotations.json'

annotations = {}
current_tags = set() 

def load_annotations():
    global annotations
    if os.path.exists(ANNOTATION_FILE):
        with open(ANNOTATION_FILE, 'r') as f:
            annotations = json.load(f)
    else:
        annotations = {}

def save_annotations():
    with open(ANNOTATION_FILE, 'w') as f:
        json.dump(annotations, f)

def toggle_tag(tag):
    """Ajoute ou retire un tag et met à jour l'affichage des tags sélectionnés."""
    if tag in current_tags:
        current_tags.remove(tag)
    else:
        current_tags.add(tag)
    update_selected_tags_display()

def update_selected_tags_display():
    """Met à jour le label pour afficher les tags sélectionnés."""
    selected_tags_label.config(text="Tags sélectionnés : " + ", ".join(current_tags))

def finalize_annotations():
    """Enregistre les tags et passe à l'image suivante ou affiche un message de fin."""
    global current_image_path
    annotations[current_image_path] = list(current_tags)
    save_annotations()
    current_tags.clear()  
    load_next_image()
    update_selected_tags_display() 

def load_next_image():
    """Charge la prochaine image ou affiche un message de fin si toutes sont annotées."""
    global current_image_path, image_label
    try:
        current_image_path = next(image_paths)
        img = Image.open(current_image_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
    except StopIteration:
        messagebox.showinfo("Fin du traitement", "Toutes les images ont été annotées !")
        save_annotations()
        root.destroy()


root = Tk()
root.title("Annotation d'Images de Peau")


image_paths = iter([os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) if f.endswith('.jpeg')])

image_label = Label(root)
image_label.pack()


button_frame = Frame(root)
button_frame.pack(pady=10)


for tag in ["Sèche", "Normale", "Grasse"]:
    button = Button(button_frame, text=tag, command=lambda t=tag: toggle_tag(t))
    button.pack(side=LEFT, padx=5)


Button(root, text="Valider les tags", command=finalize_annotations).pack(pady=10)


selected_tags_label = Label(root, text="Tags sélectionnés : ")
selected_tags_label.pack(pady=10)

load_annotations()
load_next_image()
root.mainloop()