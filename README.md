# Hibrid PDF-ből Markdown átalakító

Ez a Python szkript egy fejlett eszköz, amely a PDF dokumentumokat Markdown formátumba alakítja. A szkript a hagyományos szövegextrakciót a beágyazott szöveg kinyeréséhez (a fitz könyvtár segítségével) kombinálja a képekből történő szövegfelismeréssel (OCR - easyocr használatával). Ez a hibrid megközelítés lehetővé teszi, hogy a szkript a beolvasott, kép-alapú PDF-ekben lévő szöveget is feldolgozza, így egy átfogó megoldást nyújt a dokumentumok digitalizálására.

## Főbb funkciók

- **Hibrid megközelítés**: Képes kinyerni a beágyazott szöveget és a képeken belül található szöveget is.
- **Többnyelvű támogatás**: A szkript automatikusan felismeri és feldolgozza a magyar és angol nyelvű szövegeket.
- **Pozíció alapú sorrendezés**: A kinyert szövegblokkokat a PDF-ben elfoglalt pozíciójuk alapján rendezi, ezzel megőrzi a dokumentum eredeti logikai szerkezetét.
- **Redundancia-kezelés**: Intelligens algoritmusok segítségével kiszűri a duplikált szövegeket, amelyek a hagyományos és az OCR extrakció során is megjelenhetnek.
- **Tartalomjegyzék generálása**: Létrehoz egy kattintható tartalomjegyzéket a Markdown fájl elején, amely segíti a navigációt az egyes oldalak között.
- **OCR-jelölés**: A képekből kinyert szövegeket **[OCR]** jelöléssel látja el, így könnyen megkülönböztethető a forrása.

## Használati útmutató

1. Telepítse a szükséges függőségeket:
   ```bash
   pip install -r requirements.txt
   ```


## Követelmények

- Python 3.8 vagy újabb
- Könyvtárak:
  - fitz
  - easyocr
  - numpy
  - PIL (Pillow)

## Példa kimenet

A generált Markdown fájl tartalmazza:
- A PDF dokumentum szöveges tartalmát logikai sorrendben.
- Kattintható tartalomjegyzéket.
- **[OCR]** jelöléssel ellátott szövegeket a képekből kinyert tartalomhoz.

## Licenc és szerzői jogok

- A projektben használt csomagok (fitz, easyocr, numpy, stb.) nyílt forráskódúak, és az adott csomagok saját licencfeltételei érvényesek rájuk.
- A projekt további felhasználásához és terjesztéséhez kérjük, tartsa be a használt csomagok licencfeltételeit.
