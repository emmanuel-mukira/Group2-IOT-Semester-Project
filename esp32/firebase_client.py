# =================================================
# firebase_client.py
# Firebase Realtime Database upload logic
# =================================================

import ujson

try:
    import urequests
except ImportError:
    urequests = None

from config import FIREBASE_URL


def publish_firebase(payload):
    """
    Uploads payload to Firebase Realtime Database.

    CHANGE:
    Update FIREBASE_URL in config.py.

    IMPORTANT:
    Firebase Realtime Database REST URLs must end with .json

    Example:
    https://your-project.firebaseio.com/latest_readings.json

    The PUT method overwrites the latest_readings node.
    Use POST instead if you want to store historical readings.
    """

    if urequests is None:
        print("Firebase publish failed: urequests library not available")
        return False

    try:
        response = urequests.put(
            FIREBASE_URL,
            data=ujson.dumps(payload)
        )

        print("Firebase published:", response.status_code)

        # Critical on ESP32 to avoid memory issues.
        response.close()

        return True

    except Exception as e:
        print("Firebase publish failed:", e)

        return False
