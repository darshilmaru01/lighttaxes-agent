class FormAgent:
    name = ""

    def __init__(self, pdf_nav=None, llm=None):
        self.pdf = pdf_nav
        self.llm = llm

    def run(self, inputs: dict):
        raise NotImplementedError("Each agent must implement run()")