from Room_Manager import RoomManager
from Simulation_controller import setup_mqtt, process_input_list
from Utils import subscribe_to_topics, get_list, publish_position_configuration, count_files
from LLM import get_scenario_state
import os

FOLDER_PATH = "Scenarios"

BROKER = "your_mqtt_broker_address"
PORT = 1883
KEEP_ALIVE_INTERVAL = 60

def display_menu():
    print("\n--- User Interface ---")
    print("1. Process Scenario")
    print("2. Configure Positions")
    print("3. Get Scenario States with LLM")
    print("4. Exit")
    return input("Enter your choice: ")

def process_scenario_ui(client, room_manager):
    file_count = count_files(FOLDER_PATH)
    if file_count == 0:
        print("No scenario files found in the folder.")
        return
    print(f"\nAvailable Scenarios (1-{file_count}):")
    for i in range(1, file_count + 1):
        print(f"Scenario_{i}.txt")
    scenario_number = input(f"Enter scenario number to process (1-{file_count}): ")
    try:
        scenario_path = os.path.join(FOLDER_PATH, f"Scenario_{scenario_number}.txt")
        scenario = get_list(scenario_path)
        process_input_list(scenario, client, room_manager)
        print("Scenario processed successfully.")
    except FileNotFoundError:
        print("Scenario file not found.")
    except Exception as e:
        print(f"Error processing scenario: {e}")

def configure_positions_ui(client, room_manager):
    rooms = room_manager.get_rooms()
    if not rooms:
        print("No rooms available.")
        return
    print("\nAvailable Rooms:")
    for room in rooms:
        print(f"- {room}")
    room_id = input("Enter the room ID to configure positions: ")
    if room_id not in rooms:
        print("Invalid room ID.")
        return
    print(f"Configuring positions for room: {room_id}")
    objects = room_manager.get_objects_in_room(room_id)
    new_positions = {}
    for obj in objects:
        print(f"Enter new position for '{obj}' (format: x,y,width,height) or press Enter to skip:")
        pos_input = input("> ")
        if pos_input:
            try:
                x, y, width, height = map(int, pos_input.split(","))
                new_positions[obj] = (x, y, width, height)
            except ValueError:
                print("Invalid format. Skipping this object.")
    publish_position_configuration(room_id, new_positions, client, room_manager)
    print("Position configuration published.")

def main():
    room_manager = RoomManager()
    client = setup_mqtt(room_manager)
    client.connect(BROKER, PORT, KEEP_ALIVE_INTERVAL)
    client.loop_start()
    subscribe_to_topics(client, room_manager)
    while True:
        choice = display_menu()
        if choice == "1":
            process_scenario_ui(client, room_manager)
        elif choice == "2":
            configure_positions_ui(client, room_manager)
        elif choice == "3":
            print("Exiting the interface. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
