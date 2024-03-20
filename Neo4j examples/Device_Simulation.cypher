//-------------------------------------------
// Object Person
//-------------------------------------------

// Person 1
CREATE (P_1:Person {main_room:'Room_46'})


//-------------------------------------------
// Object Device
//-------------------------------------------

//------------
// Anchors
//------------

CREATE (Anchor_1:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR001', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_2:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR002', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_3:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR003', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_4:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR004', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_5:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR005', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_6:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR006', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_7:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR007', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_8:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR008', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_9:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR009', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_10:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR010', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_11:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR011', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_12:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR012', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_13:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR013', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_14:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR014', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})
CREATE (Anchor_15:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR015', distance_to_tag: '1m', connectivity_status: 'connected', status: 'active'})

//------------
// Tags
//------------

CREATE (Tag_1:Person {sensor_type:'UWB Tag', name:'TAG001', battery_level:80, data_rate:112500, manufacturer:'Makerfabs', status:'active'})


//-------------------------------------------
// Object Room
//-------------------------------------------

CREATE (Room_45:Room {name: 'Room 45', room_number: '45', floor: '4'})
CREATE (Room_46:Room {name: 'Room 46', room_number: '46', floor: '4'})
CREATE (Washroom_45:Room {name: 'Washing room 45', room_number: '45', floor: '4'})
CREATE (Washroom_46:Room {name: 'Washing room 46', room_number: '46', floor: '4'})                    
CREATE (Hallway:Room {name: 'Hallway', floor: '4'})




//-------------------------------------------
// Relationships
//-------------------------------------------

CREATE
(Washroom_45)-[:ROOM_IN]->(Room_45),
(Washroom_46)-[:ROOM_IN]->(Room_46)

CREATE
(Anchor_7)-[:PLACED_IN]->(Room_45),
(Anchor_11)-[:PLACED_IN]->(Room_45),
(Anchor_15)-[:PLACED_IN]->(Room_45)

CREATE
(Anchor_6)-[:PLACED_IN]->(Washroom_45),
(Anchor_10)-[:PLACED_IN]->(Washroom_45),
(Anchor_14)-[:PLACED_IN]->(Washroom_45)

CREATE
(Anchor_5)-[:PLACED_IN]->(Room_46),
(Anchor_2)-[:PLACED_IN]->(Room_46),
(Anchor_13)-[:PLACED_IN]->(Room_46)

CREATE
(Anchor_4)-[:PLACED_IN]->(Washroom_46),
(Anchor_8)-[:PLACED_IN]->(Washroom_46),
(Anchor_1)-[:PLACED_IN]->(Washroom_46)

CREATE
(Anchor_3)-[:PLACED_IN]->(Hallway),
(Anchor_9)-[:PLACED_IN]->(Hallway),
(Anchor_12)-[:PLACED_IN]->(Hallway)



CREATE
(Room_45)-[:CONTAINS_DEVICE]->(Anchor_7),
(Room_45)-[:CONTAINS_DEVICE]->(Anchor_11),
(Room_45)-[:CONTAINS_DEVICE]->(Anchor_15)

CREATE
(Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_6),
(Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_10),
(Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_14)

CREATE
(Room_46)-[:CONTAINS_DEVICE]->(Anchor_5),
(Room_46)-[:CONTAINS_DEVICE]->(Anchor_2),
(Room_46)-[:CONTAINS_DEVICE]->(Anchor_13)

CREATE
(Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_4),
(Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_8),
(Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_1)

CREATE
(Hallway)-[:CONTAINS_DEVICE]->(Anchor_3),
(Hallway)-[:CONTAINS_DEVICE]->(Anchor_9),
(Hallway)-[:CONTAINS_DEVICE]->(Anchor_12)



CREATE
(Tag_1)-[:CONNECTED_TO]->(Anchor_4),
(Tag_1)-[:CONNECTED_TO]->(Anchor_8),
(Tag_1)-[:CONNECTED_TO]->(Anchor_1)


CREATE
(Anchor_4)-[:ASSOCIATED_WITH]->(Tag_1),
(Anchor_8)-[:ASSOCIATED_WITH]->(Tag_1),
(Anchor_1)-[:ASSOCIATED_WITH]->(Tag_1)


CREATE
(Tag_1)-[:LOCATED_IN]->(Washroom_46)


CREATE
(Tag_1)-[:BELONGS_TO]->(P_1)


CREATE
(Tag_1)<-[:WEARS_DEVICE]-(P_1)


CREATE
(Washroom_46)-[:CONTAINS_PERSON]->(P_1)