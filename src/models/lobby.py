import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import csv
from typing import List, Dict, Optional

from src.models.guest import Guest
from src.models.status_type import Status_Type
from src.utils.text_format import remove_accents

class LobbyManager:
   def __init__(self):
      self._root = Path(__file__).resolve().parents[2]
      self._fields_label = ['nome', 'codigo', 'status', 'entrada_em']
      self._txt_file_src = self._root / 'src' / 'data' / 'convidados.txt'
      self._csv_file_src = self._root / 'src' / 'data' / 'lista_eventos.csv'
      self._encoding_new_line = {'encoding': 'UTF-8', 'newline': ''}

      self._csv_file_content = self.read_csv_file()
      self.get_guests_list()

   def get_guests_list(self) -> None:
      """
         Metodo responsavel por ler o arquivo cvs ou pedir parar com os dados extraido do aruqivo txt
      """
      
      try:
         guest_list = []

         with open (self._txt_file_src, 'r', **self._encoding_new_line) as file:
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

   def write_csv_file(self, dir: str, guest_list: List[Dict], update_status: bool = False) -> None:
      """
         Metodo responsavel por criar/escrever o arquivo csv
      """
      try:
         with open(dir, 'w', **self._encoding_new_line) as file:

            writer = csv.DictWriter(file, fieldnames=self._fields_label)
            writer.writeheader()
            writer.writerows(guest_list)

            created_file = f'✅ Arquivo {Path(file.name).name} criado com sucesso. ✅\n' 
            updated_file = f'\n✅ Arquivo {Path(file.name).name} atualizado com sucesso. ✅\n' 
            message = updated_file if update_status else created_file
            print(message)
      except FileNotFoundError as fileNotFoundError:
            print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except IOError as error:
         print(f'❌ Nao foi possivel criar o arquivo: {error} ❌')

   def read_csv_file(self) -> List[Dict]:
      """
         Metodo responsavel por ler o arquivo csv
      """
      try:
         with open(self._csv_file_src, 'r', **self._encoding_new_line) as file:
            reader = csv.DictReader(file)
            reader = list(reader)

            return reader
      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')

   def add_guest_csv_file(self, name: str) -> None:
      """
         Metodo responsavel por adicionar um novo convidado no arquivo csv
      """
      try:
         with open(self._csv_file_src, 'a', **self._encoding_new_line) as file:
            new_guest = Guest(name)
            # O retorno vem {name},{code},{status}{confirmation} entao o split separa por virgula
            guest_infos = new_guest.guest_info().split(',') 
      
            # Transforma no padrao do CSV {'nome': 'Trafalgar D. Water Law', 'codigo': 'TRAW', 'status': 'CONFIRMADO(A)', 'entrada_em': '20/09/2026 18:53:37'}
            formated_guest_infos = (dict(zip(self._fields_label, guest_infos))) 

            writer = csv.DictWriter(file, fieldnames=self._fields_label)
            writer.writerow(formated_guest_infos)

            message = f'\n➕ Convidado registrado na lista. ➕' 

            print(message)
      except FileNotFoundError as fileNotFoundError:
         print(f'⚠️  Falha ao localizar arquivo base. ⚠️ {fileNotFoundError}')
      except IOError as error:
         print(f'❌ Nao foi possivel adicionar o novo usuario: {error} ❌')

   def calc_guest(self) -> None:
      """
         Metodo responsavel por calcular a quantidade de convidados, mostrando o total, pendentes e confirmados
      """
      file = self._csv_file_content
      total = len(file)
      pending = 0
      confirmed = 0

      for guest in file:
        if guest['status'] == Status_Type.PENDING.value: 
           pending += 1
        else: 
           confirmed += 1

      guests_total = f'🔢 Total de convidados: {total} 🔢'
      guests_pending = f'⌛ Total de convidados pendentes com status {Status_Type.PENDING.value}: {pending} ⌛'
      guests_confirmed  = f'✅️ Total de convidados com status {Status_Type.CONFIRMED.value}: {confirmed} ✅️'

      print(f'\n{guests_total}, \n{guests_pending}, \n{guests_confirmed}')

   def show_guest_list(self, list: Optional[List[Dict]] = None, status: Status_Type = Status_Type.ALL) -> None:
      """
         Metodo responsavel por lista os convidados
      """

      if list == None:
         list = self._csv_file_content

      if len(list) <= 1:
         msg_emoji = '⌛' if status.value == Status_Type.PENDING.value else '🚫'

         msg_status = f' com status {status.value} ' if status.value != Status_Type.ALL.value else " "
         message = f'\n{msg_emoji} Poxa voce ainda nao possui nenhum convidado{msg_status}{msg_emoji}'

         print(message)
         return

      found_guests = '✔️  Convidados encontrados: ✔️'
      status_emoji = '⌛' if status.value == 'PENDENTE' else '✅️'
      status_message = f'{status_emoji} Filtrando usuarios com status: {status.value} {status_emoji}'
      message = found_guests if status.value == 'TODOS' else status_message

      print(f'\n {message} \n')

      guests = list if status.value == 'TODOS' else [guest for guest in list if guest['status'] == status.value]

      for guest in guests:
         enter_at = f", {guest['entrada_em']}" if guest['status'] == Status_Type.CONFIRMED.value else ""

         print(f'{guest['nome']}, {guest['codigo']}, {guest['status']}{enter_at}')

   def guest_by_code(self, code:str) -> List[Dict]:
      """
         Metodo responsavel por retornar convidados pesquisados pelo codigo
      """
      file = self._csv_file_content
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

   def search_guest(self, term: str) -> List[Dict]:
      """
         Metodo faz uma busca do Guest pelo termo, seja pelo NOME ou CODIGO
      """
      file = self._csv_file_content
      guest_list = []

      # Seleciona os guests que possuem o codigo com um o index da posicao dele no arquivo CSV
      for i, guest in enumerate(file):
         guest_name = remove_accents(guest['nome'].lower())
         guest_code = guest['codigo'].lower()
         term_lower = term.lower()
         
         guest_list.append({'index_in_file': i, **guest}) if term_lower in guest_name or term_lower in guest_code else ''

      # Vai mostrar os guests com o mesmo codigo com o formato padrao, nome,codigo,status,entrada_em (se houver esse registro)
            
      print()

      if len(guest_list) == 0:
         print(f'🚫 Poxa, nao foi localizado nenhum convidado com o termo digitado: {term} 🚫')
         return 
      
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

   # Metodo responsavel por atualizar o status do usuario e criar a lista
   def generate_guest_with_new_status(self, guest_list: List, selected: int) -> List[Dict]:
      """
         Metodo responsavel por tratar (gerar novo Guest, e mudar seu status) e adicionar esse Guest na posicao exata da list que ele ele foi encontrado
      """
      file = self._csv_file_content
      code = guest_list[selected - 1]['codigo'] 

      index_to_change = guest_list[selected - 1]['index_in_file'] 

      # Troca o status CONFIRMED para PENDING e vice versa
      new_status = Status_Type.CONFIRMED if file[index_to_change]['status'] == Status_Type.PENDING.value else Status_Type.PENDING

      # Cria o Guest com o nome pegando a posicao da guest_list (pode ter 1 ou mais retornos)
      new_guest = Guest(guest_list[selected - 1]['nome'])

      # Aqui sim faz a troca de status
      new_guest.guest_new_status(code.upper(), new_status)

      # O retorno vem {name},{code},{status}{confirmation} entao o split separa por virgula
      guest_infos = new_guest.guest_info().split(',') 
      # print(guest_infos)

      # Transforma no padrao do CSV {'nome': 'Trafalgar D. Water Law', 'codigo': 'TRAW', 'status': 'CONFIRMADO(A)', 'entrada_em': '20/09/2026 18:53:37'}
      formated_guest_infos = (dict(zip(self._fields_label, guest_infos))) 

      # No arquivo original, na posicao do item recebe os novos dados do usuario
      file[index_to_change] = formated_guest_infos 

      return file

   def change_guest_status(self, code: str) -> List[Dict]:
      """
         Metodo responsavel por recriar o arquivo csv o novo status do usuario
      """
      # guest_list = self.guest_by_code(code)
      guest_list = self.search_guest(code)

      if not guest_list:
         return

      selected = 1 # Para caso a lista so retorne 1 convidado, generate_guest_with_new_status ja calcula -1 para pegar a item[0] (1 posicao)

      if len(guest_list) > 1:
         selected = int(input(f'\nO codigo {code} foi localizado nos seguintes convidados. Qual deseja alterar o status? '))

      updated_file = self.generate_guest_with_new_status(guest_list, selected)

      # Cria/atualiza o usuario de fato 
      self.write_csv_file(self._csv_file_src, updated_file, True)

      print(f'✅️ Status do convidado(a) atualizado ✅️')

      self._csv_file_content = self.read_csv_file()