import paho.mqtt.client as mqtt
import time
from Room_Manager import RoomManager
from Utils import subscribe_to_topics, publish_position_configuration
import threading

position_topic = "activity/position"
activity_time_topic = "activity/time"

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    if len(topic_parts) == 3 and topic_parts[2] == "position":
        room_id, obj = topic_parts[0], topic_parts[1]
        try:
            x, y = map(int, msg.payload.decode().split(","))
            userdata['room_manager'].update_position(room_id, obj, x, y)
        except ValueError:
            print(f"Invalid position format for {obj} in {room_id}. Expected 'x,y'.")
    elif msg.topic == "activity/Finished" and msg.payload.decode() == "True":
        userdata['done'] = True

def setup_mqtt(room_manager):
    client = mqtt.Client(userdata={'done': False, 'room_manager': room_manager})
    client.on_message = on_message
    return client

# def process_input_list(input_list, client, room_manager):
#     for room_id, obj, duration in input_list:
#         done_received = False
#         while not done_received:
#             position = room_manager.get_position(room_id, obj)
#             if position:
#                 client.publish(position_topic, f"{room_id}/{obj}: {position}")
#                 client.publish(activity_time_topic, str(duration))
#                 print(f"Sent position {position} and duration {duration} for {obj} in {room_id}")
#                 while not client.user_data['done']:
#                     time.sleep(0.1)
#                 client.user_data['done'] = False
#                 done_received = True
#             else:
#                 # print(f"Waiting for position update for {obj} in {room_id}...")
#                 time.sleep(1)

def process_input_list(input_list, client, room_manager):
    """
    Processes the input list by sending positions and durations
    without using time.sleep, leveraging threading events instead.
    """
    done_event = threading.Event()

    def on_done_received():
        """Callback when 'done' is received."""
        done_event.set()

    # Attach the callback for done handling
    def wrapped_on_message(client, userdata, msg):
        original_on_message(client, userdata, msg)  # Call the original on_message
        if userdata['done']:
            on_done_received()

    # Save and override the original on_message
    original_on_message = client.on_message
    client.on_message = wrapped_on_message

    try:
        for room_id, obj, duration in input_list:
            position = room_manager.get_position(room_id, obj)
            if not position:
                print(f"Position not found for {obj} in {room_id}, skipping.")
                continue

            client.publish(position_topic, f"{room_id}/{obj}: {position}")
            client.publish(activity_time_topic, str(duration))
            print(f"Sent position {position} and duration {duration} for {obj} in {room_id}")

            # Wait for the done event to be set
            done_event.clear()
            if not done_event.wait(timeout=200):  # Wait for a maximum of 10 seconds
                print(f"Timeout waiting for 'done' signal for {obj} in {room_id}.")
                continue

            # Reset the flag for the next loop
            client.user_data['done'] = False

    finally:
        # Restore the original on_message
        client.on_message = original_on_message
