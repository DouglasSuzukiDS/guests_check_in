import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.guests_list import format_guest_list

class LobbyManager:
   def __init__(self):
      pass

   def get_guests(self):
      format_guest_list()

lobby = LobbyManager()
print(lobby.get_guests())