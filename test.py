def main(player):
    if exec('"%s" == "P1"'%player):
        print("ja")
    else:
        print("nee")


main("P1")