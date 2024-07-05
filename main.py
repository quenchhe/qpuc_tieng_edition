import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# Initialize pygame for sound
pygame.init()

# Load buzzer sound
buzzer_sound = pygame.mixer.Sound('data\media\sound\\buzzer.mp3')

# Set up main application window
root = tk.Tk()
root.title("Game Show")
root.geometry("1920x1080")

# Global variables
contestants = {}
buzzed = None

# Function to handle buzzer press
def buzz(contestant):
    global buzzed
    if buzzed is None:
        buzzed = contestant
        buzzer_sound.play()
        for c in contestants:
            if c == contestant:
                contestants[c]['label'].config(bg='red')
                blink(contestants[c]['label'])
            else:
                contestants[c]['button'].config(state=tk.DISABLED)

def blink(label):
    def toggle_color():
        current_color = label.cget("bg")
        next_color = "red" if current_color == "white" else "white"
        label.config(bg=next_color)
        label.after(500, toggle_color)
    toggle_color()

# Function to reset buzzers
def reset_buzzers():
    global buzzed
    buzzed = None
    for c in contestants:
        contestants[c]['label'].config(bg='white')
        contestants[c]['button'].config(state=tk.NORMAL)

# Load and display background image
background_image = Image.open('data\media\images\\background.png')
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Display contestant images
def display_contestant_images(names):
    for i, name in enumerate(names):
        image = Image.open(f'data\media\images\players\{name.lower()}.png')  # Assuming you have images named alice.jpg, bob.jpg, etc.
        image = image.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.grid(row=i, column=0, padx=20, pady=20)
        button = tk.Button(root, text=f"Buzz {name}", font=("Arial", 18), command=lambda n=name: buzz(n))
        button.grid(row=i, column=1, padx=20, pady=20)
        contestants[name] = {'label': label, 'button': button}

# Adjust the main window dimensions and placement
root.geometry("1920x1080")

# Sample contestants
contestant_names = ["Shulk", "Melia", "Kino", "Nene"]
display_contestant_images(contestant_names)

# Mapping of keys to contestants
key_to_contestant = {'a': "Shulk", 'z': "Melia", 'e': "Kino", 'r': "Nene"}

def on_key_press(event):
    if event.char in key_to_contestant:
        buzz(key_to_contestant[event.char])
    elif event.char == 'w':  # 'r' key to reset buzzers
        reset_buzzers()

# Bind key press event
root.bind("<Key>", on_key_press)

# Add reset button
reset_button = tk.Button(root, text="Reset Buzzers", font=("Arial", 18), command=reset_buzzers)
reset_button.grid(row=0, column=2, padx=20, pady=20)

# Start the application
root.mainloop()
