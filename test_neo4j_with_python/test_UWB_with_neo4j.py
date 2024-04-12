from neo4j import GraphDatabase
import random
from datetime import datetime, timedelta

class SensorDatabase:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_room(self, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room, room_name)

    def add_sensor(self, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, initial_observation='0m'):
        with self._driver.session() as session:
            session.write_transaction(self._create_sensor, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, initial_observation)

    def update_sensor_observation(self, device_name, new_observation):
        with self._driver.session() as session:
            session.write_transaction(self._update_sensor_observation, device_name, new_observation)

    def add_room_sensor_relationship(self, room_name, device_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room_sensor_relationship, room_name, device_name)

    def add_uwb_reading(self, device_name, value, timestamp):
        with self._driver.session() as session:
            session.write_transaction(self._create_uwb_reading, device_name, value, timestamp)

    def generate_simulated_data(self, device_name, num_readings):
        current_time = datetime.utcnow()
        for _ in range(num_readings):
            value = random.uniform(0, 10)  # Simulated UWB distance reading between 0 and 10 meters
            timestamp = current_time.isoformat() + 'Z'
            self.add_uwb_reading(device_name, value, timestamp)
            current_time -= timedelta(minutes=30)  # Decrease time by 30 minutes for the next reading

    @staticmethod
    def _create_room(tx, room_name):
        query = "CREATE (:Room {name: $room_name})"
        tx.run(query, room_name=room_name)

    @staticmethod
    def _create_sensor(tx, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, initial_observation):
        query = """
        CREATE (:Sensor {
            device_name: $device_name, 
            device_type: $device_type, 
            mac: $mac, 
            status: $status, 
            connected: $connected, 
            communication_frequency: $communication_frequency, 
            uwb_frequency: $uwb_frequency, 
            feature_of_interest: $feature_of_interest,
            observation: $initial_observation
        })
        """
        tx.run(query, device_name=device_name, device_type=device_type, mac=mac, status=status, connected=connected, communication_frequency=communication_frequency, uwb_frequency=uwb_frequency, feature_of_interest=feature_of_interest, initial_observation=initial_observation)
    
    @staticmethod
    def _update_sensor_observation(tx, device_name, new_observation):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        SET s.observation = $new_observation
        RETURN s
        """
        tx.run(query, device_name=device_name, new_observation=new_observation)

    @staticmethod
    def _create_room_sensor_relationship(tx, room_name, device_name):
        query = (
            "MATCH (r:Room {name: $room_name}) "
            "MATCH (s:Sensor {device_name: $device_name}) "
            "MERGE (r)-[:CONTAINS]->(s)"
        )
        tx.run(query, room_name=room_name, device_name=device_name)

    @staticmethod
    def _create_uwb_reading(tx, device_name, value, timestamp):
        query = (
            "MATCH (s:Sensor {device_name: $device_name}) "
            "CREATE (s)-[:MEASURES]->(:UWBReading {value: $value, timestamp: $timestamp})"
        )
        tx.run(query, device_name=device_name, value=value, timestamp=timestamp)

def main():
    uri = ""  # Change to your Neo4j URI
    user = ""  # Change to your Neo4j username
    password = ""  # Change to your Neo4j password

    db = SensorDatabase(uri, user, password)
    
    while True:
        print("\nOptions:")
        print("1. Create a room")
        print("2. Create a sensor")
        print("3. Associate a room with a sensor")
        print("4. Generate simulated data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            room_name = input("Enter the name of the room: ")
            db.add_room(room_name)
            print("Room created successfully.")
        elif choice == "2":
            device_name = input("Enter the device name: ")
            device_type = input("Enter the device type: ")
            mac = input("Enter the MAC address: ")
            status = input("Enter the status: ")
            connected = input("Enter the connected status (True/False): ")
            communication_frequency = float(input("Enter the communication frequency: "))
            uwb_frequency = float(input("Enter the UWB frequency: "))
            feature_of_interest = input("Enter the feature of interest: ")
            db.add_sensor(device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest)
            print("Sensor created successfully.")
        elif choice == "3":
            room_name = input("Enter the name of the room: ")
            device_name = input("Enter the device name: ")
            db.add_room_sensor_relationship(room_name, device_name)
            print("Relationship created successfully.")
        elif choice == "4":
            device_name = input("Enter the device name for which data needs to be generated: ")
            num_readings = int(input("Enter the number of simulated data points to generate: "))
            db.generate_simulated_data(device_name, num_readings)
            print("Simulated data generated successfully.")
        elif choice == "5":
                device_name = input("Enter the device name to update observation: ")
                new_observation = input("Enter the new observation value: ")
                db.update_sensor_observation(device_name, new_observation)
                print("Observation updated successfully.")
        elif choice == "6":
            db.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
