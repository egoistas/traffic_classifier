import pandas as pd
import joblib


processed_data = pd.read_csv("final_features_for_prediction.csv")

model = joblib.load("random_forest_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")  


predictions = model.predict(processed_data)

predicted_labels = label_encoder.inverse_transform(predictions)

processed_data['predictions'] = predictions
processed_data['predicted_category'] = predicted_labels

processed_data.to_csv("predictions_with_categories.csv", index=False)

print(processed_data[['predictions', 'predicted_category']].head())

print("Predictions saved to 'predictions_with_categories.csv'")
