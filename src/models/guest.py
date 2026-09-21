import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import arrow
from src.utils import name_code
from src.models.status_type import Status_Type

class Guest:
   def __init__(self, name: str, status: Status_Type = Status_Type.PENDING):
      self._name = name
      self._code = self.guest_code()
      self.status = status
      # self.confirmation_date = '' if status == 'PENDENTE' else arrow.now('America/Sao_Paulo').format('DD/MM/YYYY HH:mm:ss')
      self.status = Status_Type.PENDING.value if name != 'Trafalgar D. Water Law' else Status_Type.CONFIRMED.value
      self.confirmation_date = '' if name != 'Trafalgar D. Water Law' else arrow.now('America/Sao_Paulo').format('DD/MM/YYYY HH:mm:ss')
   
   def guest_name(self) -> str:
      """ O metodo retorna o nome Guest """
      return self._name

   def guest_code(self)  -> str:
      """ O metodo retorna o codigo Guest """
      return name_code(self._name)

   def guest_status(self) -> str:
      """ O metodo retorna o status Guest """
      return self.status

   def guest_new_status(self, code, status: Status_Type) -> None:
      """ 
         O metodo muda o status do Guest, adicionando ou nao a data e hora
      """
      
      if self._code == code and self.status != status.value:
         self.status = status.value

         if(status.value == Status_Type.CONFIRMED.value):
            date_now = arrow.now('America/Sao_Paulo')
            date_formatted = date_now.format('DD/MM/YYYY HH:mm:ss')

            self.confirmation_date = date_formatted
         else:
            self.confirmation_date = ''

   def guest_info(self) -> str:
      """ O metodo retorna as informacoes Guest """
      name = self._name
      code = self._code
      status = self.status
      confirmation = f',{self.confirmation_date}' if self.confirmation_date else ''

      return f'{name},{code},{status}{confirmation}'