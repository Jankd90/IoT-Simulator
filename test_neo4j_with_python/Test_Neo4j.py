from neo4j import GraphDatabase

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

# Example usage
if __name__ == "__main__":
    uri = "neo4j+s://e91e2d79.databases.neo4j.io"
    user = "neo4j"
    password = "v2agybb9KPIBM9LmwHcvehVkzub0z1cNZ51IOpNmx9s"

    db = TemperatureDatabase(uri, user, password)
    
    # Add rooms
    db.add_room('Kitchen')
    db.add_room('Living Room')
    
    # Add sensors
    db.add_sensor('Sensor1', 'Temperature')
    db.add_sensor('Sensor2', 'Temperature')
    
    # Create relationships between rooms and sensors
    db.add_room_sensor_relationship('Kitchen', 'Sensor1')
    db.add_room_sensor_relationship('Living Room', 'Sensor2')
    
    # Add temperature readings
    db.add_temperature_reading('Sensor1', 21, '2024-04-09T10:00:00Z')
    db.add_temperature_reading('Sensor2', 23, '2024-04-09T10:00:00Z')
    
    db.close()
