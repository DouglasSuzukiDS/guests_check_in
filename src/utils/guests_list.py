import sys
from pathlib import Path
import csv
from typing import List, Dict

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.models.guest import Guest
from src.models.status_type import Status_Type

fields_label = ['nome', 'codigo', 'status', 'entrada_em']

def get_guests_list():
   root = Path(__file__).resolve().parents[2]
   txt_file = root / 'src' / 'data' / 'convidados.txt'
   csv_file = root / 'src' / 'data' / 'lista_eventos.csv'

   if csv_file.is_file():
      show_guest_list(csv_file)
      return
   
   try:
      guest_list = []

      with open (txt_file, 'r', encoding='UTF-8', newline='') as file:
         for gst in file:
            name = gst.strip()

            if name:
               guest = Guest(name)

               infos = [guest.guest_name(), guest.guest_code(), guest.status, None if guest.status == Status_Type.PENDING.value else guest.confirmation_date]
               structure = zip(fields_label, infos) # Cria o dicionario associando cada chave de fields_label ao seu valor em infos

               guest_list.append(dict(structure)) 

      format_guest_list(csv_file, guest_list)
      show_guest_list(csv_file)

   except FileNotFoundError:
      print(f'⚠️ Falha ao localizar arquivo base. ⚠️')
   except Exception as error:
      print(f'❌ Nao foi possivel executar a acao. {error} ❌')

def format_guest_list(dir: str, guest_list: List[Dict]):
   try:
      with open(dir, 'w', encoding='UTF-8', newline='') as file:

         writer = csv.DictWriter(file, fieldnames=fields_label)
         writer.writeheader()
         writer.writerows(guest_list)

         print(f'✅ Arquivo {Path(file.name).name} criado com sucesso. ✅\n')
   except FileNotFoundError:
         print(f'⚠️ Falha ao localizar arquivo base. ⚠️')
   except IOError as error:
      print(f'❌ Nao foi possivel criar o arquivo: {error} ❌')
   
def show_guest_list(dir: str):
   try:

      with open(dir, 'r', encoding='UTF-8', newline='') as file:
         print(f'🔄 Lendo arquivo CSV: {Path(file.name).name} 🔄 \n')

         reader = csv.DictReader(file)

         guests = list(reader)

         print(f'✔️  Convidados encontrados: ✔️ \n')

         for guest in guests:
            enter_at = f", {guest['entrada_em']}" if guest['status'] == Status_Type.CONFIRMED.value else ""

            print(f'{guest['nome']}, {guest['codigo']}, {guest['status']}{enter_at}')
   except FileNotFoundError:
         print(f'⚠️ Falha ao localizar arquivo base. ⚠️')

get_guests_list()