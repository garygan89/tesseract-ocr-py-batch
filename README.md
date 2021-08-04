# Quick Start
 
A simple python script using Tesseract OCR engine to extract texts in batch images.

Put all images to `input` folder
Output will be store in `output` folder relative to the folder where you run this script.

1. Download Tesseract for Windows from https://github.com/UB-Mannheim/tesseract/wiki
Or use this latest one: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe
2. Add the default Tesseract installation path to System Environment `PATH` variable 
`PATH=c:\Program Files\Tesseract-OCR\`

OR modify the following in `ocr.py`
```
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```
3. Run the script and profit!
```
python3 ocr.py
```