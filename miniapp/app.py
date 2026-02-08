from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
import os

# ===== APP =====
app = Flask(__name__, template_folder='templates', static_folder='static')

# ===== TELEGRAM НАСТРОЙКИ (ЗАМЕНИ НА СВОИ) =====
BOT_TOKEN = "7766253456:AAHBe6H9d1XbQvK7b5mL8hKzX1qP0rS2tU0"  # Твой токен бота
ADMIN_CHAT_ID = "641652464"  # Твой chat_id

# ===== API =====
@app.route('/api/add-city', methods=['POST'])
def add_city():
    data = request.get_json(silent=True)
    name = data.get('name')
    slug = data.get('slug')
    
    if not name or not slug:
        return jsonify({'error': 'name and slug required'}), 400
        
    send_telegram(f"🏙️ НОВЫЙ ГОРОД\n{name} ({slug})")
    return jsonify({'status': 'ok'})

@app.route('/api/suggest', methods=['POST'])
def suggest():
    data = request.get_json(silent=True)
    
    message = f"""
🏙️ НОВОЕ ПРЕДЛОЖЕНИЕ
Тип: {data.get('type', 'неизвестно')}
Город: {data.get('city', 'не указан')}
Название: {data.get('title', 'не указано')}
От: {data.get('nickname', 'Гость')} ({data.get('user_id', 'guest')})
Описание: {data.get('description', 'не указано')}
    """
    
    send_telegram(message.strip())
    return jsonify({'status': 'ok', 'message': 'Отправлено админу!'})

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        'chat_id': ADMIN_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    })

@app.route('/api/cities')
def get_cities():
    # Пока пусто - добавляй вручную в админке или через /api/add-city
    return jsonify([
        {'name': 'Новосибирск', 'slug': 'novosibirsk'},
        {'name': 'Москва', 'slug': 'moscow'}
    ])

@app.route('/api/locations/<city_slug>')
def get_locations(city_slug):
    # Тестовые данные (добавляй в админке)
    data = {
        'novosibirsk': [{
            'title': 'Опера театр',
            'desc': 'Красивейшее здание',
            'themes': ['popular'],
            'photos': ['oper1.jpg', 'oper2.jpg']
        }],
        'moscow': [{
            'title': 'Красная площадь',
            'desc': 'Сердце России',
            'themes': ['popular'],
            'photos': ['redsquare1.jpg']
        }]
    }
    return jsonify(data.get(city_slug, []))

@app.route('/api/photo-suggest', methods=['POST'])
def photo_suggest():
    send_telegram("📸 Новые фото на модерацию! (фото временно не загружаются)")
    return jsonify({'success': True})

# ===== SITE =====
@app.route("/")
def index():
    return render_template("index.html")

# ===== STATIC & PHOTOS =====
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/photos/<path:filename>')
def photos_files(filename):
    return send_from_directory('photos', filename)

# ===== ADMIN (только для чтения) =====
@app.route("/admin")
def admin():
    return "Админка отключена на Vercel. Используй Telegram."

if __name__ == "__main__":
    print("🚀 http://localhost:8000/")
    app.run(host="0.0.0.0", port=8000, debug=True)



