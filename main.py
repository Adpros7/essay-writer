from concurrent.futures import thread
import os
import random
import threading
import time
import tkinter as tk
from easier_openai import Assistant
import pynput


def main():
    root = tk.Tk()
    root.title("Essay Writer")
    root.geometry("800x600")
    extra_params = {"justify": "center", "master": root, "bg": "black", "fg": "white"}
    prompt_box_text_var = tk.StringVar(root, value="Enter your prompt here")
    prompt_box = tk.Entry(width=100, textvariable=prompt_box_text_var, **extra_params)
    prompt_box.place(relx=0.5, rely=0.1, anchor="center")
    countdown_var = tk.StringVar(root, value="Generate button not clicked yet")
    countdown_label = tk.Label(textvariable=countdown_var, **extra_params)
    countdown_label.place(relx=0.5, rely=0.3, anchor="center")

    def generate(var=countdown_var):
        def code():
            prompt = prompt_box_text_var.get()
            key = os.getenv("OPENAI_API_KEY")
            client = Assistant(
                key,
                model="chatgpt-4o-latest",
                system_prompt="Act as an expert essay writer..."
            )

            def update(text):
                root.after(0, var.set, text)

            update("Generating...")
            response = client.chat(prompt)

            for i in range(4, -2, -1):
                update(f"Typing in {i+1}")
                time.sleep(1)

            update("Starting...")
            print(response)

            k = pynput.keyboard.Controller()

            def randsleep(num):
                time.sleep(random.uniform(num - (num / 3), num + (num / 3)))

            def press_and_release(k, key):
                if isinstance(key, pynput.keyboard.Key):
                    k.press(key)
                    k.release(key)
                else:
                    k.type(key)
                randsleep(0.08)

            for i, char in enumerate(response):
                # ... same typing logic ...
                pass

            update("Done")
            randsleep(2)
            update("Generate button not clicked yet")

        threading.Thread(target=code, daemon=True).start()

    gen_button = tk.Button(text="Generate", command=generate, **extra_params)
    gen_button.place(relx=0.5, rely=0.2, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    main()
