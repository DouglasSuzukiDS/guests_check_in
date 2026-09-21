# Objetivo

## Criar um programa que:

1. Lê uma lista bruta de nomes a partir de um arquivo TXT2. 

2. Gera códigos de identificação automáticos através de fatiamento de strings

3. Salva e gerencia os dados de forma persistente em um arquivo CSV

4. Executa um sistema interativo em loop no terminal para controle de portaria

5. Resolve conflitos de homônimos de forma inteligente

6. Permite reversão de status e geração de relatórios por comandos administrativos

7. Garante a integridade do sistema por meio de testes unitários automatizados

## Requisitos do projeto
[✅️] Classe Convidado com atributos privados e propriedades (getters)

[✅️] Classe GerenciadorPortaria para controlar o banco de dados e as buscas

[✅️] Método de importação automatizada de TXT para CSV com aviso de sobrescrita

[✅️] Algoritmo específico para geração de códigos em letras maiúsculas

[ ] Sistema de busca por termo aproximado (case-insensitive)

[✅️] Mecanismo de seleção numerada para casos de múltiplos resultados encontrados

[✅️] Registro de data e horário de entrada em tempo real via módulo datetime (usado a biblioteca arrow)

[✅️] Comandos administrativos dedicados: total, confirmados, pendentes e pendente <termo>

[✅️] Tratamento completo de exceções (try/except) para arquivos ausentes ou comandos inválidos

[ ] Mínimo de 5 testes unitários

[✅️] Type hints declarados em assinaturas de funções e métodos

[✅️] Docstrings em classes, métodos e funções

## Estrutura esperada
```js
projeto/
├── main.py                # Loop interativo da portaria (Interface CLI)
├── portaria.py (lobby.py) # Entidades, regras de negócio e persistência
├── test_portaria.py       # Testes unitários automatizados
├── convidados.txt         # Arquivo de entrada (Nomes brutos)
└── lista_eventos.csv      # Banco de dados persistido do evento
```

## Especificações
TXT de entrada obrigatório **(convidados.txt)**
```js
Felipe Silva
Lucas da Silva
Arthur
Ana Maria
Ana Júlia
```

CSV gerado de saída/persistência (lista_eventos.csv)
```js
nome,codigo,status,entrada_em
Felipe Silva,FELVA,Confirmado,11/07/2026 07:45:12
Lucas da Silva,LUCVA,Pendente,
Arthur,ARTUR,Pendente,
Ana Maria,ANAIA,Confirmado,11/07/2026 07:46:01
Ana Júlia,ANAIA,Pendente,
```

## Desafios extras
1. Acompanhantes Limitados: Permitir ler um número de acompanhantes permitidos por linha no TXT (Ex: Felipe Silva, 2) e controlar o saldo de entradas vinculadas àquele código principal.

2. Exportar Histórico Final: Adicionar o comando administrativo exportar que escreve um relatório estruturado resumindo os dados do evento.