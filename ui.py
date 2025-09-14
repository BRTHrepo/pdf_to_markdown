import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
import threading
from work import hybrid_pdf_to_markdown_enhanced_multilingual

def main():
    def select_file_with_timer():
        global timer_thread, stop_processing

        stop_processing = False
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        try:
            start_time = time.time()

            def stop_timer_callback(elapsed_time):
                timer_label.config(text=f"Feldolgozási idő: {elapsed_time:.2f} másodperc")

            def update_timer():
                def refresh_timer():
                    if not stop_processing:
                        elapsed_time = time.time() - start_time
                        timer_label.config(text=f"Feldolgozási idő: {elapsed_time:.2f} másodperc")
                        root.after(100, refresh_timer)
                    elif stop_processing:
                        stop_timer_callback(elapsed_time)
                refresh_timer()
            timer_thread = threading.Thread(target=update_timer, daemon=True)
            timer_thread.start()

            # Eszköz kiválasztás
            use_cuda = cuda_var.get()
            device = "cpu"
            try:
                import torch
                if use_cuda and torch.cuda.is_available():
                    device = "cuda"
            except ImportError:
                pass

            def stop_process():
                global stop_processing
                stop_processing = True
                if timer_thread and timer_thread.is_alive():
                    timer_thread.join(timeout=0)
                timer_label.config(text="Feldolgozási idő: N/A")
                messagebox.showinfo("Megszakítva", "A feldolgozás megszakítva lett.")
            stop_button.config(command=stop_process)

            def process_pdf():
                global stop_processing
                if stop_processing:
                    return
                try:
                    output_md_path = os.path.splitext(file_path)[0] + ".md"
                    total_pages = 0
                    current_page = 0
                    page_label.config(text="Oldalak feldolgozása: 0/0")
                    root.update()
                    def update_page_label():
                        page_label.config(text=f"Oldalak feldolgozása: {current_page}/{total_pages}")
                        root.update()
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
                    stop_timer_callback(elapsed_time)
                    messagebox.showinfo("Siker", f"A fájl feldolgozása sikeres!\nMentve: {output_md_path}")
                except Exception as e:
                    messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

            threading.Thread(target=process_pdf, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a feldolgozás során: {e}")

    # Kezdeti GUI változók
    stop_processing = False
    timer_thread = None

    root = tk.Tk()
    root.title("PDF-ből Markdown átalakító")
    root.geometry("800x600")

    select_button = tk.Button(root, text="PDF kiválasztása", width=30, height=2, font=("Arial", 14), command=select_file_with_timer)
    select_button.pack(pady=20)

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

    version_label = tk.Label(root, text="Verzióinformációk betöltése...", font=("Arial", 12))
    version_label.pack(pady=10)
    try:
        import sys
        python_version = sys.version.split()
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

    cuda_var = tk.BooleanVar(value=False)
    cuda_checkbox = tk.Checkbutton(root, text="CUDA használata (ha elérhető)", variable=cuda_var, font=("Arial", 12))
    cuda_checkbox.pack(pady=10)

    page_label = tk.Label(root, text="Oldalak feldolgozása: N/A", font=("Arial", 12))
    page_label.pack(pady=10)
    timer_label = tk.Label(root, text="Feldolgozási idő: N/A", font=("Arial", 12))
    timer_label.pack(pady=10)
    stop_button = tk.Button(root, text="Feldolgozás megszakítása", font=("Arial", 12))
    stop_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()
