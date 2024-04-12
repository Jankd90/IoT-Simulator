//-------------------------------------------
// Object Device
//-------------------------------------------

//------------
// Anchors
//------------

//------------
// Approach 1 //
//------------

CREATE (:Device {deviceName: 'Anchor_1',                    // MQTT : /ip/deviceName
                            deviceType: 'ESP32_UWB_ANCHOR', // MQTT : /ip/deviceType
                            MAC: 'ff:ff:ff:ff',             // MQTT : /ip/MAC
                            status: 'active',               // MQTT : /ip/status
                            connected: 'True',              // MQTT : /ip/status/connected
                            FeatureOfInterest: 'TAG_1',     // MQTT : /deviceName/FeatureOfInterest
                            observation: '1m',              // MQTT : /deviceName/observation/Result
                            UWB_frequency: 112500,          // MQTT : /ip/SENSOR_NAME/Frequency
                            communication_frequency: 50})   // MQTT : /ip/communication/Frequency



//------------
// Approach 2 //
//------------

// Create a base Device node
CREATE (:Device {
    ipAddress: '1.1.1.1'  // /ip/ipAddress
})

// Add properties obtained from MQTT topics
MATCH (d:Device {ipAddress: '1.1.1.1'})
SET d.deviceName = 'Anchor_2',           // /ip/deviceName
    d.deviceType = 'ESP32_UWB_ANCHOR',   // /ip/deviceType
    d.MAC = 'ff:ff:ff:ff',               // /ip/MAC
    d.status = 'active',                 // /ip/status
    d.connected = true                   // /ip/status/connected (assuming 'True' represents boolean true)

// Create FeatureOfInterest node
MERGE (:FeatureOfInterest {tag: 'TAG_1'})  // /deviceName/FeatureOfInterest

// Create observation node
MERGE (:Observation {result: '1m'})  // /deviceName/observation/Result

// Add configuration properties obtained from MQTT topics
MATCH (d:Device {deviceName: 'Anchor_2'})
SET d.UWB_frequency = 112500,          // /ip/SENSOR_NAME/Frequency
    d.communication_frequency = 50     // /ip/communication/Frequency



//------------
// Approach 3 //
//------------

// Create a base Device node
CREATE (:Device {
    ipAddress: '1.1.1.2'  // /ip/ipAddress
})

// Add properties obtained from MQTT topics
MATCH (d:Device {ipAddress: '1.1.1.2'})
SET d.deviceName = 'Anchor_3',           // /ip/deviceName
    d.deviceType = 'ESP32_UWB_ANCHOR',   // /ip/deviceType
    d.MAC = 'ff:ff:ff:ff',               // /ip/MAC
    d.status = 'active',                 // /ip/status
    d.connected = true                   // /ip/status/connected (assuming 'True' represents boolean true)

// Add configuration properties obtained from MQTT topics
SET d.UWB_frequency = 112500,          // /ip/SENSOR_NAME/Frequency
    d.communication_frequency = 50     // /ip/communication/Frequency


MATCH (d:Device {deviceName:'Anchor_3'})
// Add feature of intrest
SET d.FeatureOfInterest = 'TAG_1'  // /deviceName/FeatureOfInterest

// Add observation
SET d.Observation = '1m'  // /deviceName/observation/Result
