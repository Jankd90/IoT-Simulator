import time
import json
import paho.mqtt.client as mqtt
import numpy as np

broker_address = ''
broker_port = 1883

# [x, y, z, activity_time]
data = np.array([
    [0.55, -5.57, 0, 5],
    [4.21, -1.6, 0, 10],
    [7.84, -8.12, 0, 2],
    [7.95, -4.33, 0, 4],
    [2.33, -7.7, 0, 1],
    [2.35, -4.32, 0, 6],
    [6.82, -1.72, 0, 3]
])

activity_finished = False
i = 0

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    client.subscribe("activity/Finished")

def on_message(client, userdata, msg):
    global activity_finished
    try:
        payload = msg.payload.decode()
        if payload == 'True':
            activity_finished = True
        elif payload == 'False':
            activity_finished = False
        print(f'Received activityFinished: {activity_finished}')
    except Exception as e:
        print('Error decoding JSON: {e}')

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect to MQTT broker
client.connect(broker_address, broker_port, 60)

client.loop_start()

try:
    while True:
        # Get the current position and activity time
        current_data = data[i]
        current_position = {"x": current_data[0], "y": current_data[1], "z": current_data[2]}
        current_activity_time = current_data[3]

        if activity_finished:

            # Publish position to target topic
            position_topic = "activity/position"
            client.publish(position_topic, json.dumps(current_position))
            # Publish activity time to unit topic
            activity_time_topic = "activity/time"
            client.publish(activity_time_topic, str(current_activity_time))

            i = (i + 1) % len(data)
            # print(i)

        time.sleep(1)

except KeyboardInterrupt:
    print('Interrupted, exiting...')
finally:
    # Disconnect MQTT client
    client.disconnect()
    client.loop_stop()