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
    root.geometry("800x600")

    # Gomb a fájl kiválasztásához
    select_button = tk.Button(root, text="PDF kiválasztása", command=select_file, width=30, height=2, font=("Arial", 14))
    select_button.pack(pady=20)

    # Hardvertámogatás ellenőrzése
    hardware_label = tk.Label(root, text="Hardvertámogatás ellenőrzése...", font=("Arial", 12))
    hardware_label.pack(pady=10)

    try:
        import torch
        if torch.cuda.is_available():
            hardware_label.config(text="CUDA támogatott és használatban.", fg="green")
        else:
            hardware_label.config(text="CUDA nem érhető el.", fg="red")
    except ImportError:
        hardware_label.config(text="A PyTorch nincs telepítve.", fg="orange")

    # Verzióinformációk megjelenítése
    version_label = tk.Label(root, text="Verzióinformációk betöltése...", font=("Arial", 12))
    version_label.pack(pady=10)

    try:
        import sys
        python_version = sys.version.split()[0]
        version_text = f"Python verzió: {python_version}"

        import torch
        version_text += f"\nPyTorch verzió: {torch.__version__}"
        if torch.cuda.is_available():
            version_text += f"\nCUDA verzió: {torch.version.cuda}"
        else:
            version_text += "\nCUDA nem érhető el."

        try:
            import torchvision
            version_text += f"\nTorchvision verzió: {torchvision.__version__}"
        except ImportError:
            version_text += "\nTorchvision nincs telepítve."

        try:
            import torchaudio
            version_text += f"\nTorchaudio verzió: {torchaudio.__version__}"
        except ImportError:
            version_text += "\nTorchaudio nincs telepítve."

        version_label.config(text=version_text, fg="black")
    except Exception as e:
        version_label.config(text=f"Hiba a verziók betöltésekor: {e}", fg="red")

    # Ablak futtatása
    root.mainloop()

if __name__ == "__main__":
    main()
