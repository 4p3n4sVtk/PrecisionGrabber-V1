# PrecisionGrabber-V1

## :warning: Alerta legais

Este projeto foi desenvolvido com fins educacionais e deve ser utilizado **apenas por pessoas que possuem pleno conhecimento das implicações legais e éticas de seus atos**. O uso inadequado deste software pode acarretar em consequências legais, e a responsabilidade pelo uso é inteiramente do usuário. A utilização deste projeto é estritamente restrita a **ambientes controlados e para fins de utilidade legal, como investigações digitais autorizadas**.


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
```
