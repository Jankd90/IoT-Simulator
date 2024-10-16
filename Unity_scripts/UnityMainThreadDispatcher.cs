using System;
using System.Collections.Generic;
using UnityEngine;

public class UnityMainThreadDispatcher : MonoBehaviour
{
    // Queue for storing actions that need to be executed on the main thread
    private static readonly Queue<Action> _executionQueue = new Queue<Action>();

    // Singleton instance
    private static UnityMainThreadDispatcher _instance = null;

    // Ensure there's only one instance of UnityMainThreadDispatcher
    public static UnityMainThreadDispatcher Instance()
    {
        if (_instance == null)
        {
            throw new Exception("UnityMainThreadDispatcher is not initialized. Please add it to a GameObject in the scene.");
        }
        return _instance;
    }

    // Checks if the dispatcher instance exists
    public static bool Exists()
    {
        return _instance != null;
    }

    // This method allows other threads to enqueue actions to be executed on the main thread
    public void Enqueue(Action action)
    {
        lock (_executionQueue)
        {
            _executionQueue.Enqueue(action);
        }
    }

    // Update method processes all actions in the queue on the main thread
    void Update()
    {
        lock (_executionQueue)
        {
            while (_executionQueue.Count > 0)
            {
                _executionQueue.Dequeue().Invoke();
            }
        }
    }

    // Ensure the singleton instance is set when this script starts
    void Awake()
    {
        if (_instance == null)
        {
            _instance = this;
            DontDestroyOnLoad(this.gameObject);
        }
        else if (_instance != this)
        {
            Destroy(gameObject); // Enforce the singleton pattern
        }
    }

    // Clean up when the dispatcher is destroyed
    void OnDestroy()
    {
        if (_instance == this)
        {
            _instance = null;
        }
    }
}
