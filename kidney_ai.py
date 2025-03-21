import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ✅ 1. Generate Sample Data (Replace with real patient-donor data later)
data = {
    "blood_type_match": np.random.randint(0, 2, 500),  # 1 = Match, 0 = No Match
    "age_difference": np.random.randint(0, 50, 500),   # Age difference between donor & patient
    "tissue_match_score": np.random.randint(50, 100, 500),  # Higher score = better match
    "compatibility_score": np.random.rand(500) * 100  # AI Target Score (0-100)
}

df = pd.DataFrame(data)

# ✅ 2. Preprocess Data
X = df.drop("compatibility_score", axis=1)  # Features
y = df["compatibility_score"]  # Target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ✅ 3. Split Data into Training & Testing
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ✅ 4. Create AI Model (Neural Network)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')  # Output: Compatibility Score
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# ✅ 5. Train the AI Model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# ✅ 6. Test AI Model on a New Donor-Patient Pair
new_donor = np.array([[1, 10, 85]])  # Example: Blood type match, 10-year age diff, 85 tissue score
new_donor_scaled = scaler.transform(new_donor)
predicted_score = model.predict(new_donor_scaled)

print(f"Predicted Compatibility Score: {predicted_score[0][0]:.2f}")
