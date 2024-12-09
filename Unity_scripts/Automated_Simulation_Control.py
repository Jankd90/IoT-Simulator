import paho.mqtt.client as mqtt
import time
import ast
import os

class RoomManager:
    def __init__(self):
        # Dictionary of rooms and their objects
        self.rooms = {
            "Room_46": ["Couch", "Chair", "Bed", "Kitchen"],
            "Washroom_46": ["Sink", "Toilet", "Shower"],
            "Room_47": ["Couch", "Chair", "Bed", "Kitchen"],
            "Washroom_47": ["Sink", "Toilet", "Shower"],
            "Hallway": ["Chair_1", "Chair_2"]
        }
        # Dictionary to store dynamic positions for each room's objects
        self.positions = {room_id: {obj: None for obj in objs} for room_id, objs in self.rooms.items()}

    def update_position(self, room_id, obj, x, y):
        # Validate that the object belongs to the specified room
        if obj not in self.get_objects_in_room(room_id):
            print(f"Error: Object '{obj}' does not belong to room '{room_id}'.")
            return

        # Update the position of the object
        self.positions[room_id][obj] = (x, y)
        print(f"Updated position for {obj} in {room_id}: {self.positions[room_id][obj]}")

    def get_position(self, room_id, obj):
        # Get the position of a specific object in a specific room
        return self.positions.get(room_id, {}).get(obj, None)

    def get_objects_in_room(self, room_id):
        # Return the list of objects in the given room
        return self.rooms.get(room_id, [])

    def get_rooms(self):
        # Return the list of room IDs
        return list(self.rooms.keys())


# MQTT Broker settings
BROKER = "your_mqtt_broker_address"
PORT = 1883
KEEP_ALIVE_INTERVAL = 60

# MQTT topics
position_topic = "activity/position"
activity_time_topic = "activity/time"
activity_finished_topic = "activity/Finished"

folder_path = r'Scenarios'

# # scenario list of (room, object, duration) tuples
# input_list = [
#     ("Room_46", "Chair", 5), ("Room_46", "Bed", 10), ("Washroom_46", "Sink", 7), 
#     ("Room_46", "Couch", 3), ("Washroom_46", "Toilet", 8), 
#     ("Washroom_46", "Shower", 12), ("Room_46", "Kitchen", 6)
# ]  # Example input processed sequentially

def read_scenario(file_path):
    with open(file_path, 'r') as file:
        scenario = file.read()
    return scenario

def get_list(file):
    scenario = read_scenario(file)

    # Convert string to a list of tuples
    scenario_list = ast.literal_eval(scenario)
    return scenario_list

def count_files(folder_path):
    # List all files in the folder
    all_files = os.listdir(folder_path)

    # Count the files
    file_count = len(all_files)
    return file_count

# Create an instance of RoomManager
room_manager = RoomManager()

# Set up the MQTT client
client = mqtt.Client(userdata={'done': False})  # 'done' is used to track the "Done=True" signal


def on_message(client, userdata, msg):
    # Parse the topic to extract room ID and object ID
    topic_parts = msg.topic.split("/")
    if len(topic_parts) == 3 and topic_parts[2] == "position":
        room_id, obj = topic_parts[0], topic_parts[1]
        try:
            x, y = map(int, msg.payload.decode().split(","))
            room_manager.update_position(room_id, obj, x, y)
        except ValueError:
            print(f"Invalid position format for {obj} in {room_id}. Expected 'x,y'.")
    elif msg.topic == activity_finished_topic and msg.payload.decode() == "True":
        userdata['done'] = True


def subscribe_to_topics():
    # Subscribe to specific non-dynamic topics
    client.subscribe(activity_finished_topic)
    print(f"Subscribed to topic: {activity_finished_topic}")

    # Subscribe to dynamic topics for all objects in all rooms
    for room_id in room_manager.get_rooms():
        for obj in room_manager.get_objects_in_room(room_id):
            topic = f"{room_id}/{obj}/position"
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")


def process_input_list(input_list):
    for room_id, obj, duration in input_list:
        done_received = False
        while not done_received:
            position = room_manager.get_position(room_id, obj)
            if position:
                # Publish the position and duration to respective topics
                client.publish(position_topic, f"{room_id}/{obj}: {position}")
                client.publish(activity_time_topic, str(duration))
                print(f"Sent position {position} and duration {duration} for {obj} in {room_id}")

                # Wait for "Done=True" signal before proceeding
                while not client.user_data['done']:
                    time.sleep(0.1)  # Wait until the "Done" signal is received
                client.user_data['done'] = False  # Reset done state for the next loop
                done_received = True
            else:
                print(f"Waiting for position update for {obj} in {room_id}...")
                time.sleep(1)  # Retry after a delay


def publish_position_configuration(room_id, new_positions):
    objects = room_manager.get_objects_in_room(room_id)
    if not objects:
        print(f"No objects found in room {room_id}.")
        return

    for obj in objects:
        if obj in new_positions:
            pos = new_positions[obj]
            config_object_topic = f"config/{room_id}/{obj}/transform"
            msg = f"{pos[0]},{pos[1]},{pos[2]},{pos[3]}"
            client.publish(config_object_topic, msg)
            print(f"Published new position for {obj} in {room_id}: {msg}")
        else:
            print(f"Position not provided for {obj} in {room_id}.")


# Main program
try:
    print("Starting MQTT client...")
    client.on_message = on_message
    client.connect(BROKER, PORT, KEEP_ALIVE_INTERVAL)

    # Subscribe to all needed topics
    subscribe_to_topics()

    client.loop_start()  # Start MQTT loop globally

    file_count = count_files(folder_path)

    for i in range(1, file_count + 1):
        scenario_path = fr'{folder_path}\Scenario_{i}.txt'
        scenario = get_list(scenario_path)
        process_input_list(scenario)
        time.sleep(5)  # Prevent excessive loop cycling

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Shutting down gracefully.")

finally:
    client.loop_stop()  # Stop the MQTT loop globally
    client.disconnect()
    print("MQTT client disconnected. Program terminated.")
