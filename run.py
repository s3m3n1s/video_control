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
            publish.single(mqtt_topic+"/horizontal", payload=str(data['right'] if data['right'] else data['left']),
                           hostname=mqtt_broker_host, port=mqtt_broker_port)
            publish.single(mqtt_topic+"/vertical", payload=str(data['up'] if data['up'] else data['down']),
                           hostname=mqtt_broker_host, port=mqtt_broker_port)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    elif 'shot' in data:
        try:
            publish.single(mqtt_topic+"/fire", payload=str(data['shot']),
                           hostname=mqtt_broker_host, port=mqtt_broker_port)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
