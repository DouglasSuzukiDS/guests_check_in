from src.models.lobby import LobbyManager
from src.models.status_type import Status_Type

lobby = LobbyManager()

def start():
   run = True
   
   options = [
      'Listar todos os convidadados ✔️',
      'Listar todos os convidadados com status PENDENTES ⌛',
      'Listar todos os convidadados com status CONFIRMADOS ✅️',
      'Verificar a quantidade de convidados 🔢',
      'Adicionar novo convidado ➕',
      'Pesquisar convidado pelo CODIGO 🔎',
      'Trocar status do convidado pelo CODIGO 🔄',
      'Encerrar programa ❌'
   ]

   while run:
      print('\n📋✏️  ---------- Sistema de Gerenciamento de Convidados ----------  ✏️ 📋\n')

      for index, option in enumerate(options, start=1):
         print(f'{index}. {option}')

      select_option = input('\nDigite o numero para executar a acao: ')

      match select_option:
         case '1':
            lobby.show_guest_list()
         case '2':
            lobby.show_guest_list(Status_Type.PENDING)
         case '3':
            lobby.show_guest_list(Status_Type.CONFIRMED)
         case '4':
            lobby.calc_guest()
         case '5':
            name = input('Digite o nome do novo convidado: ')
            lobby.add_guest_csv_file(name)
         case '6':
            code = input('Digite o codigo do convidado: ')
            lobby.guest_by_code(code)
         case '7':
            code = input('Digite o codigo do convidado para mudar o status: ')
            lobby.change_guest_status(code)
         case '8':
            run = False
            print('Programa encerrado.')
         case _:
            print('Opcao invalida.')

start()