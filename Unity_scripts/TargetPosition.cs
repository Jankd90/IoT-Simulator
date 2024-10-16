using System;
using System.Collections.Generic;
using UnityEngine;
using M2MqttUnity;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using System.Text;
using Newtonsoft.Json;

public class TargetPosition : MonoBehaviour
{
    private MqttClient client;
    private string brokerHostname = ""; // Add the broker host IP here
    private int brokerPort = 0000; // Add the broker port here
    private string topic = "activity/position";
    private Queue<Action> mainThreadActions = new Queue<Action>();

    private void Start()
    {
        client = new MqttClient(brokerHostname, brokerPort, false, null, null, MqttSslProtocols.None);
        client.MqttMsgPublishReceived += OnMessageReceived;
        string clientId = Guid.NewGuid().ToString();
        client.Connect(clientId);

        client.Subscribe(new string[] { topic }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
    }

    private void Update()
    {
        lock (mainThreadActions)
        {
            while (mainThreadActions.Count > 0)
            {
                mainThreadActions.Dequeue().Invoke();
            }
        }
    }

    private void OnMessageReceived(object sender, MqttMsgPublishEventArgs e)
    {
        string message = Encoding.UTF8.GetString(e.Message);

        PositionData positionData = JsonConvert.DeserializeObject<PositionData>(message);

        if (positionData != null)
        {
            Vector3 newPosition = new Vector3(positionData.x, positionData.y, positionData.z);
            QueueMainThreadAction(() => UpdatePosition(newPosition));
        }
    }

    private void QueueMainThreadAction(Action action)
    {
        lock (mainThreadActions)
        {
            mainThreadActions.Enqueue(action);
        }
    }

    private void UpdatePosition(Vector3 newPosition)
    {
        transform.position = newPosition;
    }

    private void OnDestroy()
    {
        if (client != null && client.IsConnected)
        {
            client.Disconnect();
        }
    }
}

[System.Serializable]
public class PositionData
{
    public float x;
    public float y;
    public float z;
}
