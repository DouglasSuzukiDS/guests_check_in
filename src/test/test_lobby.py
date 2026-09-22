import pytest
from unittest.mock import patch, mock_open
from src.models.lobby import LobbyManager  
from src.models.status_type import Status_Type

@pytest.fixture
def mock_lobby():
   """Fixture que simula o LobbyManager sem ler arquivos do disco real."""
   with patch.object(LobbyManager, 'read_csv_file') as mock_read, \
      patch.object(LobbyManager, 'get_guests_list') as mock_get:
      
      mock_read.return_value = [
         {'nome': 'Monkey D. Luffy', 'codigo': 'LUFF', 'status': Status_Type.PENDING.value, 'entrada_em': ''},
         {'nome': 'Roronoa Zoro', 'codigo': 'ZORO', 'status': Status_Type.CONFIRMED.value, 'entrada_em': '21/09/2026 15:48:51'},
         {'nome': 'Nami', 'codigo': 'NAMI', 'status': Status_Type.PENDING.value, 'entrada_em': ''}
      ]
      
      lobby = LobbyManager()
      return lobby

# 1. Teste de Busca com Sucesso (Por Nome ou Código)
def test_search_guest_success(mock_lobby, capsys):
   results = mock_lobby.search_guest("luffy")
   
   assert len(results) == 1
   assert results[0]['nome'] == 'Monkey D. Luffy'
   assert results[0]['index_in_file'] == 0

# 2. Teste de Busca sem Resultados
def test_search_guest_not_found(mock_lobby):
   results = mock_lobby.search_guest("Inexistente")
   
   assert results is None

# 3. Teste do Cálculo de Totais e Status
def test_calc_guest(mock_lobby, capsys):
   mock_lobby.calc_guest()
   captured = capsys.readouterr()
   
   # Verifica se os valores impressos bateram com a fixture (3 total, 2 pendentes, 1 confirmado)
   assert "Total de convidados: 3" in captured.out
   assert f"PENDENTE: 2" in captured.out or "2" in captured.out
   assert f"CONFIRMADO: 1" in captured.out or "1" in captured.out

# 4. Teste de Inversão de Status do Convidado
@patch('src.models.lobby.Guest')
def test_generate_guest_with_new_status(mock_guest_cls, mock_lobby):
   # Simula a instância do Guest retornado
   mock_guest_instance = mock_guest_cls.return_value
   mock_guest_instance.guest_info.return_value = "Monkey D. Luffy,LUFF,CONFIRMADO(A),21/09/2026 21:00:00"

   guest_list = [{'index_in_file': 0, 'nome': 'Monkey D. Luffy', 'codigo': 'LUFF', 'status': 'PENDENTE', 'entrada_em': ''}]
   
   updated_file = mock_lobby.generate_guest_with_new_status(guest_list, selected=1)

   assert updated_file[0]['nome'] == 'Monkey D. Luffy'
   assert updated_file[0]['codigo'] == 'LUFF'
   assert updated_file[0]['status'] == Status_Type.CONFIRMED.value

# 5. Teste de Leitura de CSV utilizando Mock de Arquivo
def test_read_csv_file():
   csv_data = "nome,codigo,status,entrada_em\nTony Tony Chopper,CHOP,PENDENTE,\n"
   
   with patch.object(LobbyManager, 'get_guests_list'), \
      patch('builtins.open', mock_open(read_data=csv_data)):
      
      manager = LobbyManager()
      content = manager.read_csv_file()

      assert len(content) == 1
      assert content[0]['nome'] == 'Tony Tony Chopper'
      assert content[0]['codigo'] == 'CHOP'