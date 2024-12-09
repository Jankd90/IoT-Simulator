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
        if obj not in self.get_objects_in_room(room_id):
            print(f"Error: Object '{obj}' does not belong to room '{room_id}'.")
            return
        self.positions[room_id][obj] = (x, y)
        print(f"Updated position for {obj} in {room_id}: {self.positions[room_id][obj]}")

    def get_position(self, room_id, obj):
        return self.positions.get(room_id, {}).get(obj, None)

    def get_objects_in_room(self, room_id):
        return self.rooms.get(room_id, [])

    def get_rooms(self):
        return list(self.rooms.keys())
