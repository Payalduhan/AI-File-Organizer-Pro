import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# =========================
# GLOBAL VARIABLES
# =========================
folder_path = ""
moved_files = []

# =========================
# SMART AI CLASSIFIER
# =========================


def smart_category(filename, extension):

    name = filename.lower()

    # AI-like name based logic
    if any(word in name for word in ["resume", "cv"]):
        return "Documents"

    if any(word in name for word in ["invoice", "bill", "payment"]):
        return "Finance"

    if any(word in name for word in ["project", "ai", "ml", "report"]):
        return "Projects"

    # Extension-based fallback
    if extension in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return "Images"

    if extension in [".pdf", ".docx", ".txt", ".pptx", ".xlsx"]:
        return "Documents"

    if extension in [".mp4", ".mkv", ".mov", ".avi"]:
        return "Videos"

    if extension in [".mp3", ".wav"]:
        return "Music"

    if extension in [".zip", ".rar"]:
        return "Archives"

    if extension == ".py":
        return "Python_Files"

    return "Others"

# =========================
# SELECT FOLDER
# =========================


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    label.config(text=folder_path)

# =========================
# CREATE FOLDERS
# =========================


def create_folders():

    categories = ["Images", "Documents", "Videos", "Music",
                  "Archives", "Python_Files", "Finance", "Projects", "Others"]

    for cat in categories:
        path = os.path.join(folder_path, cat)
        if not os.path.exists(path):
            os.makedirs(path)

# =========================
# ORGANIZE FILES (AI POWERED)
# =========================


def organize_files():

    global moved_files

    if not folder_path:
        messagebox.showerror("Error", "Please select a folder first!")
        return

    moved_files = []

    create_folders()

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        category = smart_category(file, extension)

        dest = os.path.join(folder_path, category, file)

        shutil.move(file_path, dest)

        moved_files.append((dest, file_path))

    messagebox.showinfo("Success", "AI File Organization Completed!")

# =========================
# UNDO FUNCTION
# =========================


def undo_changes():

    if not moved_files:
        messagebox.showinfo("Undo", "Nothing to undo!")
        return

    for new_path, old_path in moved_files:
        if os.path.exists(new_path):
            shutil.move(new_path, old_path)

    moved_files.clear()

    messagebox.showinfo("Undo", "Changes Reverted Successfully!")

# =========================
# REMOVE DUPLICATES
# =========================


def remove_duplicates():

    if not folder_path:
        messagebox.showerror("Error", "Select a folder first!")
        return

    seen = set()
    deleted = 0

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        if file in seen:
            os.remove(file_path)
            deleted += 1
        else:
            seen.add(file)

    messagebox.showinfo("Done", f"Removed {deleted} duplicate files")


# =========================
# UI SETUP (MODERN DARK THEME)
# =========================
app = tk.Tk()
app.title("AI File Organizer Pro")
app.geometry("600x450")
app.configure(bg="#0f1115")

# ================= HEADER =================
header = tk.Label(
    app,
    text="AI FILE ORGANIZER PRO",
    font=("Helvetica", 20, "bold"),
    fg="white",
    bg="#0f1115"
)
header.pack(pady=20)

subtitle = tk.Label(
    app,
    text="Organize your files intelligently in one click",
    font=("Helvetica", 11),
    fg="#a0a0a0",
    bg="#0f1115"
)
subtitle.pack(pady=5)

# ================= STATUS =================
label = tk.Label(
    app,
    text="No folder selected",
    fg="#ffffff",
    bg="#0f1115",
    font=("Helvetica", 10)
)
label.pack(pady=15)

# ================= BUTTON STYLE =================


def styled_button(text, command):
    return tk.Button(
        app,
        text=text,
        command=command,
        font=("Helvetica", 11, "bold"),
        fg="white",
        bg="#1f2937",
        activebackground="#374151",
        activeforeground="white",
        width=30,
        height=2,
        bd=0,
        cursor="hand2"
    )


# ================= BUTTON FRAME =================
frame = tk.Frame(app, bg="#0f1115")
frame.pack(pady=10)

btn1 = styled_button("📁 Select Folder", select_folder)
btn1.pack(pady=8)

btn2 = styled_button("⚡ AI Organize Files", organize_files)
btn2.pack(pady=8)

btn3 = styled_button("↩ Undo Last Action", undo_changes)
btn3.pack(pady=8)

btn4 = styled_button("🧹 Remove Duplicates", remove_duplicates)
btn4.pack(pady=8)

# ================= FOOTER =================
footer = tk.Label(
    app,
    text="Built with Python • AI Powered Organizer",
    fg="#6b7280",
    bg="#0f1115",
    font=("Helvetica", 9)
)
footer.pack(side="bottom", pady=15)

app.mainloop()
