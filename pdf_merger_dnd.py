import os
from PyPDF2 import PdfMerger
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk

# -------------------
# Helper Functions
# -------------------

def center_window(win, width, height):
    """Centers the window on the screen."""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def browse_pdf(entry_field):
    """Opens file dialog and inserts path into entry field."""
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if file_path:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)

def drop_pdf(event, entry_field):
    """Handles file dropped into entry field."""
    file_path = event.data.strip("{}")  # Remove braces if path has spaces
    if file_path.lower().endswith(".pdf"):
        entry_field.delete(0, tk.END)
        entry_field.insert(0, file_path)
    else:
        messagebox.showwarning("Invalid File", "Please drop a valid PDF file.")

def merge_pdfs():
    """Merges two selected PDF files."""
    pdf1_path = entry_pdf1.get().strip()
    pdf2_path = entry_pdf2.get().strip()

    if not pdf1_path or not pdf2_path:
        messagebox.showwarning("⚠ Missing File", "Please select both PDF files.")
        return

    try:
        merger = PdfMerger()
        merger.append(pdf1_path)
        merger.append(pdf2_path)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Merged PDF As"
        )

        if save_path:
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("✅ Success", f"Merged PDF saved at:\n{save_path}")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to merge PDFs:\n{e}")

# -------------------
# Main Window
# -------------------

root = TkinterDnD.Tk()  # Enables drag & drop
root.title("📎 PDF Merger Tool")
root.configure(bg="#f0f2f5")
center_window(root, 500, 250)
root.resizable(False, False)

# -------------------
# UI Layout
# -------------------

title_label = tk.Label(root, text="📎 PDF Merger Tool", font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#333")
title_label.pack(pady=10)

# First PDF
frame1 = tk.Frame(root, bg="#f0f2f5")
frame1.pack(pady=5)
tk.Label(frame1, text="First PDF:", bg="#f0f2f5").pack(side=tk.LEFT, padx=5)
entry_pdf1 = tk.Entry(frame1, width=40)
entry_pdf1.pack(side=tk.LEFT, padx=5)
entry_pdf1.drop_target_register(DND_FILES)
entry_pdf1.dnd_bind("<<Drop>>", lambda e: drop_pdf(e, entry_pdf1))
tk.Button(frame1, text="Browse", command=lambda: browse_pdf(entry_pdf1), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

# Second PDF
frame2 = tk.Frame(root, bg="#f0f2f5")
frame2.pack(pady=5)
tk.Label(frame2, text="Second PDF:", bg="#f0f2f5").pack(side=tk.LEFT, padx=5)
entry_pdf2 = tk.Entry(frame2, width=40)
entry_pdf2.pack(side=tk.LEFT, padx=5)
entry_pdf2.drop_target_register(DND_FILES)
entry_pdf2.dnd_bind("<<Drop>>", lambda e: drop_pdf(e, entry_pdf2))
tk.Button(frame2, text="Browse", command=lambda: browse_pdf(entry_pdf2), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

# Merge Button
merge_btn = tk.Button(root, text="Merge PDFs", command=merge_pdfs, bg="#007BFF", fg="white", font=("Helvetica", 12), width=20)
merge_btn.pack(pady=20)

# Footer
footer_label = tk.Label(root, text="Developed in Python 🐍 | Drag & Drop Supported", font=("Helvetica", 9), bg="#f0f2f5", fg="#555")
footer_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
