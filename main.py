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
        contestants[c]['score_label'].config(text=f"Score: {contestants[c]['score']}")
        contestants[c]['has_buzzed'] = False
        contestants[c]['label'].config(bg='white')


# Load and display background image
background_image = Image.open('data\media\images\\background.png')
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Display contestant images
def display_contestant_images(names):
    buzzer_image = Image.open(f'data\media\images\\buzzer\\buzzer_neutral.png')
    for i, name in enumerate(names):
        image = Image.open(f'data\media\images\players\{name.lower()}.png')  # Assuming you have images named alice.jpg, bob.jpg, etc.
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo, text=name, compound="bottom", font=("Arial", 18))
        label.image = photo  # Keep a reference to avoid garbage collection
        label.grid(row=0, column=i, padx=20, pady=20)
        score_label = tk.Label(root, text="Score: 0", font=("Arial", 18))
        score_label.grid(row=i, column=1, padx=20, pady=20)
        contestants[name] = {'label': label, 'score_label': score_label, 'has_buzzed': False, 'score': 0}

# Adjust the main window dimensions and placement
root.geometry("1920x1080")

# Sample contestants
contestant_names = ["Shulk", "Melia", "Kino", "Nene"]
display_contestant_images(contestant_names)

# Mapping of keys to contestants
key_to_contestant = {'a': "Shulk", 'z': "Melia", 'e': "Kino", 'r': "Nene"}

def on_key_press(event):
    global buzzed
    if event.char in key_to_contestant:
        buzz(key_to_contestant[event.char])
    elif event.char == 'w':  # 'w' key to stop blinking and reset buzzers
        stop_blinking()
        reset_buzzers()
    elif event.char == 'x':  # 'w' key to stop blinking and reset buzzers
        if buzzed is not None:
            contestants[buzzed]['score'] += 1
            stop_blinking()
            reset_buzzers()
    elif event.char == 'c':  # 'x' key to gray out the buzzed contestant and enable others
        if buzzed is not None:
            stop_blinking()
            contestants[buzzed]['label'].config(bg='gray')
            buzzed = None


# Bind key press event
root.bind("<Key>", on_key_press)

# Add reset button
# reset_button = tk.Button(root, text="Reset Buzzers", font=("Arial", 18), command=reset_buzzers)
# reset_button.grid(row=0, column=2, padx=20, pady=20)

# Start the application
root.mainloop()