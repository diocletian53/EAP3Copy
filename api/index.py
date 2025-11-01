from flask import Flask, request, send_file, jsonify
from process_excel import process_excels
import os

# --- Flask setup ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "EAP Excel Processing API is running"})


@app.route("/process", methods=["POST"])
def process_files():
    """
    Endpoint to process Excel files.
    Expects:
    - 'main_file' (file)
    - 'master_file' (file)
    - 'carrier' (str): FedEx, OnTrac, UPS
    """
    main_file = request.files.get("main_file")
    master_file = request.files.get("master_file")
    carrier = request.form.get("carrier")

    # Validate input
    if not main_file or not master_file or not carrier:
        return jsonify({"error": "Please upload both files and select a carrier"}), 400

    try:
        # Process Excel files
        output = process_excels(main_file, master_file, carrier)

        # Send back the processed Excel file
        return send_file(
            output,
            as_attachment=True,
            download_name="Processed_Output.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500


# --- Health check ---
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "EAP Flask API running successfully"})


# --- Entry point for local development ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
