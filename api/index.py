from flask import Flask, render_template, request, send_file
from process_excel import process_excels
import os

# --- Flask setup ---
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get uploaded files
        main_file = request.files.get("main_file")
        master_file = request.files.get("master_file")
        vlookup_file = request.files.get("vlookup_file")  # optional
        carrier = request.form.get("carrier")

        # Validate input
        if not main_file or not master_file or not carrier:
            return render_template(
                "index.html",
                error="⚠️ Please upload both main and master files and select a carrier."
            )

        try:
            # Process the Excel files
            output = process_excels(main_file, master_file, carrier, vlookup_file)

            # Return the processed Excel file to the user
            return send_file(
                output,
                as_attachment=True,
                download_name="Processed_Output.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            # Show error on frontend
            return render_template(
                "index.html",
                error=f"❌ Processing failed: {str(e)}"
            )

    # GET request: render the upload form
    return render_template("index.html")


# --- Health check route ---
@app.route("/health")
def health():
    return {"status": "ok", "message": "Home Depot Excel Processor Flask app running successfully"}


# --- Run Flask app locally or via Vercel ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
