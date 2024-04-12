from neo4j import GraphDatabase
from datetime import datetime

class Database:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_person(self, person_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_person, person_name)
    
    @staticmethod
    def _create_person(tx, person_name):
        query = "CREATE (:Person {name: $person_name})"
        tx.run(query, person_name=person_name)

    def add_room(self, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room, room_name)
    
    @staticmethod
    def _create_room(tx, room_name):
        query = "CREATE (:Room {name: $room_name})"
        tx.run(query, room_name=room_name)

    def add_sensor(self, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, observation):
        with self._driver.session() as session:
            timestamp = self.update_time()  # Get current timestamp
            session.write_transaction(self._create_sensor, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, observation, timestamp)

    @staticmethod
    def _create_sensor(tx, device_name, device_type, mac, status, connected, communication_frequency, uwb_frequency, feature_of_interest, observation, timestamp):
        query = """
        CREATE (:Sensor {
            device_name: $device_name,
            device_type: $device_type,
            MAC: $mac,
            status: $status,
            connected: $connected,
            communication_frequency: $communication_frequency,
            uwb_frequency: $uwb_frequency,
            feature_of_interest: $feature_of_interest,
            observation: $observation,
            timestamp: $timestamp
        })
        """
        tx.run(query, device_name=device_name, device_type=device_type, mac=mac, status=status, connected=connected, communication_frequency=communication_frequency, uwb_frequency=uwb_frequency, feature_of_interest=feature_of_interest, observation=observation, timestamp=timestamp)

    def add_room_sensor_relationship(self, room_name, device_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room_sensor_relationship, room_name, device_name)

    @staticmethod
    def _create_room_sensor_relationship(tx, room_name, device_name):
        query = (
            "MATCH (r:Room {name: $room_name}) "
            "MATCH (s:Sensor {device_name: $device_name}) "
            "MERGE (r)-[:CONTAINS_DEVICE]->(s)"
        )
        tx.run(query, room_name=room_name, device_name=device_name)
    
    def add_sensor_room_relationship(self, device_name, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_sensor_room_relationship, device_name, room_name)

    @staticmethod
    def _create_sensor_room_relationship(tx, device_name, room_name):
        query = (
            "MATCH (s:Sensor {device_name: $device_name}) "
            "MATCH (r:Room {name: $room_name}) "
            "MERGE (r)-[:PLACED_IN]->(s)"
        )
        tx.run(query, device_name=device_name, room_name=room_name)

    
    def add_room_room_relationship(self, room_name_1, room_name_2):
        with self._driver.session() as session:
            session.write_transaction(self._create_room_room_relationship, room_name_1, room_name_2)

    @staticmethod
    def _create_room_room_relationship(tx, room_name_1, room_name_2):
        query = (
            "MATCH (r1:Room {name: $room_name_1}) "
            "MATCH (r2:Room {name: $room_name_2}) "
            "MERGE (r1)-[:ROOM_IN]->(r2)"
        )
        tx.run(query, room_name_1=room_name_1, room_name_2=room_name_2)

    def add_sensorTag_sensor_relationship(self, device_name_tag, device_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_sensorTag_sensor_relationship, device_name_tag, device_name)

    @staticmethod
    def _create_sensorTag_sensor_relationship(tx, device_name_tag, device_name):
        query = (
            "MATCH (s1:Sensor {device_name: $device_name_tag}) "
            "MATCH (s2:Sensor {device_name: $device_name}) "
            "MERGE (s1)-[:CONNECTED_TO]->(s2)"
        )
        tx.run(query, device_name_tag=device_name_tag, device_name=device_name)

    def add_sensor_sensorTag_relationship(self, device_name, device_name_tag):
        with self._driver.session() as session:
            session.write_transaction(self._create_sensor_sensorTag_relationship, device_name, device_name_tag)

    @staticmethod
    def _create_sensor_sensorTag_relationship(tx, device_name, device_name_tag):
        query = (
            "MATCH (s1:Sensor {device_name: $device_name}) "
            "MATCH (s2:Sensor {device_name: $device_name_tag}) "
            "MERGE (s1)-[:ASSOCIATED_WITH]->(s2)"
        )
        tx.run(query, device_name=device_name, device_name_tag=device_name_tag)

    def add_person_room_relationship(self, person_name, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_person_room_relationship, person_name, room_name)

    @staticmethod
    def _create_person_room_relationship(tx, person_name, room_name):
        query = (
            "MATCH (p:Person {name: $person_name}) "
            "MATCH (r:Room {name: $room_name}) "
            "MERGE (p)-[:LOCATED_IN]->(r)"
        )
        tx.run(query, person_name=person_name, room_name=room_name)

    def add_room_person_relationship(self, room_name, person_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_room_person_relationship, room_name, person_name)

    @staticmethod
    def _create_room_person_relationship(tx, room_name, person_name):
        query = (
            "MATCH (r:Room {name: $room_name}) "
            "MATCH (p:Person {name: $person_name}) "
            "MERGE (p)-[:CONTAINS_PERSON]->(r)"
        )
        tx.run(query, room_name=room_name, person_name=person_name)

    def add_person_device_relationship(self, person_name, device_name_tag):
        with self._driver.session() as session:
            session.write_transaction(self._create_person_device_relationship, person_name, device_name_tag)

    @staticmethod
    def _create_person_device_relationship(tx, person_name, device_name_tag):
        query = (
            "MATCH (p:Person {name: $person_name}) "
            "MATCH (s:Sensor {device_name: $device_name_tag}) "
            "MERGE (p)-[:USES_DEVICE]->(s)"
        )
        tx.run(query, person_name=person_name, device_name_tag=device_name_tag)

    def add_device_person_relationship(self, device_name_tag, person_name):
        with self._driver.session() as session:
            session.write_transaction(self._create_device_person_relationship, device_name_tag, person_name)

    @staticmethod
    def _create_device_person_relationship(tx, device_name_tag, person_name):
        query = (
            "MATCH (s:Sensor {device_name: $device_name_tag}) "
            "MATCH (p:Person {name: $person_name}) "
            "MERGE (p)-[:USED_BY]->(s)"
        )
        tx.run(query, device_name_tag=device_name_tag, person_name=person_name)

    def update_communication_frequency(self, device_name, new_frequency):
        with self._driver.session() as session:
            timestamp = self.update_time()  # Get current timestamp
            session.write_transaction(self._update_communication_frequency, device_name, new_frequency, timestamp)

    @staticmethod
    def _update_communication_frequency(tx, device_name, new_frequency, timestamp):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        SET s.communication_frequency = $new_frequency,
            s.timestamp = $timestamp
        """
        tx.run(query, device_name=device_name, new_frequency=new_frequency, timestamp=timestamp)

    def update_uwb_frequency(self, device_name, new_frequency):
        with self._driver.session() as session:
            timestamp = self.update_time()  # Get current timestamp
            session.write_transaction(self._update_uwb_frequency, device_name, new_frequency, timestamp)

    @staticmethod
    def _update_uwb_frequency(tx, device_name, new_frequency, timestamp):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        SET s.uwb_frequency = $new_frequency,
            s.timestamp = $timestamp
        """
        tx.run(query, device_name=device_name, new_frequency=new_frequency, timestamp=timestamp)

    def update_feature_of_interest(self, device_name, new_feature):
        with self._driver.session() as session:
            timestamp = self.update_time()  # Get current timestamp
            session.write_transaction(self._update_feature_of_interest, device_name, new_feature, timestamp)

    @staticmethod
    def _update_feature_of_interest(tx, device_name, new_feature, timestamp):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        SET s.feature_of_interest = $new_feature,
            s.timestamp = $timestamp
        """
        tx.run(query, device_name=device_name, new_feature=new_feature, timestamp=timestamp)

    def update_observation(self, device_name, new_observation):
        with self._driver.session() as session:
            timestamp = self.update_time()  # Get current timestamp
            session.write_transaction(self._update_observation, device_name, new_observation, timestamp)

    @staticmethod
    def _update_observation(tx, device_name, new_observation, timestamp):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        SET s.observation = $new_observation,
            s.timestamp = $timestamp
        """
        tx.run(query, device_name=device_name, new_observation=new_observation, timestamp=timestamp)


    def delete_person(self, person_name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_person, person_name)

    @staticmethod
    def _delete_person(tx, person_name):
        query = """
        MATCH (p:Person {person_name: $person_name})
        DETACH DELETE p
        """
        tx.run(query, person_name=person_name)

    def delete_room(self, room_name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_room, room_name)

    @staticmethod
    def _delete_room(tx, room_name):
        query = """
        MATCH (r:Room {room_name: $room_name})
        DETACH DELETE r
        """
        tx.run(query, room_name=room_name)

    def delete_sensor(self, device_name):
        with self._driver.session() as session:
            session.write_transaction(self._delete_sensor, device_name)

    @staticmethod
    def _delete_sensor(tx, device_name):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        DETACH DELETE s
        """
        tx.run(query, device_name=device_name)

    def get_person_names(self):
        with self._driver.session() as session:
            return session.read_transaction(self._get_person_names)

    @staticmethod
    def _get_person_names(tx):
        query = """
        MATCH (p:Person)
        RETURN p.person_name AS personName
        """
        result = tx.run(query)
        return [record["personName"] for record in result]
    
    def get_room_names(self):
        with self._driver.session() as session:
            return session.read_transaction(self._get_room_names)

    @staticmethod
    def _get_room_names(tx):
        query = """
        MATCH (r:Room)
        RETURN r.room_name AS roomName
        """
        result = tx.run(query)
        return [record["roomName"] for record in result]

    def get_sensor_names(self):
        with self._driver.session() as session:
            return session.read_transaction(self._get_sensor_names)

    @staticmethod
    def _get_sensor_names(tx):
        query = """
        MATCH (s:Sensor)
        RETURN s.device_name AS deviceName
        """
        result = tx.run(query)
        return [record["deviceName"] for record in result]

    def get_sensor_properties(self, device_name):
        with self._driver.session() as session:
            return session.read_transaction(self._get_sensor_properties, device_name)

    @staticmethod
    def _get_sensor_properties(tx, device_name):
        query = """
        MATCH (s:Sensor {device_name: $device_name})
        RETURN s {.*}
        """
        result = tx.run(query, device_name=device_name).single()
        if result:
            return dict(result['s'])
        else:
            return None

    def get_person_properties(self, person_name):
        with self._driver.session() as session:
            return session.read_transaction(self._get_person_properties, person_name)

    @staticmethod
    def _get_person_properties(tx, person_name):
        query = """
        MATCH (p:Person {name: $person_name})
        RETURN p {.*}
        """
        result = tx.run(query, person_name=person_name).single()
        if result:
            return dict(result['p'])
        else:
            return None

    def get_room_properties(self, room_name):
        with self._driver.session() as session:
            return session.read_transaction(self._get_room_properties, room_name)

    @staticmethod
    def _get_room_properties(tx, room_name):
        query = """
        MATCH (r:Room {name: $room_name})
        RETURN r {.*}
        """
        result = tx.run(query, room_name=room_name).single()
        if result:
            return dict(result['r'])
        else:
            return None

    def update_time(self):
        current_time = datetime.utcnow()
        timestamp = current_time.isoformat() + 'Z'
        return timestamp
