import os, subprocess

def clear_console() -> None:
   """ Limpa o console independente do OS """
   subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)