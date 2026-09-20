import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import csv
from typing import List, Dict

from src.models.guest import Guest
from src.models.status_type import Status_Type
from src.models.class_only_method import ClassOnlyMethod

class LobbyManager:
   def __init__(self):
      self._root = Path(__file__).resolve().parents[2]
      self._fields_label = ['nome', 'codigo', 'status', 'entrada_em']
      self._txt_file = self._root / 'src' / 'data' / 'convidados.txt'
      self._csv_file = self._root / 'src' / 'data' / 'lista_eventos.csv'
      self._encoding_new_line = {'encoding': 'UTF-8', 'newline': ''}

      self.get_guests_list()

   def get_guests_list(self):
      if self._csv_file.is_file():
         # self.show_guest_list(self._csv_file)
         return
      
      try:
         guest_list = []

         with open (self._txt_file, 'r', **self._encoding_new_line) as file:
            for gst in file:
               name = gst.strip()

               if name:
                  guest = Guest(name)

                  infos = [guest.guest_name(), guest.guest_code(), guest.status, None if guest.status == Status_Type.PENDING.value else guest.confirmation_date]
                  structure = zip(self._fields_label, infos) # Cria o dicionario associando cada chave de fields_label ao seu valor em infos

                  guest_list.append(dict(structure)) 

         self.format_guest_list(self._csv_file, guest_list)
         # self.show_guest_list(guest_list)

      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except Exception as error:
         print(f'❌ Nao foi possivel executar a acao. {error} ❌')

   def format_guest_list(self, dir: str, guest_list: List[Dict]):
      try:
         with open(dir, 'w', **self._encoding_new_line) as file:

            writer = csv.DictWriter(file, fieldnames=self._fields_label)
            writer.writeheader()
            writer.writerows(guest_list)

            print(f'✅ Arquivo {Path(file.name).name} criado com sucesso. ✅\n')
      except FileNotFoundError as fileNotFoundError:
            print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except IOError as error:
         print(f'❌ Nao foi possivel criar o arquivo: {error} ❌')

   def read_csv_file(self):
      try:
         with open(self._csv_file, 'r', **self._encoding_new_line) as file:
            reader = csv.DictReader(file)
            reader = list(reader)

            return reader
      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
         
   def show_guest_list(self, list: List[Dict], status: Status_Type = Status_Type.ALL):
      found_guests = '✔️  Convidados encontrados: ✔️'
      status_emoji = '⌛' if status.value == 'PENDENTE' else '✅️'
      status_message = f'{status_emoji} Filtrando usuarios com status: {status.value} {status_emoji}'
      message = found_guests if status.value == 'TODOS' else status_message

      print(f'{message} \n')

      guests = list if status.value == 'TODOS' else [guest for guest in list if guest['status'] == status.value]

      for guest in guests:
         # enter_at = f", {guest['entrada_em']}" if guest['status'] == Status_Type.CONFIRMED.value else ""

         # print(f'{guest['nome']}, {guest['codigo']}, {guest['status']}{enter_at}')
         guest = Guest(guest['nome'])
         print(guest.guest_info())

   def guests_list(self, status: Status_Type = Status_Type.ALL):
      file = self.read_csv_file()

      self.show_guest_list(file, status)

   def guest_code(self, code:str):
      list = self.read_csv_file()
  
      guests = [guest for guest in list if guest['codigo'] == code.upper()]

      for guest in guests:
         guest = Guest(guest['nome'])
         print(guest.guest_info())


   def change_guest_status(self, code: str, status: Status_Type):
      new_status = Status_Type.CONFIRMED.value if status.value != Status_Type.CONFIRMED.value else Status_Type.PENDING.value