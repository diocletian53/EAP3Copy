from flask import Flask, render_template, request, send_file
from process_excel import process_excels
import os

# --- Flask setup ---
app = Flask(
    __name__,
    template_folder="templates",  # Ensure templates folder is at this path
    static_folder="static"        # Optional static folder
)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page for uploading Excel files and selecting carrier.
    Handles POST to process Excel and returns output file.
    """
    if request.method == "POST":
        # --- Get uploaded files ---
        main_file = request.files.get("main_file")
        master_file = request.files.get("master_file")
        vlookup_file = request.files.get("vlookup_file")  # optional
        carrier = request.form.get("carrier")

        # --- Basic validation ---
        if not main_file or not master_file or not carrier:
            return render_template(
                "index.html",
                error="⚠️ Please upload both main & master files and select a carrier."
            )

        try:
            # --- Run Excel processing ---
            output = process_excels(main_file, master_file, carrier, vlookup_file)

            # --- Return processed Excel file to user ---
            return send_file(
                output,
                as_attachment=True,
                download_name="Processed_Output.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            # --- Catch errors and display ---
            return render_template(
                "index.html",
                error=f"❌ Processing failed: {str(e)}"
            )

    # --- GET request renders form ---
    return render_template("index.html")


@app.route("/health")
def health():
    """
    Health check route
    """
    return {"status": "ok", "message": "EAP Flask app running successfully"}


# --- Run app ---
if __name__ == "__main__":
    # Get port from environment (e.g., for Vercel deployment)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
