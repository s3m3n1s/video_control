from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
from app import app

mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "turel/contol"


@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json()
    if 'down' in data:
        try:
            if data['right']:
                publish.single(mqtt_topic + "/horizontal/right", payload=str(data['right']),
                               hostname=mqtt_broker_host, port=mqtt_broker_port)
            if data['left']:
                publish.single(mqtt_topic + "/horizontal/left", payload=str(data['left']),
                               hostname=mqtt_broker_host, port=mqtt_broker_port)
            if data['up']:
                publish.single(mqtt_topic + "/vertical/up", payload=str(data['up']),
                               hostname=mqtt_broker_host, port=mqtt_broker_port)
            if data['down']:
                publish.single(mqtt_topic + "/vertical/down", payload=str(data['down']),
                               hostname=mqtt_broker_host, port=mqtt_broker_port)

            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    elif 'shot' in data:
        try:
            publish.single(mqtt_topic + "/fire", payload=str(data['shot']),
                           hostname=mqtt_broker_host, port=mqtt_broker_port)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
