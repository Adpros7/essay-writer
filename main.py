import os
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Essay Writer")
    root.geometry("800x600")
    extra_params = {"justify": "center", "master": root, "bg": "black", "fg": "white"}
    prompt_box_text_var = tk.StringVar(root, value="Enter your prompt here")
    prompt_box = tk.Entry(width=100, textvariable=prompt_box_text_var, **extra_params)
    prompt_box.place(relx=0.5, rely=0.1, anchor="center")
    def generate():
        prompt = prompt_box_text_var.get()
        key = os.getenv("OPENAI_API_KEY")

    gen_button = tk.Button(text="Generate", command=generate, **extra_params)
    gen_button.place(relx=0.5, rely=0.2, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    main()
