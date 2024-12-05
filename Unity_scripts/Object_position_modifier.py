import paho.mqtt.client as mqtt
import time

# MQTT broker settings
broker_address = ''  # Replace with your MQTT broker address
port = 1883  # Typically 1883 for unencrypted MQTT communication

# The topic to which the Unity object is subscribed
objectID = "Couch"  # Replace with the object ID from Unity
roomID = "Hallway"  # Replace with the room ID from Unity
publish_topic = f"config/{roomID}/{objectID}/transform"  # Topic format used in Unity

# Create a new MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, port)

# Function to publish new position to the topic
def publish_new_position(x, y, z, rotZ):
    # Format the position as "x,y,z"
    message = f"{x},{y},{z},{rotZ}"
    
    # Publish the message to the topic
    client.publish(publish_topic, message)
    print(f"Published new position to {publish_topic}: {message}")

# Example of publishing new positions
def main():
    try:
        while True:
            # Example: update new position (you can modify this with real data)
            x, y, z, rotZ = 2.07, -7.056, -1, 0  # Example new position
            
            # Publish the new position
            publish_new_position(x, y, z, rotZ)

            # Wait for 5 seconds before sending the next position
            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping script")
    
    finally:
        # Disconnect MQTT client
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    main()



# import time
# import json
# import paho.mqtt.client as mqtt
# import numpy as np

# broker_address = ''
# broker_port = 1883

# def on_connect(client, userdata, flags, rc):
#     print(f'Connected with result code {str(rc)}')
#     client.subscribe("activity/Finished")

# def on_message(client, userdata, msg):
#     global activity_finished
#     try:
#         payload = msg.payload.decode()
#         if payload == 'True':
#             activity_finished = True
#         elif payload == 'False':
#             activity_finished = False
#         print(f'Received activityFinished: {activity_finished}')
#     except Exception as e:
#         print('Error decoding JSON: {e}')

# # Initialize MQTT client
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# # connect to MQTT broker
# client.connect(broker_address, broker_port, 60)

# client.loop_start()

# try:
#     while True:
#         # Get the current position and activity time
#         current_data = data[i]
#         current_position = {"x": current_data[0], "y": current_data[1], "z": current_data[2]}
#         current_activity_time = current_data[3]

#         if activity_finished:

#             # Publish position to target topic
#             position_topic = "activity/position"
#             client.publish(position_topic, json.dumps(current_position))
#             # Publish activity time to unit topic
#             activity_time_topic = "activity/time"
#             client.publish(activity_time_topic, str(current_activity_time))

#             i = (i + 1) % len(data)
#             # print(i)

#         time.sleep(1)

# except KeyboardInterrupt:
#     print('Interrupted, exiting...')
# finally:
#     # Disconnect MQTT client
#     client.disconnect()
#     client.loop_stop()