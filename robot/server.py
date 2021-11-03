import json
import random
import time
from threading import Thread
import paho.mqtt.client as mqtt


def send_way(client, way, device_id):

    client.publish(f'device/{device_id}/way', payload=json.dumps(way), qos=1, retain=False)
    print(f'Send way to device {device_id}')

def on_connect(client, obj, flags, rc):

    print("rc: " + str(rc))


def on_message(client, obj, msg):
    topic = msg.topic
    topic_split = topic.split('/')
    device_id = topic_split[1]
    action = topic_split[2]

    # trogn vi du duogn lay co dinh tu file , thuc te lay tu DB tuy theo thiet bi
    global way
    if action == 'get-way':
        print(f'Device {device_id} get way')
        # can xu ly callback ton time lien quan den client o thread khac
        Thread(target=send_way, args=(client, way, device_id)).start()




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

f = open('way.json', )

# returns JSON object as
# a dictionary
way = json.load(f)

client_id = f'server-{random.randint(0, 1000)}'

#  # trong topic dai dien cho chuoi bat ky (co / ),lister topic cac thiet bi  device/{device_id}/{action}
topic_location = f'device/#'

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
