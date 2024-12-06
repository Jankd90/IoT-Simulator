import paho.mqtt.client as mqtt
import time

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

# Input list of input lists (each sublist contains (object, duration) tuples)
input_lists = [
    [("Room_46", "Chair", 5), ("Bed", 10), ("Sink", 7)],
    [("Couch", 3), ("Toilet", 8)],
    [("Shower", 12), ("Kitchen", 6)],
]  # Example input, each sublist will be processed sequentially

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
    for room, obj, duration in input_list:
        done_received = False
        while not done_received:
            position = room_manager.get_position(room, obj)
            if position:
                # Publish the position and duration to respective topics
                client.publish(position_topic, f"{room}/{obj}: {position}")
                client.publish(activity_time_topic, str(duration))
                print(f"Sent position {position} and duration {duration} for {obj} in {room}")

                # Wait for "Done=True" signal before proceeding
                while not client.user_data['done']:
                    time.sleep(0.1)  # Wait until the "Done" signal is received
                client.user_data['done'] = False  # Reset done state for the next loop
                done_received = True
            else:
                print(f"Waiting for position update for {obj} in {room}...")
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


def process_all_input_lists(input_lists):
    list_count = 0

    for input_list in input_lists:
        print(f"Processing new input list: {input_list}")
        process_input_list(input_list)
        list_count += 1

        if list_count % 10 == 0:
            print("Processed 10 lists, publishing configuration to change object positions.")
            new_positions = {
                "Chair": (10, 10, 0, 0),
                "Bed": (20, 10, 0, 0),
                "Sink": (30, 10, 0, 0),
                "Kitchen": (40, 10, 0, 0),
                "Couch": (15, 15, 0, 0),
                "Toilet": (25, 15, 0, 0),
                "Shower": (35, 15, 0, 0),
            }
            publish_position_configuration("Room_46", new_positions)


# Main program
try:
    print("Starting MQTT client...")
    client.on_message = on_message
    client.connect(BROKER, PORT, KEEP_ALIVE_INTERVAL)

    # Subscribe to all needed topics
    subscribe_to_topics()

    client.loop_start()  # Start MQTT loop globally

    while True:
        process_all_input_lists(input_lists)
        time.sleep(5)  # Prevent excessive loop cycling

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Shutting down gracefully.")

finally:
    client.loop_stop()  # Stop the MQTT loop globally
    client.disconnect()
    print("MQTT client disconnected. Program terminated.")
