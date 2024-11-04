from flask import Flask, jsonify
import mlflow


# Initialize the Flask app
app = Flask(__name__)
@app.route('/')
def new():
    return "Welcome to the Flask & MLflow Demonstration!"

@app.route('/Peehu', methods=['GET'])
def log_data():
    # Create or set the experiment
    mlflow.set_experiment("Flask_MLflow_Demo")

    # Start an MLflow run
    with mlflow.start_run():
        # Sample data to log
        sample_data = {
            "param1": 100,
            "param2": 200,
            "description": "Sample parameters logged to MLflow"
        }
      

        # Log parameters to MLflow
        for key, value in sample_data.items():
            mlflow.log_param(key, value)
    
       # Log a simple metric
        mlflow.log_metric("sample_metric", 1.23)

 
    return jsonify(sample_data)

if __name__ == '__main__':

    app.run(debug=True,port=5001)