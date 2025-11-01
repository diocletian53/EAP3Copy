from flask import Flask, render_template, request, send_file, redirect, url_for
from process_excel import process_excels
import io
import os

# --- Flask setup ---
app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        main_file = request.files.get("main_file")
        master_file = request.files.get("master_file")
        carrier = request.form.get("carrier")  # <-- read radio button

        # Check for missing inputs
        if not main_file or not master_file or not carrier:
            return render_template(
                "index.html",
                error="⚠️ Please upload both files and select a carrier before processing."
            )

        try:
            # Run main processing
            output = process_excels(main_file, master_file, carrier)

            # Return the processed Excel file
            return send_file(
                output,
                as_attachment=True,
                download_name="Processed_Output.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            # Capture and show any processing errors
            return render_template("index.html", error=f"❌ Processing failed: {str(e)}")

    # Render the upload form by default
    return render_template("index.html")

# --- Health check route ---
@app.route("/health")
def health():
    return {"status": "ok", "message": "EAP Flask app running successfully"}

# --- Vercel entry point ---
if __name__ != "__main__":
    app = app  # for Vercel
else:
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
