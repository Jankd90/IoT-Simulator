from neo4j import GraphDatabase
import random
from datetime import datetime, timedelta

class TemperatureDatabase:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_room(self, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room, room_name)

    def add_sensor(self, sensor_id, sensor_type):
        with self._driver.session() as session:
            session.write_transaction(self._create_sensor, sensor_id, sensor_type)

    def add_room_sensor_relationship(self, room_name, sensor_id):
        with self._driver.session() as session:
            session.write_transaction(self._create_room_sensor_relationship, room_name, sensor_id)

    def add_temperature_reading(self, sensor_id, value, timestamp):
        with self._driver.session() as session:
            session.write_transaction(self._create_temperature_reading, sensor_id, value, timestamp)

    def generate_simulated_data(self, sensor_id, num_readings):
        current_time = datetime.utcnow()
        for _ in range(num_readings):
            value = random.uniform(15, 30)  # Simulated temperature reading between 15 and 30 degrees Celsius
            timestamp = current_time.isoformat() + 'Z'
            self.add_temperature_reading(sensor_id, value, timestamp)
            current_time -= timedelta(minutes=30)  # Decrease time by 30 minutes for the next reading

    @staticmethod
    def _create_room(tx, room_name):
        query = "CREATE (:Room {name: $room_name})"
        tx.run(query, room_name=room_name)

    @staticmethod
    def _create_sensor(tx, sensor_id, sensor_type):
        query = "CREATE (:Sensor {id: $sensor_id, type: $sensor_type})"
        tx.run(query, sensor_id=sensor_id, sensor_type=sensor_type)

    @staticmethod
    def _create_room_sensor_relationship(tx, room_name, sensor_id):
        query = (
            "MATCH (r:Room {name: $room_name}) "
            "MATCH (s:Sensor {id: $sensor_id}) "
            "MERGE (r)-[:CONTAINS]->(s)"
        )
        tx.run(query, room_name=room_name, sensor_id=sensor_id)

    @staticmethod
    def _create_temperature_reading(tx, sensor_id, value, timestamp):
        query = (
            "MATCH (s:Sensor {id: $sensor_id}) "
            "CREATE (s)-[:MEASURES]->(:TemperatureReading {value: $value, timestamp: $timestamp})"
        )
        tx.run(query, sensor_id=sensor_id, value=value, timestamp=timestamp)

def main():
    uri = ""  # Change to your Neo4j URI
    user = ""  # Change to your Neo4j username
    password = ""  # Change to your Neo4j password

    db = TemperatureDatabase(uri, user, password)
    
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
            sensor_id = input("Enter the sensor ID: ")
            sensor_type = input("Enter the sensor type: ")
            db.add_sensor(sensor_id, sensor_type)
            print("Sensor created successfully.")
        elif choice == "3":
            room_name = input("Enter the name of the room: ")
            sensor_id = input("Enter the sensor ID: ")
            db.add_room_sensor_relationship(room_name, sensor_id)
            print("Relationship created successfully.")
        elif choice == "4":
            sensor_id = input("Enter the sensor ID for which data needs to be generated: ")
            num_readings = int(input("Enter the number of simulated data points to generate: "))
            db.generate_simulated_data(sensor_id, num_readings)
            print("Simulated data generated successfully.")
        elif choice == "5":
            db.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
