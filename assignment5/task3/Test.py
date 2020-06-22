from PdfGenerator import PdfPrinter


printer = PdfPrinter()
printer.print_dictionaries({"A" : { "A1" : "B1" , "A2":"B2"}, "V" : "C1"})
printer.print_bar_chart("test", "x","y", {"A":1,"B":2})
printer.save_file("change_fonts.pdf")