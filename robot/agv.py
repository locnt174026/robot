import json
import random
import time
from threading import Thread
import paho.mqtt.client as mqtt


def send_location(client, way):
    for distance in way:
        for node in distance['nodes']:
            location = json.dumps(node)
            print(location)
            client.publish(f'device/{device_id}/location', payload=location, qos=1, retain=False)
            time.sleep(0.5)


def on_connect(client, obj, flags, rc):
    # thông báo kết nối , đánh dấu là đang online
    client.publish(f'device/{device_id}/status', payload=1, qos=1, retain=True)
    print("rc: " + str(rc))


def on_message(client, obj, msg):
    # nhan duong di chuyen va gui lai vi tri
    if msg.topic == f'device/{device_id}/way':
        global way
        way = json.loads(msg.payload)
        # can xu ly callback ton time lien quan den client o thread khac
        Thread(target=send_location, args=(client, way)).start()


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
has_way = False
way = list()

device_id = 10
client_id = f'device-{device_id}-{random.randint(0, 1000)}'

# sub tat ca cac topic dang device/10/xxx
topic_sub = f'device/{device_id}/#'

broker = '127.0.0.1'
port = 1883
username = 'python-user'
password = '123'
# client_id khong được trùng
client = mqtt.Client(client_id)
client.username_pw_set(username, password)
# set lastwill để tự gửi thông báo  khi mất kết nối , đánh dấu là đang offline
client.will_set(f'device/{device_id}/status', payload=0, qos=1, retain=True)

# set callback function
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# client.on_log = on_log
client.connect(broker, port, 600)

client.subscribe(topic_sub, 1)
# get way
client.publish(f'device/{device_id}/get-way', payload=1, qos=1, retain=False)

client.loop_forever()
