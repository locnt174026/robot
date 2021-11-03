import json
import random
import time
from threading import Thread
import paho.mqtt.client as mqtt



def on_connect(client, obj, flags, rc):

    print("rc: " + str(rc))


def on_message(client, obj, msg):
    topic = msg.topic
    device_id = topic.split('/')[1]
    data = msg.payload
    print(f'Device {device_id} : {data}')


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# client = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

client_id = f'map-view-{random.randint(0, 1000)}'

#  + trong topic dai dien cho chuoi bat ky ,lister topic cac thiet bi gui vi tri device/{device_id}/location
topic_location = f'device/+/location'

broker = '127.0.0.1'
port = 1883
username = 'python-user'
password = '123'
# client_id khong được trùng
client = mqtt.Client(client_id)
client.username_pw_set(username, password)

# set callback function
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# client.on_log = on_log
client.connect(broker, port, 600)

client.subscribe(topic_location, 1)


client.loop_forever()
