import face_recognition
import numpy as np
import cv2
import base64

def decode_base64_image(base64_str):
    try:
        img_data = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Decoded image is None")
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        print("Image shape:", rgb_image.shape)
        return rgb_image
    except Exception as e:
        print("Decode error:", e)
        return None

#

def encode_face(image):
    try:
        encodings = face_recognition.face_encodings(image)
        print("Face encodings found:", len(encodings))

        if len(encodings) != 1:
            print("⚠️ Expected exactly one face, found:", len(encodings))
            return None  # Or raise a custom error

        return encodings[0]
    except Exception as e:
        print("Encoding error:", e)
        return None


def verify_face(known_encoding, test_encoding, tolerance=0.6):
    try:
        #result = face_recognition.compare_faces([known_encoding], test_encoding, tolerance)[0]
        result = face_recognition.compare_faces([known_encoding], test_encoding, tolerance=0.45)[0]

        print("Face match result:", result)
        return result
    except Exception as e:
        print("Verification error:", e)
        return False
