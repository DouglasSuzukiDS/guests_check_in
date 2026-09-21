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
         print('Entrou')
         self.guests_list()
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
         enter_at = f", {guest['entrada_em']}" if guest['status'] == Status_Type.CONFIRMED.value else ""

         print(f'{guest['nome']}, {guest['codigo']}, {guest['status']}{enter_at}')

   def guests_list(self, status: Status_Type = Status_Type.ALL):
      file = self.read_csv_file()

      self.show_guest_list(file, status)

   def guest_by_code(self, code:str):
      file = self.read_csv_file()
      guest_list = []

      # list = [guest for guest in file if guest['codigo'] == code.upper()]

      # Seleciona os guests que possuem o codigo com um o index da posicao dele no arquivo CSV
      for i, guest in enumerate(file):
         guest_list.append({'index_in_file': i, **guest}) if code.upper() == guest['codigo'] else ''

      # Vai mostrar os guests com o mesmo codigo com o formato padrao, nome,codigo,status,entrada_em (se houver esse registro)
      
      print()
      print(f'🔎 Convidado(s) localizado(s): 🔎 \n')

      for i, guest in enumerate(guest_list, start=1):
         values = [
            guest['nome'],
            guest['codigo'],
            guest['status'],
         ]

         if guest['entrada_em']:
            values.append(guest['entrada_em'])
         
         guest_selected = f'{str(i) + ". " if len(guest_list) > 1 else ""}{",".join(values)}'
         print(guest_selected)

      return guest_list


   def change_guest_status(self, code: str, status: Status_Type):
      file = self.read_csv_file()
      guest_list = self.guest_by_code(code)

      selected = int(input(f'\nO codigo {code} foi localizado nos seguintes convidados. Qual deseja alterar o status? '))

      index_to_change = guest_list[selected - 1]['index_in_file'] 

      new_status = Status_Type.CONFIRMED if file[index_to_change]['status'] == Status_Type.PENDING.value else Status_Type.PENDING
      new_guest = Guest(guest_list[selected - 1]['nome'])
      new_guest.guest_new_status(code.upper(), new_status)

      file[index_to_change] = new_guest.guest_info()

      for item in file:
         print(item)

      print(guest_list[0])