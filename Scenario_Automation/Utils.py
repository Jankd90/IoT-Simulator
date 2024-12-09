import os
import ast

def read_scenario(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_list(file_path):
    scenario = read_scenario(file_path)
    return ast.literal_eval(scenario)

def count_files(folder_path):
    return len(os.listdir(folder_path))

def subscribe_to_topics(client, room_manager):
    client.subscribe("activity/Finished")
    print(f"Subscribed to topic: activity/Finished")
    for room_id in room_manager.get_rooms():
        for obj in room_manager.get_objects_in_room(room_id):
            topic = f"{room_id}/{obj}/position"
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")

def publish_position_configuration(room_id, new_positions, client, room_manager):
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
