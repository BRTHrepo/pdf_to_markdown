import tkinter as tk
from tkinter import filedialog, messagebox
import os
from work import hybrid_pdf_to_markdown_enhanced_multilingual

def select_file():
    # Fájl kiválasztása
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    timer_label.config(text="Feldolgozás elkezdődött...")
    root.update()
    if file_path:
        try:
            # Feldolgozás és mentés
            output_md_path = os.path.splitext(file_path)[0] + ".md"
            hybrid_pdf_to_markdown_enhanced_multilingual(file_path, output_md_path)
            messagebox.showinfo("Siker", f"A fájl feldolgozása sikeres!\nMentve: {output_md_path}")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

# Tkinter ablak létrehozása
def start():
    global stop_processing, root, timer_label
    stop_processing = False
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

    # CUDA használatának kapcsolója
    cuda_var = tk.BooleanVar(value=False)
    cuda_checkbox = tk.Checkbutton(root, text="CUDA használata (ha elérhető)", variable=cuda_var, font=("Arial", 12))
    cuda_checkbox.pack(pady=10)

    # Oldalszám kijelző címke
    page_label = tk.Label(root, text="Oldalak feldolgozása: N/A", font=("Arial", 12))
    page_label.pack(pady=10)

    # Időmérő címke
    timer_label = tk.Label(root, text="Feldolgozási idő: N/A", font=("Arial", 12))
    timer_label.pack(pady=10)

    # Megszakító gomb inicializálása
    if not hasattr(root, "stop_button"):
        root.stop_button = tk.Button(root, text="Feldolgozás megszakítása", font=("Arial", 12))
        root.stop_button.pack(pady=10)

    # Frissített fájl kiválasztási funkció
    def select_file_with_timer():
        global stop_processing
        stop_processing = False
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                import time
                start_time = time.time()

                # Időmérő frissítése külön szálon
                import threading

                def update_timer():
                    while not stop_processing:
                        elapsed_time = time.time() - start_time
                        timer_label.config(text=f"Feldolgozási idő: {elapsed_time:.2f} másodperc")
                        root.update()
                        time.sleep(0.1)

                timer_thread = threading.Thread(target=update_timer, daemon=True)
                timer_thread.start()

                # CUDA vagy CPU használata a kapcsoló állapota alapján
                use_cuda = cuda_var.get()
                if use_cuda and torch.cuda.is_available():
                    device = "cuda"
                else:
                    device = "cpu"

                # Feldolgozás megszakításának támogatása
                def stop_process():
                    global stop_processing
                    stop_processing = True
                    if timer_thread and timer_thread.is_alive():
                        timer_thread.join(timeout=0)
                    timer_label.config(text="Feldolgozási idő: N/A")
                    messagebox.showinfo("Megszakítva", "A feldolgozás megszakítva lett.")

                root.stop_button.config(command=stop_process)

                # Feldolgozás külön szálon
                def process_pdf():
                    if stop_processing:
                        return
                    try:
                        output_md_path = os.path.splitext(file_path)[0] + ".md"
                        total_pages = 0
                        current_page = 0

                        # Oldalszám kijelzés inicializálása
                        page_label.config(text="Oldalak feldolgozása: 0/0")
                        root.update()

                        def update_page_label():
                            page_label.config(text=f"Oldalak feldolgozása: {total_pages}/{current_page}")
                            root.update()

                        # Feldolgozás logikája
                        def process_page_callback(page, total):
                            nonlocal current_page, total_pages
                            if stop_processing:
                                raise Exception("A feldolgozás megszakítva lett.")
                            current_page = page
                            total_pages = total
                            update_page_label()

                        hybrid_pdf_to_markdown_enhanced_multilingual(
                            file_path, output_md_path, device=device, page_callback=process_page_callback
                        )
                        if timer_thread and timer_thread.is_alive():
                            timer_thread.join(timeout=0)
                        elapsed_time = time.time() - start_time
                        timer_label.config(text=f"Feldolgozási idő: {elapsed_time:.2f} másodperc")
                        messagebox.showinfo("Siker", f"A fájl feldolgozása sikeres!\nMentve: {output_md_path}")
                    except Exception as e:
                        messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

                process_thread = threading.Thread(target=process_pdf, daemon=True)
                process_thread.start()
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

    # Gomb a fájl kiválasztásához (frissített funkcióval)
    select_button.config(command=select_file_with_timer)

    # Ablak futtatása
    root.mainloop()

# Az `ui.py` most már kizárólag modulként használható.
