import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import name_code
from typing import Literal
import arrow

Status_Type = Literal['PENDENTE', 'CONFIRMADO']

class Guest:
   def __init__(self, name: str):
      self.__name = name
      self.__code = self.guest_code()
      self.status = 'PENDENTE'
      self.confirmation_date = ''

   def guest_name(self) -> str:
      return self.__name

   def guest_code(self)  -> str:
      return name_code(self.__name)

   def guest_new_status(self, code, status: Status_Type):
      if self.__code == code and self.status != status:
         self.status = status

         if(status == 'CONFIRMADO'):
            date_now = arrow.now('America/Sao_Paulo')
            date_formatted = date_now.format('DD/MM/YYYY HH:mm:ss')

            self.confirmation_date = date_formatted
         else:
            self.confirmation_date = ''

   def guest_info(self) -> str:
      name = self.__name
      code = self.__code
      status = self.status
      confirmation = f',{self.confirmation_date}' if self.confirmation_date else ''

      return f'{name},{code},{status}{confirmation}'

if __name__ == "__main__":
   user = Guest("Luffy")
   print(user.guest_name())
   print(user.guest_code())
   print(user.guest_info())

   print('\n--------------- Trocando para Confirmado ---------------')
   print(user.guest_new_status(user.guest_code(), 'CONFIRMADO'))
   print(user.guest_info())
   print('--------------- XXXXXXXXXXXXXXXXXXXX ---------------\n')

   print('\n--------------- Trocando para pendente ---------------')
   print(user.guest_new_status(user.guest_code(), 'PENDENTE'))
   print(user.guest_info())
   print('--------------- XXXXXXXXXXXXXXXXXXXX ---------------\n')