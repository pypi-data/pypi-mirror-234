import PyPDF2
import docx

class DocReader:

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        if(self.file_path.endswith('.pdf')):
            self.content = self.load_pdf_text()
        elif(self.file_path.endswith('.doc') or self.file_path.endswith('.docx')):
            self.content = self.load_docs_text()
        

    def load_pdf_text(self):
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def load_docs_text(self):
        doc = docx.Document(self.file_path)
        # Extract text from paragraphs in the document
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def get_content(self):
        return(self.content)

    