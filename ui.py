import tkinter as tk
from tkinter import filedialog, messagebox
import os
from work import hybrid_pdf_to_markdown_enhanced_multilingual

def select_file():
    # Fájl kiválasztása
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            # Feldolgozás és mentés
            output_md_path = os.path.splitext(file_path)[0] + ".md"
            hybrid_pdf_to_markdown_enhanced_multilingual(file_path, output_md_path)
            messagebox.showinfo("Siker", f"A fájl feldolgozása sikeres!\nMentve: {output_md_path}")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

# Tkinter ablak létrehozása
def main():
    root = tk.Tk()
    root.title("PDF-ből Markdown átalakító")

    # Gomb a fájl kiválasztásához
    select_button = tk.Button(root, text="PDF kiválasztása", command=select_file, width=30, height=2)
    select_button.pack(pady=20)

    # Ablak futtatása
    root.mainloop()

if __name__ == "__main__":
    main()
