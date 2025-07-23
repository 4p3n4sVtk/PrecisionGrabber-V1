# PrecisionGrabber-V1

Este projeto foi desenvolvido como parte da disciplina de Investigação Digital, com o objetivo de construir uma aplicação capaz de registrar e armazenar logs de acesso de usuários em um banco de dados SQLite. A aplicação utiliza o Flask, um framework de desenvolvimento web em Python, e integra consultas geográficas de IPs para obter informações sobre a localização dos usuários, como país, cidade, ISP (provedor de internet) e coordenadas geográficas (latitude e longitude).

Além disso, a aplicação foi projetada para registrar informações sobre o **user-agent** (informações do navegador do usuário), o **referrer** (origem do acesso) e o **timestamp** (data e hora do acesso).

A coleta de dados ocorre de forma assíncrona, utilizando uma tarefa em segundo plano para não impactar o desempenho da aplicação. Essa arquitetura de back-end visa melhorar a performance, processando os dados sem bloquear a execução de outras requisições.

## Principais Funcionalidades:

- Registro de logs de acessos dos usuários (IP, user-agent, referrer).
- Consulta de geolocalização baseada no IP do usuário, com informações como:
  - País
  - Cidade
  - ISP (provedor de internet)
  - Latitude e longitude
- Armazenamento eficiente em um banco de dados SQLite.
- Execução de tarefas assíncronas para processar dados de forma não bloqueante.
- Middleware de proxy para garantir que informações corretas de IP sejam obtidas quando a aplicação estiver atrás de proxies ou balanceadores de carga.

## Tecnologias Utilizadas:

- **Flask:** Framework web em Python para a construção da aplicação.
- **SQLite:** Banco de dados leve utilizado para armazenar os logs de acesso.
- **Requests:** Biblioteca Python para fazer requisições HTTP à API de geolocalização.
- **Threading:** Para execução de tarefas em segundo plano.
- **Werkzeug:** Middleware para lidar com proxies e headers corretamente.

## Como rodar o projeto:

1. Clone o repositório:
   ```bash
   git clone https://github.com/4p3n4sVtk/PrecisionGrabber-V1
 ```
2. Instale as dependências:
   ```bash
pip install -r requirements.txt
 ```
3. Inicie o servidor Flask:
   ```bash
flask run

```
4. Acesse a aplicação pelo navegador em:
   ```bash
http://127.0.0.1:5000/
