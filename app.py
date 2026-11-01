
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import threading

# --------------------------------
# 1. Load Gemini API Key
# --------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found. Check your .env file.")

# Connect to Gemini
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=60_000,
        retry_options=types.HttpRetryOptions(
            attempts=3,
            initial_delay=1,
            max_delay=10,
            http_status_codes=[408, 429, 500, 502, 503, 504]
        )
    )
)


# --------------------------------
# 2. Generate Academic Content
# --------------------------------

def generate_content():

    user_input = input_box.get("1.0", tk.END).strip()
    task = task_choice.get()

    if not user_input:
        messagebox.showwarning(
            "Input Required",
            "Please enter some academic content."
        )
        return

    # Create prompts based on selected task

    if task == "Generate Notes":

        prompt = f"""
        Create well-structured academic notes.
        Include headings, subheadings and bullet points.

        Content: {user_input}
        """

    elif task == "Summarize Content":

        prompt = f"""
        Summarize the following academic content.
        Include only the important points.

        Content: {user_input}
        """

    elif task == "Explain a Concept":

        prompt = f"""
        Explain the following academic concept
        in simple language with examples.

        Content: {user_input}
        """

    else:

        prompt = f"""
        Create study material from the following content.
        Include definitions, key concepts and revision points.

        Content: {user_input}
        """

    # Display loading message

    generate_button.config(state=tk.DISABLED)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Generating content... Please wait.")

    def show_result(response=None, error=None):
        output_box.delete("1.0", tk.END)

        if error:
            output_box.insert(tk.END, f"Error Details:\n{error}")
            print("Gemini API Error:", error)
        elif response and response.text:
            output_box.insert(tk.END, response.text)
        else:
            output_box.insert(tk.END, "Gemini returned an empty response.")

        generate_button.config(state=tk.NORMAL)

    def request_content():
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            root.after(0, show_result, response, None)
        except Exception as error:
            root.after(0, show_result, None, str(error))

    threading.Thread(target=request_content, daemon=True).start()


# --------------------------------
# 3. Clear Input and Output
# --------------------------------

def clear_content():

    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)


# --------------------------------
# 4. Create Main Window
# --------------------------------

root = tk.Tk()

root.title("EduGenie - AI Study Assistant")
root.geometry("850x700")
root.minsize(650, 550)

root.configure(bg="#F1F4F9")


# --------------------------------
# 5. Application Heading
# --------------------------------

heading = tk.Label(
    root,
    text="EduGenie",
    font=("Arial", 28, "bold"),
    bg="#F1F4F9",
    fg="#3448A5"
)

heading.pack(pady=(20, 5))


subtitle = tk.Label(
    root,
    text="Your AI-Powered Academic Study Assistant",
    font=("Arial", 12),
    bg="#F1F4F9",
    fg="#666666"
)

subtitle.pack(pady=(0, 20))


# --------------------------------
# 6. Task Selection
# --------------------------------

task_label = tk.Label(
    root,
    text="Select Your Task:",
    font=("Arial", 12, "bold"),
    bg="#F1F4F9"
)

task_label.pack(anchor="w", padx=40)


task_choice = ttk.Combobox(
    root,
    values=[
        "Generate Notes",
        "Summarize Content",
        "Explain a Concept",
        "Generate Study Material"
    ],
    state="readonly",
    font=("Arial", 11)
)

task_choice.current(0)

task_choice.pack(
    fill="x",
    padx=40,
    pady=10
)


# --------------------------------
# 7. Academic Content Input
# --------------------------------

input_label = tk.Label(
    root,
    text="Enter Your Academic Content:",
    font=("Arial", 12, "bold"),
    bg="#F1F4F9"
)

input_label.pack(anchor="w", padx=40)


input_box = scrolledtext.ScrolledText(
    root,
    height=7,
    font=("Arial", 11),
    wrap=tk.WORD
)

input_box.pack(
    fill="x",
    padx=40,
    pady=10
)


# --------------------------------
# 8. Generate Button
# --------------------------------

generate_button = tk.Button(
    root,
    text="Generate Content",
    font=("Arial", 12, "bold"),
    bg="#3448A5",
    fg="white",
    command=generate_content
)

generate_button.pack(pady=10)


# --------------------------------
# 9. Generated Content Output
# --------------------------------

output_label = tk.Label(
    root,
    text="Generated Academic Content:",
    font=("Arial", 12, "bold"),
    bg="#F1F4F9"
)

output_label.pack(
    anchor="w",
    padx=40,
    pady=(10, 0)
)


output_box = scrolledtext.ScrolledText(
    root,
    height=12,
    font=("Arial", 11),
    wrap=tk.WORD
)

output_box.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=10
)


# --------------------------------
# 10. Clear Button
# --------------------------------

clear_button = tk.Button(
    root,
    text="Clear",
    font=("Arial", 11),
    bg="#555555",
    fg="white",
    command=clear_content
)

clear_button.pack(pady=10)


# --------------------------------
# 11. Footer
# --------------------------------

footer = tk.Label(
    root,
    text="Powered by Python and Google Gemini AI",
    font=("Arial", 9),
    bg="#F1F4F9",
    fg="#777777"
)

footer.pack(pady=10)


# --------------------------------
# 12. Run Application
# --------------------------------

root.mainloop()
