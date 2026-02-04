import pdfplumber

class PDFNavigator:
    def __init__(self, pdf_path: str):
        self.pdf = pdfplumber.open(pdf_path)

    def search(self, keyword: str, max_pages: int = 10):
        """
        Search for a keyword in the first N pages of the PDF.
        Returns list of {page, snippet}.
        """
        results = []
        for i, page in enumerate(self.pdf.pages[:max_pages]):
            text = page.extract_text() or ""
            if keyword.lower() in text.lower():
                results.append({
                    "page": i + 1,
                    "snippet": text[:1500]
                })
        return results