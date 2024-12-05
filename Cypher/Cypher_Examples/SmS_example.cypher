// MATCH (n)
// DETACH DELETE n

//-------------------------------------------
// Object Person
//-------------------------------------------
CREATE (P_1:Person {name:'Person 1', main_room:'Room_46'}),
       (P_2:Person {name:'Person 2', main_room:'Room_46'}),
       (P_3:Person {name:'Person 3', main_room:'Room_46'}),
       (P_4:Person {name:'Person 4', main_room:'Room_46'}),
       (P_5:Person {name:'Person 5', main_room:'Room_46'})


//-------------------------------------------
// Object Device
//-------------------------------------------

//------------
// Tags
//------------
CREATE (Tag_1:Device {sensor_type:'UWB Tag', name:'TAG001', battery_level:80, data_rate:112500, manufacturer:'Makerfabs', status:'active'}),
       (Tag_2:Device {sensor_type:'UWB Tag', name:'TAG002', battery_level:85, data_rate:125000, manufacturer:'Makerfabs', status:'active'}),
       (Tag_3:Device {sensor_type:'UWB Tag', name:'TAG002', battery_level:85, data_rate:125000, manufacturer:'Makerfabs', status:'active'}),
       (Tag_4:Device {sensor_type:'UWB Tag', name:'TAG002', battery_level:85, data_rate:125000, manufacturer:'Makerfabs', status:'active'}),
       (Tag_5:Device {sensor_type:'UWB Tag', name:'TAG003', battery_level:90, data_rate:120000, manufacturer:'Makerfabs', status:'active'})


//------------
// Anchors
//------------
CREATE (Anchor_1:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR001', distance_to_tag: '1.5m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_2:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR002', distance_to_tag: '2m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_3:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR003', distance_to_tag: '1.8m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_4:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR004', distance_to_tag: '1.2m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_5:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR005', distance_to_tag: '1.7m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_6:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR006', distance_to_tag: '1.4m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_7:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR007', distance_to_tag: '1.6m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_8:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR008', distance_to_tag: '1.3m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_9:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR009', distance_to_tag: '1.1m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_10:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR010', distance_to_tag: '1.9m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_11:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR011', distance_to_tag: '1.8m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_12:Device {sensor_type:'UWB Anchor', communication_type:'Wi-Fi', name: 'ANCHOR012', distance_to_tag: '1.5m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_13:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR013', distance_to_tag: '1.3m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_14:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR014', distance_to_tag: '1.7m', connectivity_status: 'connected', status: 'active'}),
       (Anchor_15:Device {sensor_type:'UWB Anchor', communication_type:'BLE', name: 'ANCHOR015', distance_to_tag: '1.2m', connectivity_status: 'connected', status: 'active'})

//-------------------------------------------
// Object Room
//-------------------------------------------

CREATE (Room_45:Room {name: 'Room 45', room_number: 'r45', floor: '4'}),
       (Room_46:Room {name: 'Room 46', room_number: 'r46', floor: '4'}),
       (Washroom_45:Room {name: 'W_room 45', room_number: 'wr45', floor: '4'}),
       (Washroom_46:Room {name: 'W_room 46', room_number: 'wr46', floor: '4'}),
       (Hallway:Room {name: 'Hallway', floor: '4'})

//-------------------------------------------
// Relationships
//-------------------------------------------

// Room In Relationships
CREATE (Washroom_45)-[:ROOM_IN]->(Room_45),
       (Washroom_46)-[:ROOM_IN]->(Room_46)

// Placed In Relationships
CREATE (Anchor_1)-[:PLACED_IN]->(Room_45),
       (Anchor_2)-[:PLACED_IN]->(Room_45),
       (Anchor_3)-[:PLACED_IN]->(Room_45),
       (Anchor_4)-[:PLACED_IN]->(Washroom_46),
       (Anchor_5)-[:PLACED_IN]->(Washroom_46),
       (Anchor_6)-[:PLACED_IN]->(Washroom_46),
       (Anchor_7)-[:PLACED_IN]->(Room_46),
       (Anchor_8)-[:PLACED_IN]->(Room_46),
       (Anchor_9)-[:PLACED_IN]->(Room_46),
       (Anchor_10)-[:PLACED_IN]->(Washroom_45),
       (Anchor_11)-[:PLACED_IN]->(Washroom_45),
       (Anchor_12)-[:PLACED_IN]->(Washroom_45),
       (Anchor_13)-[:PLACED_IN]->(Hallway),
       (Anchor_14)-[:PLACED_IN]->(Hallway),
       (Anchor_15)-[:PLACED_IN]->(Hallway)

// Contains Device Relationships
CREATE (Room_45)-[:CONTAINS_DEVICE]->(Anchor_1),
       (Room_45)-[:CONTAINS_DEVICE]->(Anchor_2),
       (Room_45)-[:CONTAINS_DEVICE]->(Anchor_3),
       (Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_4),
       (Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_5),
       (Washroom_46)-[:CONTAINS_DEVICE]->(Anchor_6),
       (Room_46)-[:CONTAINS_DEVICE]->(Anchor_7),
       (Room_46)-[:CONTAINS_DEVICE]->(Anchor_8),
       (Room_46)-[:CONTAINS_DEVICE]->(Anchor_9),
       (Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_10),
       (Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_11),
       (Washroom_45)-[:CONTAINS_DEVICE]->(Anchor_12),
       (Hallway)-[:CONTAINS_DEVICE]->(Anchor_13),
       (Hallway)-[:CONTAINS_DEVICE]->(Anchor_14),
       (Hallway)-[:CONTAINS_DEVICE]->(Anchor_15)

// Connected To Relationships
CREATE (Tag_1)-[:CONNECTED_TO]->(Anchor_1),
       (Tag_1)-[:CONNECTED_TO]->(Anchor_2),
       (Tag_1)-[:CONNECTED_TO]->(Anchor_3),
       (Tag_2)-[:CONNECTED_TO]->(Anchor_4),
       (Tag_2)-[:CONNECTED_TO]->(Anchor_5),
       (Tag_2)-[:CONNECTED_TO]->(Anchor_6),
       (Tag_3)-[:CONNECTED_TO]->(Anchor_7),
       (Tag_3)-[:CONNECTED_TO]->(Anchor_8),
       (Tag_3)-[:CONNECTED_TO]->(Anchor_9),
       (Tag_4)-[:CONNECTED_TO]->(Anchor_10),
       (Tag_4)-[:CONNECTED_TO]->(Anchor_11),
       (Tag_4)-[:CONNECTED_TO]->(Anchor_12),
       (Tag_5)-[:CONNECTED_TO]->(Anchor_13),
       (Tag_5)-[:CONNECTED_TO]->(Anchor_14),
       (Tag_5)-[:CONNECTED_TO]->(Anchor_15)

// Associated With Relationships
CREATE (Tag_1)<-[:ASSOCIATED_WITH]-(Anchor_1),
       (Tag_1)<-[:ASSOCIATED_WITH]-(Anchor_2),
       (Tag_1)<-[:ASSOCIATED_WITH]-(Anchor_3),
       (Tag_2)<-[:ASSOCIATED_WITH]-(Anchor_4),
       (Tag_2)<-[:ASSOCIATED_WITH]-(Anchor_5),
       (Tag_2)<-[:ASSOCIATED_WITH]-(Anchor_6),
       (Tag_3)<-[:ASSOCIATED_WITH]-(Anchor_7),
       (Tag_3)<-[:ASSOCIATED_WITH]-(Anchor_8),
       (Tag_3)<-[:ASSOCIATED_WITH]-(Anchor_9),
       (Tag_4)<-[:ASSOCIATED_WITH]-(Anchor_10),
       (Tag_4)<-[:ASSOCIATED_WITH]-(Anchor_11),
       (Tag_4)<-[:ASSOCIATED_WITH]-(Anchor_12),
       (Tag_5)<-[:ASSOCIATED_WITH]-(Anchor_13),
       (Tag_5)<-[:ASSOCIATED_WITH]-(Anchor_14),
       (Tag_5)<-[:ASSOCIATED_WITH]-(Anchor_15)

// Located In Relationships
CREATE (Tag_1)-[:LOCATED_IN]->(Room_45),
       (Tag_2)-[:LOCATED_IN]->(Washroom_46),
       (Tag_3)-[:LOCATED_IN]->(Room_46),
       (Tag_4)-[:LOCATED_IN]->(Washroom_45),
       (Tag_5)-[:LOCATED_IN]->(Hallway)
// Contains Person Relationships
CREATE (Tag_1)<-[:CONTAINS_TAG]-(Room_45),
       (Tag_2)<-[:CONTAINS_TAG]-(Washroom_46),
       (Tag_3)<-[:CONTAINS_TAG]-(Room_46),
       (Tag_4)<-[:CONTAINS_TAG]-(Washroom_45),
       (Tag_5)<-[:CONTAINS_TAG]-(Hallway)

// Belongs To Relationships
CREATE (Tag_1)-[:BELONGS_TO]->(P_1),
       (Tag_2)-[:BELONGS_TO]->(P_2),
       (Tag_3)-[:BELONGS_TO]->(P_3),
       (Tag_4)-[:BELONGS_TO]->(P_4),
       (Tag_5)-[:BELONGS_TO]->(P_5)

// Wears Device Relationships
CREATE (Tag_1)<-[:WEARS_DEVICE]-(P_1),
       (Tag_2)<-[:WEARS_DEVICE]-(P_2),
       (Tag_3)<-[:WEARS_DEVICE]-(P_3),
       (Tag_4)<-[:WEARS_DEVICE]-(P_4),
       (Tag_5)<-[:WEARS_DEVICE]-(P_5)