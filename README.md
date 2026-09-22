# Sistema de gerenciamento de convidados

A proposta desse projeto e cumprir o desafio proposto no encerramento dos Modulos de 'Base do Python 🐍' com suas especificações. 

### Foram instaladas as seguintes dependencias:
```js
   arrow    : Para manipular data e hora
   poethepoe: Para facilitar a execucao de script (venv e test)
```

# 🎯 Objetivo 🎯

## 👨‍💻 Criar um programa que: 

1️⃣ Lê uma lista bruta de nomes a partir de um arquivo TXT2. 

2️⃣ Gera códigos de identificação automáticos através de fatiamento de strings

3️⃣ Salva e gerencia os dados de forma persistente em um arquivo CSV

4️⃣ Executa um sistema interativo em loop no terminal para controle de portaria

5️⃣ Resolve conflitos de homônimos de forma inteligente

6️⃣ Permite reversão de status e geração de relatórios por comandos administrativos

7️⃣ Garante a integridade do sistema por meio de testes unitários automatizados

## 📋 Requisitos do projeto
✅️ Classe Convidado com atributos privados e propriedades (getters)

✅️ Classe GerenciadorPortaria para controlar o banco de dados e as buscas

✅️ Método de importação automatizada de TXT para CSV com aviso de sobrescrita

✅️ Algoritmo específico para geração de códigos em letras maiúsculas

✅️ Sistema de busca por termo aproximado (case-insensitive)

✅️ Mecanismo de seleção numerada para casos de múltiplos resultados encontrados

✅️ Registro de data e horário de entrada em tempo real via módulo datetime (usado a biblioteca arrow)

✅️ Comandos administrativos dedicados: total, confirmados, pendentes e pendente <termo>

✅️ Tratamento completo de exceções (try/except) para arquivos ausentes ou comandos inválidos

✅️ Mínimo de 5 testes unitários

✅️ Type hints declarados em assinaturas de funções e métodos

✅️ Docstrings em classes, métodos e funções

## 🗂️ Estrutura esperada
```js
projeto/
├── main.py                # Loop interativo da portaria (Interface CLI)
├── portaria.py (lobby.py) # Entidades, regras de negócio e persistência
├── test_portaria.py       # Testes unitários automatizados
├── convidados.txt         # Arquivo de entrada (Nomes brutos)
└── lista_eventos.csv      # Banco de dados persistido do evento
```

## 🗂️ Estrutura do projeto
```js
guests_check_in/
├── src/                       # Pasta raiz do projeto
│   ├── data/                    # Pasta para armazenar os arquivos
│   │   ├── convidados.txt          # Arquivo de entrada (Nomes brutos)
│   │   └── lista_eventos.csv       # Banco de dados persistido do evento
│   ├── models/                  # Pasta para armazenar os arquivos de class
│   │   ├── guest.py                # Arquivo para class Guest com seus Methods 
│   │   ├── lobby.py                # Arquivo para class Guest com seus Methods 
│   │   └── status_type.py          # Arquivo centralizar os valores de status disponiveis 
│   ├── test/                    # Pasta para armazenar o arquivo de teste
│   │   └── test_lobby.py           # Testes unitários automatizados
│   └── utils/                   # Pasta para armazenar os arquivos de utils
│       ├── __init__.py             # Arquivo para agilizar a importacao das funcoes 
│       ├── clear_console.py        # Arquivo para limpar o console
│       └── text_format.py          # Arquivo para formatar strings (remover acentor, gerar codigo de Guest)
├── .gitignore                 # Arquivo para nao serem enviados ao repositorio git 
├── main.py                    # Loop interativo da portaria (Interface CLI)
├── pyproject.toml             # Arquivo para simplificar na hora de iniciar o virtual ambient & rodar os testes (usando poe + venv/test)
├── README.md                  # Arquivo para documentar o projeto 
└── requirements.txt           # Arquivo com todas as depencias usadas no projeto
```

## 📝 Especificações
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

## 📌 Desafios extras
1️⃣ Acompanhantes Limitados: Permitir ler um número de acompanhantes permitidos por linha no TXT (Ex: Felipe Silva, 2) e controlar o saldo de entradas vinculadas àquele código principal.

2️⃣ Exportar Histórico Final: Adicionar o comando administrativo exportar que escreve um relatório estruturado resumindo os dados do evento.

----

## 💻 Configuração do Ambiente e Instalação
### 1️⃣. Criar e Ativar o Ambiente Virtual (venv)

#### No Windows:

```js
   python -m venv venv

   .\venv\Scripts\activate
```

#### No Linux/macOS:

```js
   python3 -m venv venv

   source venv/bin/activate
```

### 2️⃣ Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```js
   pip install -r requirements.txt
```

### 3️⃣ Executar o Projeto
Para iniciar a interface interativa de controle de portaria no terminal:

```js
   python main.py
```

### 4️⃣ Executar os Testes Automatizados
O projeto utiliza o pytest para a validação dos métodos da classe LobbyManager por meio de mocks (evitando alteração nos arquivos reais durante a execução dos testes).

Você pode executar os testes de duas formas:

#### Opção 🅰️: Usando o Poe (Poe the Poet)
Caso tenha a biblioteca poethepoet instalada no ambiente, utilize a task declarada no pyproject.toml:

```js
   poe test
```

#### Opção 🅱️: Comando Nativo
Executando diretamente pelo módulo do pytest:

```js
   python -m pytest
```