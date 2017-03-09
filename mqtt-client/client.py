import paho.mqtt.client as mqtt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
cert = os.path.join(dir_path, 'foo.crt')

USERNAME='team21'
PASSWORD='BobsBurgers5598'
HOST='openchirp.andrew.cmu.edu'
PORT=1883
KEEPALIVE=60

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("gateway/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(cert)
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, PORT, KEEPALIVE)

    client.loop_forever()