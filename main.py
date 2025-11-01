from concurrent.futures import thread
import glob
import os
import random
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
            global countdown_var
            var.set("Generating...")
            prompt = prompt_box_text_var.get()
            key = os.getenv("OPENAI_API_KEY")
            client = Assistant(
                key,
                model="chatgpt-4o-latest",
                system_prompt="Act as an expert essay writer. Begin with a concise checklist (3-7 bullets) outlining your approach: planning, drafting, reviewing, and refining the essay but don't actually include this in the response. Write in a natural, human-like style by referencing examples of how people type on the web. Only respond with the essay itself—do not include any headers or formatting other than plain text. Ensure your essay uses clear indentation and follows standard paragraph structure. Do not use Markdown formatting; write as if intended for a plain text (.txt) file. Set reasoning_effort = minimal for plain text composition and output only the completed essay.",
            )
            response = client.chat(prompt)
            for i in range(4, -2, -1):
                var.set(f"Typing in {i+1}")
                time.sleep(1)

            var.set("Starting...")
            print(response)

            def press_and_release(k, key):
                k.press(key)
                k.release(key)

            k = pynput.keyboard.Controller()
            extra_key = ""
            for char in response:
                if random.randint(0, 10) == 0:
                    type_of_typo = random.randint(0, 2)
                    if type_of_typo == 0:
                        press_and_release(k, "l")
                        press_and_release(k, str(char))
                        press_and_release(k, pynput.keyboard.Key.left)
                        press_and_release(k, pynput.keyboard.Key.backspace)
                        press_and_release(k, pynput.keyboard.Key.right)

                    elif type_of_typo == 1:
                        press_and_release(k, "z")
                        press_and_release(k, pynput.keyboard.Key.backspace)
                        press_and_release(k, char)

                    else:
                        extra_key = char


                else:
                    k.press(str(char))

                    k.release(str(char))
                if extra_key:
                    press_and_release(k, extra_key)
                if not char == " ":
                    time.sleep(0.2)

                else:
                    time.sleep(0.1)

            var.set("Done")
            time.sleep(2)
            var.set("Generate button not clicked yet")

        thread.ThreadPoolExecutor().submit(code)

    gen_button = tk.Button(text="Generate", command=generate, **extra_params)
    gen_button.place(relx=0.5, rely=0.2, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    main()
