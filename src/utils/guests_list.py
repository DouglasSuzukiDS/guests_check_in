import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.models.guest import Guest

def get_guests_list():
   root = Path(__file__).resolve().parents[2]
   data = root / 'src' / 'data' / 'convidados.txt'

   try:
      guest_list = []

      with open (data, 'r', encoding='UTF-8') as file:
         for gst in file:
            guest = Guest(gst)

            print(guest)
   except FileExistsError:
      print(f'Falha ao localizar arquivo base')

def format_guest_list():
   pass

if __name__ == "__main__":
    get_guests_list()