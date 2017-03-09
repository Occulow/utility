import paho.mqtt.client as mqtt
import os
import ssl

cert_path = "."

USERNAME='team21'
with open('pass', 'r') as f:
    PASSWORD=f.read().strip()
HOST='openchirp.andrew.cmu.edu'
PORT=1883
KEEPALIVE=60

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(msg.topic.encode('utf-8'))+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)

    client.tls_set(os.path.join(cert_path, "ca-certificates.crt"), 
        cert_reqs=ssl.CERT_REQUIRED, 
        tls_version=ssl.PROTOCOL_TLSv1_2, 
        ciphers=None)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, PORT, KEEPALIVE)

    client.loop_forever()