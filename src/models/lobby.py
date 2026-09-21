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

         self.write_csv_file(self._csv_file, guest_list)
         # self.show_guest_list(guest_list)

      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except Exception as error:
         print(f'❌ Nao foi possivel executar a acao. {error} ❌')

   def write_csv_file(self, dir: str, guest_list: List[Dict], update_status: bool = False):
      try:
         with open(dir, 'w', **self._encoding_new_line) as file:

            writer = csv.DictWriter(file, fieldnames=self._fields_label)
            writer.writeheader()
            writer.writerows(guest_list)

            created_file = f'✅ Arquivo {Path(file.name).name} criado com sucesso. ✅\n' 
            updated_file = f'✅ Arquivo {Path(file.name).name} atualizado com sucesso. ✅\n' 
            message = updated_file if update_status else created_file
            print(message)
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

   def add_guest_csv_file(self, name: str):
      try:
         with open(self._csv_file, 'a', **self._encoding_new_line) as file:
            new_guest = Guest(name)
            # O retorno vem {name},{code},{status}{confirmation} entao o split separa por virgula
            guest_infos = new_guest.guest_info().split(',') 
      
            # Transforma no padrao do CSV {'nome': 'Trafalgar D. Water Law', 'codigo': 'TRAW', 'status': 'CONFIRMADO(A)', 'entrada_em': '20/09/2026 18:53:37'}
            formated_guest_infos = (dict(zip(self._fields_label, guest_infos))) 

            writer = csv.DictWriter(file, fieldnames=self._fields_label)
            writer.writerow(formated_guest_infos)

            message = f'➕ Convidado registrado na lista. ➕\n' 

            print(message)
      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except IOError as error:
         print(f'❌ Nao foi possivel adicionar o novo usuario: {error} ❌')
   
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

   # Funcao responsavel por atualizar o status do usuario e criar a lista
   def generate_guest_with_new_status(self, guest_list: List, code: str, selected: int):
      file = self.read_csv_file()
      guest_list = self.guest_by_code(code)

      index_to_change = guest_list[selected - 1]['index_in_file'] 

      # Troca o status CONFIRMED para PENDING e vice versa
      new_status = Status_Type.CONFIRMED if file[index_to_change]['status'] == Status_Type.PENDING.value else Status_Type.PENDING

      # Cria o Guest com o nome pegando a posicao da guest_list (pode ter 1 ou mais retornos)
      new_guest = Guest(guest_list[selected - 1]['nome'])

      # Aqui sim faz a troca de status
      new_guest.guest_new_status(code.upper(), new_status)

      # O retorno vem {name},{code},{status}{confirmation} entao o split separa por virgula
      guest_infos = new_guest.guest_info().split(',') 

      # Transforma no padrao do CSV {'nome': 'Trafalgar D. Water Law', 'codigo': 'TRAW', 'status': 'CONFIRMADO(A)', 'entrada_em': '20/09/2026 18:53:37'}
      formated_guest_infos = (dict(zip(self._fields_label, guest_infos))) 

      # No arquivo original, na posicao do item recebe os novos dados do usuario
      file[index_to_change] = formated_guest_infos 

      return file

   def change_guest_status(self, code: str):
      guest_list = self.guest_by_code(code)

      selected = 1 # Para caso a lista so retorne 1 convidado, generate_guest_with_new_status ja calcula -1 para pegar a item[0] (1 posicao)

      if len(guest_list) > 1:
         selected = int(input(f'\nO codigo {code} foi localizado nos seguintes convidados. Qual deseja alterar o status? '))

      updated_file = self.generate_guest_with_new_status(guest_list, code, selected)

      # Cria/atualiza o usuario de fato 
      self.write_csv_file(self._csv_file, updated_file, True)