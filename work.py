import fitz
import easyocr
import numpy as np
from PIL import Image
import io
import os
import re


def slugify(text):
    """Generál egy slugot (webbarát címet) a Markdown hivatkozásokhoz."""
    text = text.lower()
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'[^\w-]', '', text)
    return text


def hybrid_pdf_to_markdown_enhanced_multilingual(pdf_path, output_md_path, confidence_threshold=0.5):
    """
    Fejlett hibrid PDF-feldolgozás EasyOCR-rel, pozíció alapú sorrendezéssel,
    redundancia-kezeléssel, tartalomjegyzékkel és OCR-jelöléssel.
    Támogatja a többnyelvű dokumentumokat.
    """
    if not os.path.exists(pdf_path):
        print(f"Hiba: A fájl nem található: {pdf_path}")
        return

    # Az EasyOCR olvasó inicializálása több nyelvvel
    reader = easyocr.Reader(['hu', 'en'])

    doc = fitz.open(pdf_path)
    page_contents = []
    toc = []

    print(f"Feldolgozás alatt: {pdf_path}")

    for page_num in range(doc.page_count):
        print(f"Oldal {page_num + 1} feldolgozása...")
        page = doc.load_page(page_num)
        page_elements = []

        # Hagyományos szöveg kinyerése pozícióval
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            bbox = block[:4]
            text = block[4].strip()
            if text:
                page_elements.append({
                    "type": "text",
                    "bbox": bbox,
                    "text": text
                })

        # Képek kinyerése és OCR futtatása
        images = page.get_images(full=True)
        for img_index, img_info in enumerate(images):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            try:
                image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                img_np = np.array(image_pil)

                results = reader.readtext(img_np)

                for (bbox, text, prob) in results:
                    if prob > confidence_threshold:
                        page_elements.append({
                            "type": "ocr",
                            "bbox": (bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]),
                            "text": text,
                            "prob": prob
                        })
            except Exception as e:
                print(f"Hiba a kép {img_index + 1} feldolgozásakor: {e}")

        # Rendezés, deduplikáció és kombinálás
        page_elements.sort(key=lambda x: (x["bbox"][1], x["bbox"][0]))

        combined_text = []
        processed_texts = set()

        for element in page_elements:
            text = element["text"]

            is_redundant = False
            if text in processed_texts:
                is_redundant = True
            else:
                for processed_text in processed_texts:
                    if text in processed_text and len(text) < len(processed_text):
                        is_redundant = True
                        break

            if not is_redundant:
                if element["type"] == "ocr":
                    combined_text.append(f"**[OCR]** {text}")
                else:
                    combined_text.append(text)
                processed_texts.add(text)

        final_text = "\n".join(combined_text).strip()
        page_title = f"Oldal {page_num + 1}"
        toc.append(f"- [{page_title}](#{slugify(page_title)})")
        page_contents.append(f"## {page_title}\n\n{final_text}\n\n---")

    doc.close()

    final_markdown = "## Tartalomjegyzék\n\n" + "\n".join(toc) + "\n\n" + "\n".join(page_contents)

    try:
        with open(output_md_path, "w", encoding="utf-8") as md_file:
            md_file.write(final_markdown)
        print(f"A feldolgozás befejeződött! A kimeneti fájl: {output_md_path}")
    except Exception as e:
        print(f"Hiba történt a fájl írásakor: {e}")


# Használati példa
if __name__ == '__main__':
    input_pdf = "minta.pdf"  # Cseréld le a saját többnyelvű PDF fájlodra
    output_markdown = "kinyert_szoveg_fejlett_multilingual.md"
    hybrid_pdf_to_markdown_enhanced_multilingual(input_pdf, output_markdown)