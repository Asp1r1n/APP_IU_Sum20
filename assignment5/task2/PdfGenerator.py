from fpdf import FPDF


class PdfPrinter:
    pdf = FPDF()

    def __init__(self):
        self.pdf.set_font('Arial', 'B', 12)


    def print_dictionaries(self, *dictionaris : dict):
        self.pdf.add_page()

        for dict in dictionaris:
            self.pdf.cell(0, 10, "{", 0, 1, "L")
            self.__print_dictionary(dict)
            self.pdf.cell(0, 10, "}", 0, 1, "L")

    def __print_dictionary(self, dictionary : dict):
        for rec in dictionary.keys():
            txt = str(rec) + " : "
            if type(dictionary[rec]) is dict:
                self.pdf.cell(0, 10, txt + "{", 0, 1, "L")
                self.__print_dictionary(dictionary[rec])
                self.pdf.cell(0, 10, "}", 0, 1, "L")
            else:
                txt += str(dictionary[rec])
                self.pdf.cell(0, 10, txt, 0, 1, "L")


    def save_file(self):
        self.pdf.output("change_fonts.pdf")