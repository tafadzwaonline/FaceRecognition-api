from flask import Flask, request, jsonify
from face_utils import decode_base64_image, encode_face, verify_face
import numpy as np
import face_recognition


app = Flask(__name__)
known_faces = {}

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        image_base64 = data.get("image")

        if not user_id or not image_base64:
            return jsonify({"error": "Missing user_id or image"}), 400

        image = decode_base64_image(image_base64)
        if image is None:
            return jsonify({"error": "Invalid image data"}), 400

        encoding = encode_face(image)
        if encoding is None:
            return jsonify({"error": "Face not detected"}), 400

        known_faces[user_id] = encoding.tolist()
        #return jsonify({"message": "Face registered successfully"}), 200
        return jsonify({"message": "Face registered successfully","encoding": encoding.tolist()}), 200
    except Exception as ex:
        print("Register error:", ex)
        return jsonify({"error": "Internal error"}), 500


@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    image_base64 = data.get("image")
    known_encoding_list = data.get("known_encoding")

    if not image_base64 or not known_encoding_list:
        return jsonify({"error": "Missing data"}), 400

    image = decode_base64_image(image_base64)
    if image is None:
        return jsonify({"error": "Invalid image data"}), 400

    test_encoding = encode_face(image)
    if test_encoding is None:
        return jsonify({"error": "Face not detected"}), 400

    try:
        known_encoding = np.array(known_encoding_list)
        test_encoding = np.array(test_encoding)
        distance = face_recognition.face_distance([known_encoding], test_encoding)[0]
        match = distance < 0.45  # strict threshold

        return jsonify({
            "match": bool(match),
            "distance": float(distance),
            "threshold": 0.45
        }), 200
    except Exception as e:
        print("Verification error:", e)
        return jsonify({"error": "Internal server error"}), 500




if __name__ == "__main__":
    app.run(debug=True, port=5000)
