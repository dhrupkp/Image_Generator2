import customtkinter as ctk
import tkinter
import os
import openai
from PIL import Image, ImageTk
import requests
import io
from openai import OpenAI

def generate():
    client = OpenAI()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Get the list of prompts from the multiline entry widget
    user_prompts = prompt_entry.get("1.0", tkinter.END).splitlines()

    style = style_dropdown.get()
    num_images = int(number_slider.get())

    image_urls = []

    for prompt in user_prompts:
        prompt += " in style: " + style
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=num_images,
            size="512x512"
        )

        for i in range(len(response.data)):
            image_urls.append(response.data[i].url)

    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)

    # Clear canvas before updating images
    canvas.delete("all")

    def update_image(index=0):
        if index < len(images):
            canvas.image = images[index]
            canvas.create_image(0, 0, anchor="nw", image=images[index])
            canvas.after(3000, update_image, (index + 1) % len(images))

    update_image()

def clear_canvas():
    canvas.delete("all")
    # Permanently delete the images from memory
    del images[:]

root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(input_frame, text="Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(input_frame, text="# Images")
number_label.grid(row=2, column=0)
number_slider = ctk.CTkSlider(input_frame, from_=1, to=10, number_of_steps=9)
number_slider.grid(row=2, column=1)

generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

clear_button = ctk.CTkButton(input_frame, text="Clear Canvas", command=clear_canvas)
clear_button.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

# Initialize the list to hold images
images = []

root.mainloop()
