from Neo4j_database import Database
from Connect_to_MQTT import MQTTClient


def main():
    uri = ""  # Change to your Neo4j URI
    user = ""  # Change to your Neo4j username
    password = ""  # Change to your Neo4j password

    db = Database(uri, user, password)

    # # MQTT IP to connect to
    # mqtt_client = MQTTClient("")
    # mqtt_client.connect()

    while True:
        print("\nOptions:")
        print("1.  Add a person")
        print("2.  Add a room")
        print("3.  Add a sensor")
        print("4.  Make a relationship")
        print("5.  Update sensor properties")
        print("6.  Delete person")
        print("7.  Delete room")
        print("8.  Delete sensor")
        print("9.  Get names of (person, room, or device)")
        print("10. Get properties of a person, room, or device")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            person_name = input("Enter the name of the person: ")
            db.add_person(person_name)
            print("Person created successfully.")

        if choice == "2":
            room_name = input("Enter the name of the room: ")
            db.add_room(room_name)
            print("Room created successfully.")
        
        elif choice == "3":
            device_name = input("Enter the device name: ")
            device_type = 'ESP32_UWB_ANCHOR' # input("Enter the device type: ")
            mac = 'ff:ff:ff:ff' # input("Enter the MAC address: ")
            status = 'active' # input("Enter the status: ")
            connected = True # input("Is the device connected (True/False)?: ")
            communication_frequency = 50 # input("Enter the communication frequency: ")
            uwb_frequency = 115200 # input("Enter the UWB frequency: ")
            feature_of_interest = 'TAG_1' # input("Enter the feature of interest: ")
            observation = input("Enter the observation: ")
            db.add_sensor(device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, observation)
            print("Sensor added successfully.")
        
        elif choice == "4":
            print("\nMake Relationship Options:")
            print("1. Room -- :CONTAINS_DEVICE --> Device")
            print("2. Device -- :PLACED_IN --> Room")
            print("3. Room -- :ROOM_IN --> Room")
            print("4. Device (tag) -- :CONNECTED_TO --> Device")
            print("5. Device -- :ASSOCIATED_WITH --> Device (tag)")
            print("6. Person -- :LOCATED_IN --> Room")
            print("7. Room -- :CONTAINS_PERSON --> Person")
            print("8. Person -- :USES_DEVICE --> Device (tag)")
            print("9. Device (tag) -- :USED_BY --> Person")
            print("10. Back to main menu")

            relationship_choice = input("Enter your relationship choice: ")

            if relationship_choice == "1":
                room_name = input("Enter the name of the room: ")
                device_name = input("Enter the device name: ")
                db.add_room_sensor_relationship(room_name, device_name)
                print("Relationship created successfully.")

            elif relationship_choice == "2":
                device_name = input("Enter the device name: ")
                room_name = input("Enter the name of the room: ")
                db.add_sensor_room_relationship(device_name, room_name)
                print("Relationship created successfully.")

            elif relationship_choice == "3":
                room_name = input("Enter the name of the room: ")
                room_name_2 = input("Enter the name of the other room: ")
                db.add_room_room_relationship(room_name, room_name_2)
                print("Relationship created successfully.")

            elif relationship_choice == "4":
                device_name_tag = input("Enter the name of the device (tag): ")
                device_name = input("Enter the name of the device: ")
                db.add_sensorTag_sensor_relationship(device_name_tag, device_name)
                print("Relationship created successfully.")

            elif relationship_choice == "5":
                device_name = input("Enter the name of the device: ")
                device_name_tag = input("Enter the name of the device (tag): ")
                db.add_sensor_sensorTag_relationship(device_name, device_name_tag)
                print("Relationship created successfully.")

            elif relationship_choice == "6":
                person_name = input("Enter the name of the person: ")
                room_name = input("Enter the name of the room: ")
                db.add_person_room_relationship(person_name, room_name)
                print("Relationship created successfully.")

            elif relationship_choice == "7":
                room_name = input("Enter the name of the room: ")
                person_name = input("Enter the name of the person: ")
                db.add_room_person_relationship(room_name, person_name)
                print("Relationship created successfully.")

            elif relationship_choice == "8":
                person_name = input("Enter the name of the person: ")
                device_name_tag = input("Enter the name of the device (tag): ")
                db.add_person_device_relationship(person_name, device_name_tag)
                print("Relationship created successfully.")

            elif relationship_choice == "9":
                device_name_tag = input("Enter the name of the device (tag): ")
                person_name = input("Enter the name of the person: ")
                db.add_device_person_relationship(device_name_tag, person_name)
                print("Relationship created successfully.")

            elif relationship_choice == "10":
                continue

            else:
                print("Invalid relationship choice. Please try again.")

        elif choice == "5":
            print("\nUpdate Options:")
            print("1. Update communication frequency")
            print("2. Update UWB frequency")
            print("3. Update feature of interest")
            print("4. Update observation")
            print("5. Back to main menu")

            update_choice = input("Enter your update choice: ")

            if update_choice == "1":
                device_name = input("Enter the device name whose communication frequency you want to update: ")
                new_frequency = input("Enter the new communication frequency: ")
                db.update_communication_frequency(device_name, new_frequency)
                print("Communication frequency updated successfully.")
            
            elif update_choice == "2":
                device_name = input("Enter the device name whose UWB frequency you want to update: ")
                new_frequency = input("Enter the new UWB frequency: ")
                db.update_uwb_frequency(device_name, new_frequency)
                print("UWB frequency updated successfully.")
            
            elif update_choice == "3":
                device_name = input("Enter the device name whose feature of interest you want to update: ")
                new_feature = input("Enter the new feature of interest: ")
                db.update_feature_of_interest(device_name, new_feature)
                print("Feature of interest updated successfully.")
            
            elif update_choice == "4":
                device_name = input("Enter the device name whose observation you want to update: ")
                new_observation = input("Enter the new observation: ")
                db.update_observation(device_name, new_observation)
                print("Observation updated successfully.")
            
            elif update_choice == "5":
                continue
            
            else:
                print("Invalid update choice. Please try again.")
        
        elif choice == "6":
            person_name = input("Enter the name of person to delete: ")
            db.delete_person(person_name)
            print("Person deleted successfully.")

        elif choice == "7":
            room_name = input("Enter the name of room to delete: ")
            db.delete_room(room_name)
            print("Room deleted successfully.")

        elif choice == "8":
            device_name = input("Enter the device name to delete: ")
            db.delete_sensor(device_name)
            print("Device deleted successfully.")

        elif choice == "9":
            print("\nGet Name Options:")
            print("1. Get name of Persons")
            print("2. Get name of Rooms")
            print("3. Get name of Devices")
            print("4. Back to main menu")

            get_name_choice = input("Enter your get names choice: ")

            if get_name_choice == "1":
                db.get_person_names()
                print("\nPersons name given successfully.")
            
            elif get_name_choice == "2":
                db.get_room_names()
                print("\nRooms name given successfully.")
            
            elif get_name_choice == "3":
                db.get_sensor_names()
                print("\nDevices name given successfully.")

            elif get_name_choice == "4":
                continue
            
            else:
                print("Invalid get names choice. Please try again.")

        elif choice == "10":
            print("\nGet properties Options:")
            print("1. Get properties of a Person")
            print("2. Get properties of a Room")
            print("3. Get properties of a Device")
            print("4. Back to main menu")

            get_properties_choice = input("Enter your get properties choice: ")

            if get_properties_choice == "1":
                device_name = input("Enter the name of the device: ")
                sensor_properties = db.get_sensor_properties(device_name)
                if sensor_properties:
                    print("Sensor Properties:")
                    for key, value in sensor_properties.items():
                        print(f"{key}: {value}")
                else:
                    print("Sensor not found.")

            elif get_properties_choice == "2":
                person_name = input("Enter the name of the person: ")
                person_properties = db.get_person_properties(person_name)
                if person_properties:
                    print("Person Properties:")
                    for key, value in person_properties.items():
                        print(f"{key}: {value}")
                else:
                    print("Person not found.")

            elif get_properties_choice == "3":
                room_name = input("Enter the name of the room: ")
                room_properties = db.get_room_properties(room_name)
                if room_properties:
                    print("Room Properties:")
                    for key, value in room_properties.items():
                        print(f"{key}: {value}")
                else:
                    print("Room not found.")

            elif get_properties_choice == "4":
                continue
            
            else:
                print("Invalid get properties choice. Please try again.")

        elif choice == "11":
            db.close()
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
