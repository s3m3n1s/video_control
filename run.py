from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import paho.mqtt.client as client
from app import app

mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "turel/contol"


mqtt_client = client.Client()
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
mqtt_send = mqtt_client.publish


@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json()
    if 'down' in data:
        try:
            if data['right']:
                mqtt_send(mqtt_topic + "/horizontal/right", payload=str(data['right']))
            if data['left']:
                mqtt_send(mqtt_topic + "/horizontal/left", payload=str(data['left']))
            if data['up']:
                publish.single(mqtt_topic + "/vertical/up", payload=str(data['up']))
            if data['down']:
                publish.single(mqtt_topic + "/vertical/down", payload=str(data['down']))

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
