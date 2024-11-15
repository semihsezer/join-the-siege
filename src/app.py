from datetime import datetime, time
from flask import Flask, request, jsonify

from src.classifier import classify_file, ClassifierType
from src.extractors import SUPPORTED_FILE_TYPES

app = Flask(__name__)

ALLOWED_EXTENSIONS = SUPPORTED_FILE_TYPES


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/classify_file", methods=["POST"])
def classify_file_route():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    classifier = request.args.get("classifier", ClassifierType.CONTENT)
    convert_pdf_to_image = request.args.get("convert_pdf_to_image", False)

    if classifier not in ClassifierType:
        raise ValueError(f"Unsupported classifier: {classifier}. "
                         f"Has to be one of: {ClassifierType}")

    try:
        start_time = datetime.now()
        classification = classify_file(file, classifier, convert_pdf_to_image)
        duration = (datetime.now() - start_time).seconds
        return jsonify({"file_class": classification,
                        "duration_seconds": duration}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
