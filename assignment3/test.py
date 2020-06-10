from decor import reflect


@reflect(word = 'if')
def fooo(a, b =''):
    """ This function does nothing useful
        :param bar1: description
        :param bar2: description
    """
    if True == True:
        print("Its ok")
    else:
        print("Ay-ya-ya-ya-Indiaaaaaaa")
        print("ruppy comes ruppy goes")
        print("give me my money")
        
    if False == True:
        print("We do american magic hear")
    else:
        print("And hear we do real work russian work")

    print(1)


if __name__ == "__main__":
    fooo(12, b = 'hello')
    
