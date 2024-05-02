import os
from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog, Tk, StringVar, Label, Entry, Button

root = Tk()
root.title("PDF 처리 도구")

pdf_file_path = StringVar()
password = StringVar()

# PDF 파일 선택 함수
def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_file_path.set(file_path)

# PDF 파일 복호화 및 텍스트 파일 생성 함수
def decrypt_and_convert():
    pdf_file = pdf_file_path.get()
    pdf_pwd = password.get().encode()

    with open(pdf_file, "rb") as file:
        pdf_reader = PdfReader(file)
        if pdf_reader.is_encrypted:
            try:
                pdf_reader.decrypt(pdf_pwd)
                pdf_writer = PdfWriter()
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
                decrypted_file = os.path.splitext(pdf_file)[0] + "_decrypted.pdf"
                with open(decrypted_file, "wb") as output_file:
                    pdf_writer.write(output_file)
                print(f"PDF 파일이 성공적으로 복호화되었습니다: {decrypted_file}")

                text_content = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text()
                
                text_file = os.path.splitext(pdf_file)[0] + ".txt"
                with open(text_file, "w", encoding="utf-8") as output_file:
                    output_file.write(text_content)
                
                print(f"PDF 파일이 성공적으로 텍스트 파일로 변환되었습니다: {text_file}")
            except ValueError:
                print("비밀번호가 올바르지 않습니다.")
        else:
            print("PDF 파일이 암호화되어 있지 않습니다.")

# 텍스트 파일만 생성하는 함수
def convert_to_text():
    pdf_file = pdf_file_path.get()
    
    with open(pdf_file, "rb") as file:
        pdf_reader = PdfReader(file)
        text_content = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()
    
    text_file = os.path.splitext(pdf_file)[0] + ".txt"
    with open(text_file, "w", encoding="utf-8") as output_file:
        output_file.write(text_content)
    
    print(f"PDF 파일이 성공적으로 텍스트 파일로 변환되었습니다: {text_file}")

# GUI 구성 요소
Label(root, text="PDF 파일 선택:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=pdf_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="파일 선택", command=select_pdf_file).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="비밀번호:").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=password, show="*", width=20).grid(row=1, column=1, padx=10, pady=10)

Button(root, text="암호 해제 파일 및 텍스트 파일 생성", command=decrypt_and_convert).grid(row=2, column=0, padx=10, pady=10)
Button(root, text="바로 텍스트 파일 생성", command=convert_to_text).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()