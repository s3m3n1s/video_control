from flask import request, jsonify
import paho.mqtt.client as client
from app import app

mqtt_broker_host = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "turel/contol"

mqtt_client = client.Client()
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)


@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json()
    if 'down' in data:
        try:
            if data['right']:
                mqtt_client.publish(mqtt_topic + "/horizontal/right", payload=str(data['right']))
            if data['left']:
                mqtt_client.publish(mqtt_topic + "/horizontal/left", payload=str(data['left']))
            if data['up']:
                mqtt_client.publish(mqtt_topic + "/vertical/up", payload=str(data['up']))
            if data['down']:
                mqtt_client.publish(mqtt_topic + "/vertical/down", payload=str(data['down']))

            return jsonify({"status": "success"})
        except Exception as e:
            mqtt_client.reconnect()
            # mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
            return jsonify({"status": "error", "message": str(e)})
    elif 'shot' in data:
        try:
            mqtt_client.publish(mqtt_topic + "/fire", payload=str(data['shot']))
            return jsonify({"status": "success"})
        except Exception as e:
            mqtt_client.reconnect()
            # mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
            return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
