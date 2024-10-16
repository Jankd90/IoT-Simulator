/*
Adopted from https://github.com/SebLague/Pathfinding
*/

/*
MIT License

Copyright (c) 2017 Sebastian Lague

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Unit : MonoBehaviour {

	const float minPathUpdateTime = .2f;
	const float pathUpdateMoveThreshold = .01f;

	public Transform target;
	public float speed = 1;
	Vector3[] path;
	int targetIndex;
	float sleepTime;

	private bool _activityFinished;
	public bool activityFinished {
		get { return _activityFinished; }
		private set {
			if (_activityFinished != value) {
				_activityFinished = value;
				PublishToMqtt("activity/Finished", _activityFinished);
			}
		} 
	}

	void Start() {
		if (MqttManager.instance != null) {
			MqttManager.instance.OnSleepTimeReceived += SetSleepTime;
		}
		StartCoroutine (UpdatePath ());
	}

	public void OnPathFound(Vector3[] newPath, bool pathSuccessful) {
		if (pathSuccessful) {
			path = newPath;
			targetIndex = 0;
			activityFinished = false;
			StopCoroutine("FollowPath");
			StartCoroutine("FollowPath");
		}
	}

	IEnumerator UpdatePath() {

		if (Time.timeSinceLevelLoad < .3f) {
			yield return new WaitForSeconds (.3f);
		}
		PathRequestManager.RequestPath (transform.position, target.position, OnPathFound);

		float sqrMoveThreshold = pathUpdateMoveThreshold * pathUpdateMoveThreshold;
		Vector3 targetPosOld = target.position;

		while (true) {
			yield return new WaitForSeconds (minPathUpdateTime);
			if ((target.position - targetPosOld).sqrMagnitude > sqrMoveThreshold) {
				PathRequestManager.RequestPath (transform.position, target.position, OnPathFound);
				targetPosOld = target.position;
			}
		}
	}


	IEnumerator FollowPath() {
		Vector3 currentWaypoint = path[0];
		while (true) {
			if (transform.position == currentWaypoint) {
				targetIndex ++;
				if (targetIndex >= path.Length) {
					// SUBSCRIE TO MQTT AND ADD A STATEMENT INDICATING THE TIME OF THE ACTIVITY

					// Debug.Log("Path completed. Waiting for sleep time: " + sleepTime + " seconds");
                    yield return new WaitForSeconds(sleepTime);
                    // Debug.Log("Sleep time finished. Setting activityFinished to true.");


					// yield return new WaitForSeconds (sleepTime);
					activityFinished = true; // SET TO (TRUE) AFTER THE TIME OF ACTIVITY IS FINISHED AND PUBLISH IT TO MQTT
					yield break;
				}
				currentWaypoint = path[targetIndex];
			}

			transform.position = Vector3.MoveTowards(transform.position,currentWaypoint,speed * Time.deltaTime);
			yield return null;

		}
	}

	private void SetSleepTime(float newSleepTime) {
		// Debug.Log("Received new sleep time: " + newSleepTime);
		sleepTime = newSleepTime;
	}

	private void PublishToMqtt(string topic, bool value) {
		if (MqttManager.instance != null) {
			MqttManager.instance.PublishMessage(topic, value.ToString());
		}
	}

	public void OnDrawGizmos() {
		if (path != null) {
			for (int i = targetIndex; i < path.Length; i ++) {
				Gizmos.color = Color.black;
				// Gizmos.DrawCube(path[i], new Vector3(0.1f, 0.1f, 1));
				Gizmos.DrawCube(path[i], Vector3.one * 0.1f);


				if (i == targetIndex) {
					Gizmos.DrawLine(transform.position, path[i]);
				}
				else {
					Gizmos.DrawLine(path[i-1],path[i]);
				}
			}
		}
	}
}