import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter
import pytesseract
from pdf2image import convert_from_path, pdfinfo_from_path
import fitz  # PyMuPDF
from PIL import Image
import io
from tqdm import tqdm
import threading
import sys
import os



ocr_thread = None
cancel_flag = False

def ocr_pdf(input_pdf_path, output_pdf_path, dpi=150, quality=50):
    global cancel_flag
    try:
        pdf_info = pdfinfo_from_path(input_pdf_path)
        total_pages = pdf_info["Pages"]
        doc = fitz.open()
        progressbar['maximum'] = total_pages
        
        #for page_number in tqdm(range(1, total_pages + 1), desc="Processing pages"):# Remove tqdm from loop
        for page_number in range(1, total_pages + 1):

            if cancel_flag:
                messagebox.showinfo("Cancelled", "OCR processing was cancelled.")
                return
            
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
            
            progress_var.set(page_number)
            progress_label.configure(text=f"{page_number}/{total_pages} pages processed")
            progressbar.update_idletasks()
        
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
        autofill_output_file(file_path)

def autofill_output_file(input_path):
    base, ext = os.path.splitext(input_path)
    suggested_output = f"{base}_searchable.pdf"
    output_entry.delete(0, tk.END)
    output_entry.insert(0, suggested_output)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def start_ocr():
    global ocr_thread, cancel_flag
    cancel_flag = False
    input_path = input_entry.get()
    output_path = output_entry.get()
    if not input_path or not output_path:
        messagebox.showwarning("Warning", "Please select both input and output file paths.")
        return
    ocr_thread = threading.Thread(target=ocr_pdf, args=(input_path, output_path), daemon=True)
    ocr_thread.start()

def cancel_ocr():
    global cancel_flag
    cancel_flag = True

# UI setup
window = customtkinter.CTk()
window.title("PDF OCR Tool")
window.geometry("400x600")
window.configure(bg="#e9a5a5")

customtkinter.CTkLabel(window, text="Input", font=("Arial", 14), text_color="#fff").place(x=150, y=70)
input_entry = customtkinter.CTkEntry(window, placeholder_text="choose the file", width=200, font=("Arial", 14))
input_entry.place(x=100, y=110)
customtkinter.CTkButton(window, text="Browse", command=select_input_file, width=95).place(x=150, y=150)

customtkinter.CTkLabel(window, text="Output", font=("Arial", 14), text_color="#fff").place(x=150, y=220)
output_entry = customtkinter.CTkEntry(window, placeholder_text="save as", width=195, font=("Arial", 14))
output_entry.place(x=100, y=260)
customtkinter.CTkButton(window, text="Browse", command=select_output_file, width=95).place(x=150, y=300)

customtkinter.CTkButton(window, text="START OCR", command=start_ocr, width=100, height=50, fg_color="#44fd63").place(x=150, y=350)

progress_var = tk.DoubleVar()
progressbar = ttk.Progressbar(window, variable=progress_var, maximum=100, mode='determinate', length=350)
progressbar.place(x=75, y=550)
progress_label = customtkinter.CTkLabel(window, text="0/0 pages processed", font=("Arial", 12), text_color="#fff")
progress_label.place(x=150, y=460)

customtkinter.CTkButton(window, text="CANCEL", command=cancel_ocr, width=95, fg_color="#e12d2d").place(x=150, y=500)

window.mainloop()
