import os
import pandas as pd
from flask import Flask, request, render_template, send_file
import pickle
import matplotlib.pyplot as plt
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Load pre-trained model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)
    
    
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    store_id = request.form.get("store_id")
    csv_file = request.files["csv_file"]

    # Save uploaded CSV to uploads folder
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], csv_file.filename)
    csv_file.save(filepath)

    # Load CSV data
    data = pd.read_csv(filepath)

    # Add store_id and other necessary columns to data
    data["Store_id"] = store_id

    # Perform predictions
    predictions = model.predict(data)
    data["Predicted_Sales"] = predictions[:, 0]  # Assuming first column is sales
    data["Predicted_Customers"] = predictions[:, 1]  # Second column is customer count

    # Create plot of predictions
    plt.figure(figsize=(10, 5))
    plt.plot(data["Date"], data["Predicted_Sales"], label="Predicted Sales")
    plt.plot(data["Date"], data["Predicted_Customers"], label="Predicted Customers")
    plt.xlabel("Date")
    plt.ylabel("Predictions")
    plt.legend()
    plt.tight_layout()

    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    # Return a downloadable CSV file of predictions
    output_csv = os.path.join(app.config["UPLOAD_FOLDER"], "predictions.csv")
    data.to_csv(output_csv, index=False)

    return send_file(
        img, mimetype="image/png", as_attachment=False,
        download_name="predictions.png",
        attachment_filename="predictions.png"
    )


@app.route("/download_predictions", methods=["GET"])
def download_predictions():
    output_csv = os.path.join(app.config["UPLOAD_FOLDER"], "predictions.csv")
    return send_file(output_csv, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

