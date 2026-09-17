def first_two_letters(name: str):
   return name[0:2]

def last_two_letters(name: str):
   return name[-2:]

def name_code(name: str):
   name_split = name.split()
   initial_name = name_split[0]
   final_name = name_split[-1] if len(name_split) >= 2 else initial_name

   initial = first_two_letters(initial_name)
   final = last_two_letters(final_name)

   code = f'{initial}{final}'.upper()
   
   return code