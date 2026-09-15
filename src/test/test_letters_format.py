import pytest
from src.utils.letter_format import name_code

def test_simple_name():
   assert name_code('Luffy') == 'LUFY'
   assert name_code('Law') == 'LAAW'

def test_full_name():
   assert name_code('Monkey D. Luffy') == 'MOFY'
   assert name_code('Tragalfar D. Watter Law') == 'TRAW'