# Hibrid PDF-ből Markdown átalakító

Ez a projekt egy Python-alapú eszköz, amely PDF dokumentumokat alakít át Markdown formátumba. A szkript a hagyományos szövegextrakciót és az OCR technológiát kombinálja, hogy a beágyazott és képalapú szövegeket is feldolgozza.

## Főbb funkciók
- **Hibrid megközelítés**: Képes kinyerni a beágyazott szöveget és a képeken belül található szöveget is.
- **Többnyelvű támogatás**: A szkript automatikusan felismeri és feldolgozza a magyar és angol nyelvű szövegeket. Jelenleg csak ez a két nyelv támogatott. A rendszer könnyen bővíthető további nyelvek támogatására az EasyOCR konfigurációjának módosításával, így más nyelvű dokumentumok feldolgozása is lehetővé válik.
- **Pozíció alapú sorrendezés**: A kinyert szövegblokkokat a PDF-ben elfoglalt pozíciójuk alapján rendezi, ezzel megőrzi a dokumentum eredeti logikai szerkezetét.
- **Redundancia-kezelés**: Intelligens algoritmusok segítségével kiszűri a duplikált szövegeket, amelyek a hagyományos és az OCR extrakció során is megjelenhetnek.
- **Tartalomjegyzék generálása**: Létrehoz egy kattintható tartalomjegyzéket a Markdown fájl elején, amely segíti a navigációt az egyes oldalak között.
- **OCR-jelölés**: A képekből kinyert szövegeket **[OCR]** jelöléssel látja el, így könnyen megkülönböztethető a forrása.
- **GUI funkciók**: A szkript egy Tkinter-alapú grafikus felületet biztosít, amely lehetővé teszi a PDF fájlok kiválasztását, feldolgozását, és a folyamat megszakítását.
- **Hardver ellenőrzés**: A GUI ellenőrzi a CUDA és PyTorch elérhetőségét, valamint megjeleníti a verzióinformációkat.
- **Időzítő és állapotjelzés**: A feldolgozási idő és az oldalak feldolgozásának állapota valós időben követhető.

## CUDA és GPU támogatás

A PyTorch GPU-támogatást biztosít. A CUDA 12.9 használatához kövesse az alábbi lépéseket. Jelenleg a 12.9-es verzió kompatibilis minden komponenssel, de a jövőben újabb verziók is megjelenhetnek, amelyek szintén támogatottak lehetnek.

1. **CUDA Toolkit telepítése (12.9)**:
   - Látogasson el az NVIDIA hivatalos [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) oldalára, és töltse le a 12.9-es verziót.

2. **cuDNN telepítése (CUDA 12.9 kompatibilis)**:
   - Töltse le a cuDNN-t az NVIDIA [cuDNN](https://developer.nvidia.com/cudnn) oldaláról, és másolja a megfelelő CUDA 12.9 könyvtárba.

3. **PyTorch CUDA 12.9 támogatású verzió telepítése**:
   - A PyTorch CUDA-kompatibilis verzióját a következő paranccsal telepítheti:
     ```bash
     pip install torch torchvision --index-url https://download.pytorch.org/whl/cu129
     ```

4. **Ellenőrzés**:
   - A CUDA támogatás ellenőrzéséhez futtassa a következő parancsokat:
     ```python
     import torch
     print(torch.cuda.is_available())
     print(torch.version.cuda)
     ```

Ezekkel a lépésekkel biztosítható, hogy a rendszer megfelelően használja a CUDA 12.9 támogatást.

### Haladó beállítások: NVIDIA kártyák használata CUDA-hoz

Az NVIDIA GPU-k használatához a következő lépéseket kell elvégezni:
1. Telepítse az NVIDIA illesztőprogramokat a GPU-jához.
2. Telepítse a CUDA Toolkit-et az NVIDIA hivatalos weboldaláról: [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit).
3. Telepítse a cuDNN könyvtárat a megfelelő CUDA verzióhoz: [cuDNN](https://developer.nvidia.com/cudnn).
4. Győződjön meg róla, hogy a telepített CUDA verzió kompatibilis a PyTorch verzióval.

## Modellek letöltése

Az EasyOCR az első futtatáskor automatikusan letölti a szükséges modelleket.

Ez a Python szkript egy fejlett eszköz, amely a PDF dokumentumokat Markdown formátumba alakítja. A szkript a hagyományos szövegextrakciót a beágyazott szöveg kinyeréséhez (a fitz könyvtár segítségével) kombinálja a képekből történő szövegfelismeréssel (OCR - easyocr használatával). Ez a hibrid megközelítés lehetővé teszi, hogy a szkript a beolvasott, kép-alapú PDF-ekben lévő szöveget is feldolgozza, így egy átfogó megoldást nyújt a dokumentumok digitalizálására.

## Főbb funkciók

- **Hibrid megközelítés**: Képes kinyerni a beágyazott szöveget és a képeken belül található szöveget is.
- **Többnyelvű támogatás**: A szkript automatikusan felismeri és feldolgozza a magyar és angol nyelvű szövegeket.
- **Pozíció alapú sorrendezés**: A kinyert szövegblokkokat a PDF-ben elfoglalt pozíciójuk alapján rendezi, ezzel megőrzi a dokumentum eredeti logikai szerkezetét.
- **Redundancia-kezelés**: Intelligens algoritmusok segítségével kiszűri a duplikált szövegeket, amelyek a hagyományos és az OCR extrakció során is megjelenhetnek.
- **Tartalomjegyzék generálása**: Létrehoz egy kattintható tartalomjegyzéket a Markdown fájl elején, amely segíti a navigációt az egyes oldalak között.
- **OCR-jelölés**: A képekből kinyert szövegeket **[OCR]** jelöléssel látja el, így könnyen megkülönböztethető a forrása.

## Használati útmutató

A szkript használatához kövesse az alábbi lépéseket:

1. Telepítse a szükséges függőségeket:
   ```bash
   pip install -r requirements.txt
   ```


## Követelmények

- Python 3.8 vagy újabb
- Könyvtárak:
  - PyMuPDF
  - torch
  - torchvision
  - torchaudio
  - easyocr
  - numpy

## Példa kimenet

A generált Markdown fájl tartalmazza:
- A PDF dokumentum szöveges tartalmát logikai sorrendben.
- Kattintható tartalomjegyzéket.
- **[OCR]** jelöléssel ellátott szövegeket a képekből kinyert tartalomhoz.

## Licenc és szerzői jogok

A projektben használt csomagok (fitz, easyocr, numpy, stb.) nyílt forráskódúak, és az adott csomagok saját licencfeltételei érvényesek rájuk. A projektet szabadon felhasználhatja, módosíthatja és terjesztheti a megfelelő licencfeltételek betartásával. Kérjük, hogy a projekt használata során tartsa tiszteletben az eredeti szerzők jogait, és hivatkozzon a forrásra, ha szükséges.
