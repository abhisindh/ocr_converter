![LOGO](https://raw.githubusercontent.com/abhisindh/ocr_converter/refs/heads/master/icon.ico)
# OCR PDF Tool

## Description
OCR PDF Tool is a Python-based application that converts scanned PDFs into searchable PDFs using Optical Character Recognition (OCR). The application provides a user-friendly GUI to select input PDFs, process them with OCR, and save the output as a searchable PDF. The tool utilizes `pytesseract` for OCR, `pdf2image` for PDF to image conversion, and `PyMuPDF` for handling PDFs.

## Features
- Convert scanned PDFs to searchable PDFs
- Simple and easy-to-use GUI
- Supports image compression for optimized output
- Multi-page PDF processing with progress tracking
- Works entirely offline

## Requirements
Before running the application, ensure you have the following installed:

- Python 3.x
- Tesseract OCR (Install from https://github.com/tesseract-ocr/tesseract)
- Required Python libraries:

```
pip install pytesseract pdf2image PyMuPDF pillow tqdm
```

## Installation and Usage

### 1. Clone the Repository
```
git clone https://github.com/abhisindh/ocr_converter
cd ocr_converter
```


### 2. Run the Application
```
python app.py
```

## Creating an Executable (Windows)
If you want to generate a standalone `.exe` file:
```
pyinstaller --onefile --windowed --icon=icon.ico --name=ocr_converter app.py
```
The `.exe` file will be generated in the `dist` folder.

## Notes
- Ensure `Tesseract` is properly installed and added to the system PATH.
- If encountering issues with OCR, verify `pytesseract.get_tesseract_cmd()` points to the correct `tesseract.exe` location.

## License
This project is open-source and licensed under the MIT License.

## Contributing
Pull requests and contributions are welcome! Feel free to fork the repository and submit your improvements.

## Author
[Your Name]  
GitHub: [your-github-profile](https://github.com/your-username)

