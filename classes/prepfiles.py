class prepfiles:

    # fájl beolvasása
    def read_files(index):
        with open(index + '.txt', 'r', encoding='utf-8') as file_:
            for row in file_:
                # A strip() eltávolítja a sówégi újsor karaktereket (\n)
                cleaned_row = row.strip() 
                