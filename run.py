from flask import Flask, request, jsonify
import paho.mqtt.publish as publish

from app import app



mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "turel/contol"


@app.route('/send_command', methods=['POST'])
def send_command():
    try:
        data = request.get_json()

        # Отправка данных в MQTT брокер
        publish.single(mqtt_topic, payload=str(data), hostname=mqtt_broker_host, port=mqtt_broker_port)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
