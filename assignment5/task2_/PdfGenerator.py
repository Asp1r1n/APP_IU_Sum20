from fpdf import FPDF


class PdfPrinter:
    pdf = FPDF()

    def __init__(self):
        self.pdf.set_font('Arial', 'B', 12)


    def print_dictionaries(self, *dictionaris: dict):
        self.pdf.add_page()

        for dict in dictionaris:
            self.pdf.cell(0, 10, " ", 0, 1, "L")
            self.__print_dictionary(dict)
            self.pdf.cell(0, 10, " ", 0, 1, "L")

    def __print_dictionary(self, dictionary: dict, offset = 1):
        for rec in dictionary.keys():
            txt = (" " * offset) + str(rec) + " : "
            if type(dictionary[rec]) is dict:
                self.pdf.cell(0, 10, txt + " ", 0, 1, "L")
                self.__print_dictionary(dictionary[rec], offset+1)
                self.pdf.cell(0, 10, " ", 0, 1, "L")
            else:
                if len(str(dictionary[rec]).split("\n")) == 1 :
                    txt += str(dictionary[rec])
                    self.pdf.cell(0, 10, txt, 0, 1)
                else:
                    txt += str('"')
                    self.pdf.cell(0, 10, txt, 0, 1)
                    for line in str(dictionary[rec]).split("\n"):
                        self.pdf.cell(0, 10, (" " * offset) + line, 0, 1)
                    self.pdf.cell(0, 10, (" " * offset) +'"', 0, 1)


    def save_file(self, filename : str):
        self.pdf.output(filename)