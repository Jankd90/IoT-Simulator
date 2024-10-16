using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Text;
using Newtonsoft.Json;

public class ObjectPositionModifier : MonoBehaviour
{
    private MqttClient client;
    private string brokerHostname = ""; // Add the broker host IP here
    private int brokerPort = 0000; // Add the broker port here
    public string objectID;
    public string roomID;

    private string publishTopic;
    private string subscribeTopic;

    // Store the last published position to compare with the current position
    private Vector3 lastPublishedPosition;
    private float lastPublishedRotation;

    // private Queue<Action> mainThreadActions = new Queue<Action>();


    // Start is called before the first frame update
    void Start()
    {
        client = new MqttClient(brokerHostname, brokerPort, false, null, null, MqttSslProtocols.None);
        client.MqttMsgPublishReceived += OnMessageReceived;
        string clientId = System.Guid.NewGuid().ToString();
        client.Connect(clientId);

        // Define topics
        publishTopic = $"{roomID}/{objectID}/transform";
        subscribeTopic = $"config/{roomID}/{objectID}/transform";

        client.Subscribe(new string[] { subscribeTopic }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });

        // Publish object's position immediately when the script starts
        PublishTransform(transform.position, transform.rotation.eulerAngles.z);

        lastPublishedPosition = transform.position;
        lastPublishedRotation = NormalizeAngle(transform.rotation.eulerAngles.z);

        StartCoroutine(CheckAndPublishTransform());
    }

    void OnMessageReceived(object sender, MqttMsgPublishEventArgs e)
    {
        string message = Encoding.UTF8.GetString(e.Message);

        string[] transformData = message.Split(',');

        if (transformData.Length == 4)
        {
            // Parse position data (x, y, z)
            float x = float.Parse(transformData[0]);
            float y = float.Parse(transformData[1]);
            float z = float.Parse(transformData[2]);
            // Parse rotation data (z)
            float rotZ = float.Parse(transformData[3]);

            // Convert the angle from degrees to radians
            float rotZRadians = rotZ * Mathf.Deg2Rad;

            // Calculate the quaternion for the rotation around the Z-axis
            float cos = Mathf.Cos(rotZRadians / 2);
            float sin = Mathf.Sin(rotZRadians / 2);
            Quaternion rotationQuat = new Quaternion(0, 0, sin, cos);

            // // Update the object's position
            // transform.position = new Vector3(x, y, z);

            // Run the position update on the main thread using UnityMainThreadDispatcher
            UnityMainThreadDispatcher.Instance().Enqueue(() => {
                transform.position = new Vector3(x, y, z);
                transform.rotation = rotationQuat;
            });
        }
    }

    IEnumerator CheckAndPublishTransform() {

        while (true) {
            // Get current position and rotation of the object
            Vector3 currentPosition = transform.position;
            float currentRotation = NormalizeAngle(transform.rotation.eulerAngles.z);

            // Check if position is changed
            if (!currentPosition.Equals(lastPublishedPosition) || !currentRotation.Equals(lastPublishedRotation)) {
                
                // // Create the message in format "x,y,z"
                // string message = $"{currentPosition.x},{currentPosition.y},{currentPosition.z}";

                // // Publish the message
                // client.Publish(publishTopic, Encoding.UTF8.GetBytes(message), MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE, false);

                // Publish the new position if it has changed
                PublishTransform(currentPosition, currentRotation);
                
                // Update the last published position
                lastPublishedPosition = currentPosition;
                lastPublishedRotation = currentRotation;
            }

            // wait for 0.5 seconds before checking again
            yield return new WaitForSeconds(0.5f);
        }
    }

    float NormalizeAngle(float angle)
    {
        if (angle > 180)
            angle -= 360;
        return angle;
    }

    void PublishTransform(Vector3 position, float rotation) {
        
        // Create the message in format "x,y,z"
        string message = $"{position.x},{position.y},{position.z},{rotation}";

        // Publish the message
        client.Publish(publishTopic, Encoding.UTF8.GetBytes(message), MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE, false);
    }

    void OnDestroy() {
        // Disconnect the client when the object is destroyed
        if (client.IsConnected) {
            client.Disconnect();
        }
    }
}
