
import matplotlib.pyplot as plt
from fpdf import FPDF
import numpy as np


class PdfPrinter:
    pdf = FPDF()

    def __init__(self):
        self.pdf.set_font('Arial', 'B', 12)

    def print_dictionaries(self, *dictionaris: dict):
        self.pdf.add_page()

        for dict in dictionaris:
            self.pdf.cell(0, 10, "{", 0, 1, "L")
            self.__print_dictionary(dict)
            self.pdf.cell(0, 10, "}", 0, 1, "L")

    def __print_dictionary(self, dictionary: dict):
        for rec in dictionary.keys():
            txt = str(rec) + " : "
            if type(dictionary[rec]) is dict:
                self.pdf.cell(0, 10, txt + "{", 0, 1, "L")
                self.__print_dictionary(dictionary[rec])
                self.pdf.cell(0, 10, "}", 0, 1, "L")
            else:
                txt += str(dictionary[rec])
                self.pdf.cell(0, 10, txt, 0, 1, "L")

    def print_bar_chart(self, name: str, xlable: str, ylable: str, dictionary: dict):
        objects = list(dictionary.keys())
        y_pos = np.arange(len(objects))
        performance = list(dictionary.values())

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel(ylable)
        plt.xlabel(xlable)
        plt.title(name)

        plt.savefig('tmp.png')

        self.pdf.image('tmp.png', w= 200, type='png')

    def save_file(self, filename: str):
        self.pdf.output(filename)
