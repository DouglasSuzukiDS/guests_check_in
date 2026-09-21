import unicodedata

def first_two_letters(name: str):
   return name[0:2]

def last_two_letters(name: str):
   return name[-2:]

def remove_accents(name: str) -> str:
   # Normaliza a string decompondo os acentos dos caracteres (ex: 'á' vira 'a' + '´')
   nfkd = unicodedata.normalize('NFKD', name)

   # Filtra mantendo apenas os caracteres que não são marcas de acentuação (Mn)
   return "".join([c for c in nfkd if not unicodedata.combining(c)])

def name_code(name: str):
   name_without_accents = remove_accents(name)
   name_split = name_without_accents.split()
   initial_name = name_split[0]
   final_name = name_split[-1] if len(name_split) >= 2 else initial_name

   initial = first_two_letters(initial_name)
   final = last_two_letters(final_name)

   code = f'{initial}{final}'.upper()
   
   return code