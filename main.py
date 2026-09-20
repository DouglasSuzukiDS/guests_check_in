from src.models.lobby import LobbyManager
from src.models.status_type import Status_Type

lobby = LobbyManager()

def start():
   run = True
   
   options = [
      'Listar todos os convidadados ✔️',
      'Listar todos os convidadados com status PENDENTES ⌛',
      'Listar todos os convidadados com status CONFIRMADOS ✅️',
      'Pesquisar confidado pelo CODIGO 🔎',
      'Encerrar programa ❌'
   ]

   while run:
      print('\n📋✏️  ---------- Sistema de Gerenciamento de Convidados ----------  ✏️ 📋\n')

      for index, option in enumerate(options, start=1):
         print(f'{index}. {option}')

      select_option = input('\nDigite o numero para executar a acao: ')

      match select_option:
         case '1':
            lobby.guests_list()
         case '2':
            lobby.guests_list(Status_Type.PENDING)
         case '3':
            lobby.guests_list(Status_Type.CONFIRMED)
         case '4':
            print('Pesquisando por codigo')
         case '5':
            run = False
            print('Programa encerrado.')
         case _:
            print('Opcao invalida.')

start()