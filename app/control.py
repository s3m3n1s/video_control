from flask import request
from app import app

# import paho.mqtt.client as mqtt

# Код для управления MQTT-клиентом
# ...

@app.route('/send_command', methods=['POST'])
def send_command():
    # Получение данных от джойстика и отправка команды по MQTT
    # ...

    return 'OK'
