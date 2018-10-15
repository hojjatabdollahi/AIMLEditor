import re

def de_punctuate(input:str) -> str:
        return " ".join(re.sub(r'[^\w]', ' ', input).split()).upper()