from flask import Flask, render_template, request, send_file
from process_excel import process_excels
import io
import os

# --- Flask setup ---
app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get uploaded files
        main_file = request.files.get("main_file")
        master_file = request.files.get("master_file")
        carrier = request.form.get("carrier")  # radio button value

        # Validate user input
        if not main_file or not master_file or not carrier:
            return render_template(
                "index.html",
                error="⚠️ Please upload both files and select a carrier before processing."
            )

        try:
            # Call your Excel processor function
            output = process_excels(main_file, master_file, carrier)

            # Send back the processed Excel file
            return send_file(
                output,
                as_attachment=True,
                download_name="Processed_Output.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            # Display any error message on the page
            return render_template("index.html", error=f"❌ Processing failed: {str(e)}")

    # Default page (GET request)
    return render_template("index.html")


# --- Health check route ---
@app.route("/health")
def health():
    return {"status": "ok", "message": "EAP Flask app running successfully"}


# --- Entry point for Vercel and local development ---
if __name__ != "__main__":
    # Vercel looks for a WSGI callable named 'app'
    app = app
else:
    # Run locally
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
