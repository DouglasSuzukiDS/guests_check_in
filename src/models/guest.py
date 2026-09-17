import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import name_code
from typing import Literal
import arrow
from src.models.status_type import Status_Type

class Guest:
   def __init__(self, name: str):
      self.__name = name
      self.__code = self.guest_code()
      self.status = Status_Type.PENDING.value if name != 'Trafalgar D. Water Law' else Status_Type.CONFIRMED.value
      self.confirmation_date = '' if name != 'Trafalgar D. Water Law' else arrow.now('America/Sao_Paulo').format('DD/MM/YYYY HH:mm:ss')

   def guest_name(self) -> str:
      return self.__name

   def guest_code(self)  -> str:
      return name_code(self.__name)

   def guest_new_status(self, code, status: Status_Type):
      if self.__code == code and self.status != status:
         self.status = status

         if(status == Status_Type.CONFIRMED.value):
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