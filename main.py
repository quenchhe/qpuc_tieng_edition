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
root.title("QPUC Tieng Edition")
root.geometry("1920x1080")

# Global variables
contestants = {}
buzzed = None

def buzz(contestant):
    global buzzed
    if buzzed is None and not(contestants[contestant]['has_buzzed']):
        buzzed = contestant
        buzzer_sound.play()
        for c in contestants:
            if c == contestant:
                contestants[c]['label'].config(bg='red')
                start_blinking(contestants[c]['label'])
                contestants[c]['has_buzzed'] = True
            else:
                contestants[c]['button'].config(state=tk.DISABLED)

def start_blinking(label):
    def toggle_color():
        current_color = label.cget("bg")
        next_color = "red" if current_color == "white" else "white"
        label.config(bg=next_color)
        global blink_id
        blink_id = label.after(500, toggle_color)
    toggle_color()

def stop_blinking():
    global blink_id
    if blink_id:
        root.after_cancel(blink_id)
        blink_id = None

# Function to reset buzzers
def reset_buzzers():
    global buzzed
    buzzed = None
    stop_blinking()
    for c in contestants:
        contestants[c]['has_buzzed'] = False
        contestants[c]['label'].config(bg='white')
        if contestants[c]['button'].cget('state') != tk.DISABLED:
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
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.grid(row=i, column=0, padx=20, pady=20)
        button = tk.Button(root, text=f"Buzz {name}", font=("Arial", 18), command=lambda n=name: buzz(n))
        button.grid(row=i, column=1, padx=20, pady=20)
        contestants[name] = {'label': label, 'button': button, 'has_buzzed': False}

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
    elif event.char == 'w':  # 'w' key to stop blinking and reset buzzers
        stop_blinking()
        reset_buzzers()
    elif event.char == 'x':  # 'x' key to gray out the buzzed contestant and enable others
        global buzzed
        if buzzed is not None:
            stop_blinking()
            contestants[buzzed]['label'].config(bg='gray')
            contestants[buzzed]['button'].config(state=tk.DISABLED)
            for c in contestants:
                if c != buzzed:
                    contestants[c]['button'].config(state=tk.NORMAL)
            buzzed = None

# Bind key press event
root.bind("<Key>", on_key_press)

# Add reset button
# reset_button = tk.Button(root, text="Reset Buzzers", font=("Arial", 18), command=reset_buzzers)
# reset_button.grid(row=0, column=2, padx=20, pady=20)

# Start the application
root.mainloop()