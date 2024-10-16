using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using M2MqttUnity;
using uPLibrary.Networking.M2Mqtt.Messages;

public class MqttManager : M2MqttUnityClient
{

    public static MqttManager instance;
    public string sleepTimeTopic = "activity/time";

    public delegate void OnSleepTimeReceivedHandler(float sleepTime);
    public event OnSleepTimeReceivedHandler OnSleepTimeReceived;

    private void Awake () {
        if (instance == null) {
            instance = this;
            DontDestroyOnLoad(gameObject);
        } else {
            Destroy(gameObject);
        }
    }

    protected override void OnConnected() {
        base.OnConnected();
        Debug.Log("Connected to MQTT broker");
        SubscribeToSleepTimeTopic();
    }

    protected override void OnDisconnected() {
        base.OnDisconnected();
        Debug.Log("Disconnected from MQTT broker");
    }

    protected override void SubscribeTopics() {
        SubscribeToSleepTimeTopic();
    }

    protected override void UnsubscribeTopics() {
        client.Unsubscribe(new string[] { sleepTimeTopic });
    }

    private void SubscribeToSleepTimeTopic() {
        if (client != null && client.IsConnected) {
            Debug.Log("Subscribing to sleep time topic");
            client.Subscribe(new string[] { sleepTimeTopic }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        } else
        {
            Debug.LogError("Client not connected");
        }
    }

    protected override void Start () {
        base.Start();
        Connect();
    }

    protected override void DecodeMessage(string topic, byte[] message) {
        string messageString = Encoding.UTF8.GetString(message);
        Debug.Log($"Message received on topic {topic}: {messageString}");

        if (topic == sleepTimeTopic) {
            if (float.TryParse(messageString, out float sleepTime)) {
                Debug.Log($"Parsed sleep time: {sleepTime}");
                OnSleepTimeReceived?.Invoke(sleepTime);
            } else
            {
                Debug.LogError($"Failed to parse sleep time: {messageString}");
            }
        }
    }

    public void PublishMessage(string topic, string message) {
        if (client != null && client.IsConnected) {
            client.Publish(topic, Encoding.UTF8.GetBytes(message), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, true);
        }
    }
}
