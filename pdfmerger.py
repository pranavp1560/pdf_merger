import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
import subprocess
import os

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if files:
        for file in files:
            listbox_files.insert(tk.END, file)

def merge_pdfs():
    if listbox_files.size() == 0:
        messagebox.showerror("Error", "No files selected.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not save_path:
        return

    merger = PdfMerger()

    try:
        for file in listbox_files.get(0, tk.END):
            merger.append(file)
        
        merger.write(save_path)
        merger.close()
        messagebox.showinfo("Success", f"PDFs merged successfully and saved as {save_path}")
        listbox_files.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

def image_to_pdf():
    image_files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if not image_files:
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not save_path:
        return

    try:
        image_list = []
        for image_file in image_files:
            img = Image.open(image_file).convert("RGB")
            image_list.append(img)
        
        if image_list:
            image_list[0].save(save_path, save_all=True, append_images=image_list[1:])
            messagebox.showinfo("Success", f"Images converted to PDF and saved as {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert images to PDF:\n{e}")

def compress_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not save_path:
        return

    try:
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            # You could add options here to modify the page (e.g., lower image quality)
            writer.add_page(page)

        # Save to the new compressed file
        with open(save_path, "wb") as f:
            writer.write(f)

        messagebox.showinfo("Success", f"PDF compressed and saved as {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress PDF:\n{e}")

def clear_list():
    listbox_files.delete(0, tk.END)

def remove_selected():
    selected_items = listbox_files.curselection()
    for index in reversed(selected_items):
        listbox_files.delete(index)

root = tk.Tk()
root.title("PDF Merger and Tools")
root.geometry("1200x900")
root.config(bg="cyan")

header = tk.Label(root, text="PDF Merger and Tools", font=("Helvetica", 18, "bold"), bg="cyan", fg="#333")
header.pack(pady=10)
frame_buttons = tk.Frame(root, bg="cyan")
frame_buttons.pack(pady=5)

btn_select_files = tk.Button(frame_buttons, text="Select PDFs", command=select_files, bg="#4CAF50", fg="white", font=("Helvetica", 12), padx=10)
btn_select_files.grid(row=0, column=0, padx=5)

btn_merge = tk.Button(frame_buttons, text="Merge PDFs", command=merge_pdfs, bg="#2196F3", fg="white", font=("Helvetica", 12), padx=10)
btn_merge.grid(row=0, column=1, padx=5)

btn_image_to_pdf = tk.Button(frame_buttons, text="Images to PDF", command=image_to_pdf, bg="#8E44AD", fg="white", font=("Helvetica", 12), padx=10)
btn_image_to_pdf.grid(row=0, column=2, padx=5)

btn_compress = tk.Button(frame_buttons, text="Compress PDF", command=compress_pdf, bg="#E67E22", fg="white", font=("Helvetica", 12), padx=10)
btn_compress.grid(row=0, column=3, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear List", command=clear_list, bg="#f44336", fg="white", font=("Helvetica", 12), padx=10)
btn_clear.grid(row=0, column=4, padx=5)

btn_remove_selected = tk.Button(frame_buttons, text="Remove Selected", command=remove_selected, bg="#FFC107", fg="black", font=("Helvetica", 12), padx=10)
btn_remove_selected.grid(row=0, column=5, padx=5)

listbox_files = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80, height=15, font=("Helvetica", 10))  # Increased listbox height
listbox_files.pack(pady=10)

root.mainloop()
