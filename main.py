import sys
from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel

class PDFDecryptor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('PDF解密工具')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        self.file_label = QLabel('选择加密的PDF文件:')
        layout.addWidget(self.file_label)
        
        self.file_button = QPushButton('选择文件')
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)
        
        self.output_label = QLabel('选择解密后的PDF文件保存路径:')
        layout.addWidget(self.output_label)
        
        self.output_button = QPushButton('选择路径')
        self.output_button.clicked.connect(self.select_output_path)
        layout.addWidget(self.output_button)
        
        self.decrypt_button = QPushButton('开始解密')
        self.decrypt_button.clicked.connect(self.decrypt_pdf)
        layout.addWidget(self.decrypt_button)
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
        
        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择加密的PDF文件", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.file_path = file_path
            self.log.append(f'选择的文件: {file_path}')

    def select_output_path(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "选择解密后的PDF文件保存路径", options=options)
        if folder_path:
            self.output_path = folder_path
            self.log.append(f'保存路径: {folder_path}')

    def decrypt_pdf(self):
        if hasattr(self, 'file_path'):
            input_path = self.file_path
            
            if not hasattr(self, 'output_path'):
                output_path = "".join(input_path.split('.')[:-1]) + '_decrypted.pdf'
            else:
                output_path = f"{self.output_path}/{input_path.split('/')[-1].split('.')[0]}_decrypted.pdf"
            
            self.log.append('正在解密...')
            pdf_reader = self.load_pdf(input_path)
            if pdf_reader is None:
                self.log.append("未能读取内容")
            elif not pdf_reader.is_encrypted:
                self.log.append('文件未加密，无需操作')
            else:
                pdf_writer = PdfWriter()
                pdf_writer.append_pages_from_reader(pdf_reader)
                
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                self.log.append(f"解密文件已生成: {output_path}")
        else:
            self.log.append("请先选择PDF文件")
    
    def load_pdf(self, file_path):
        try:
            pdf_file = open(file_path, 'rb')
        except Exception as error:
            self.log.append('无法打开文件: ' + str(error))
            return None

        reader = PdfReader(pdf_file, strict=False)

        if reader.is_encrypted:
            try:
                reader.decrypt('')
            except Exception as error:
                self.log.append('无法解密文件: ' + str(error))
                return None
        return reader

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFDecryptor()
    ex.show()
    sys.exit(app.exec_())