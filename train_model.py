import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Dummy training data with 40 features (to match your model expectations)
X_train = np.random.rand(100, 40)
y_train = np.random.rand(100)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save with scikit-learn 1.7.0
joblib.dump(model, "trained_model.joblib")

print("✅ Model retrained and saved cleanly under scikit-learn 1.7.0")
