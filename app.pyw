import tkinter as tk
from tkinter import filedialog, messagebox
import pytesseract
from pdf2image import convert_from_path, pdfinfo_from_path
import fitz  # PyMuPDF
from PIL import Image
import io
from tqdm import tqdm
import threading

def ocr_pdf(input_pdf_path, output_pdf_path, dpi=150, quality=50):
    try:
        pdf_info = pdfinfo_from_path(input_pdf_path)
        total_pages = pdf_info["Pages"]
        doc = fitz.open()
        
        for page_number in tqdm(range(1, total_pages + 1), desc="Processing pages"):
            images = convert_from_path(input_pdf_path, first_page=page_number, last_page=page_number, dpi=dpi)
            image = images[0]
            
            text = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
            ocr_pdf = fitz.open("pdf", text)
            
            img_byte_arr = io.BytesIO()
            image = image.convert("RGB")
            image.save(img_byte_arr, format='JPEG', quality=quality)
            img_byte_arr = img_byte_arr.getvalue()
            
            img_pdf = fitz.open()
            rect = fitz.Rect(0, 0, image.width, image.height)
            page = img_pdf.new_page(width=image.width, height=image.height)
            page.insert_image(rect, stream=img_byte_arr)
            
            doc.insert_pdf(ocr_pdf)
            
            progress_var.set((page_number / total_pages) * 100)
            root.update_idletasks()
        
        doc.save(output_pdf_path, garbage=4, deflate=True)
        doc.close()
        messagebox.showinfo("Success", "OCR processing completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def start_ocr():
    input_path = input_entry.get()
    output_path = output_entry.get()
    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please select both input and output file paths.")
        return
    threading.Thread(target=ocr_pdf, args=(input_path, output_path), daemon=True).start()

# UI setup
root = tk.Tk()
root.title("PDF OCR Tool")
root.geometry("500x300")

progress_var = tk.DoubleVar()

tk.Label(root, text="Select PDF file:").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack()
tk.Button(root, text="Browse", command=select_input_file).pack(pady=5)

tk.Label(root, text="Save OCR PDF as:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack()
tk.Button(root, text="Browse", command=select_output_file).pack(pady=5)

tk.Button(root, text="Start OCR", command=start_ocr).pack(pady=10)

progress_bar = tk.Scale(root, variable=progress_var, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
progress_bar.pack(pady=10)

root.mainloop()
