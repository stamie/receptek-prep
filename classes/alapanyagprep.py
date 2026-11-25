import json
import re
from pathlib import Path

class alapanyagprep:
    @staticmethod
    def alapanyagprep( fileName ):
        kategoriak = []
        alapanyagok = []
        nemAlapanyagok = []
        data = []
        with open(str(fileName), "r", encoding="utf-8") as f:
            data = json.load(f)
        for alapanyag_e in data:
            if re.match('#', alapanyag_e) and alapanyag_e not in kategoriak:
                kategoriak.append(alapanyag_e)
            else :
                alapanyagprep.alapanyagba(alapanyag_e, alapanyagok, nemAlapanyagok)
        outputFile = Path('../szurt_alapanyagok.json')
        with outputFile.open("w", encoding="utf-8") as f:
            json.dump(alapanyagok, f, ensure_ascii=False, indent=2)

        outputFile = Path('../szurendo_kategioriak.json')
        with outputFile.open('w', encoding="utf-8") as f:
            json.dump(kategoriak, f, ensure_ascii=False, indent=2)
        outputFile = Path('../nem_alapanyagok.json')
        with outputFile.open('w', encoding="utf-8") as f:
            json.dump(nemAlapanyagok, f, ensure_ascii=False, indent=2)
        
    
    @staticmethod
    def alapanyagba(kerdeseElem, alapanyagok, nem_alapanyagok) :
        alapanyagok_ = kerdeseElem.split()
        for alapanyag in alapanyagok_ : 
            if alapanyag not in nem_alapanyagok and alapanyag not in alapanyagok:
                valasz = input ('alapanyag-e: ' + alapanyag + ' (I/N)')
                if valasz == 'I':
                    alapanyagok.append(alapanyag)
                else:
                    nem_alapanyagok.append(alapanyag)

alapanyagprep.alapanyagprep('../alapanyag.json')