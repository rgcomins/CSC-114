import os
os.environ["KERAS_BACKEND"] = "torch"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import keras
import numpy as np
import matplotlib.pyplot as plt

# Load model and data
model = keras.models.load_model("mnist_best_model.keras", compile=False)
(_, _), (x_test, y_test) = keras.datasets.mnist.load_data()

# Pick an image
index = 1
image = x_test[index]

# Preprocess and predict
image_input = image.astype("float32") / 255.0
image_input = image_input.reshape(1, 784)

prediction = model.predict(image_input)
predicted_class = prediction.argmax()

# Save image to file
plt.imshow(image, cmap="gray")
plt.title(f"Actual: {y_test[index]}  |  Predicted: {predicted_class}")
plt.axis("off")
plt.savefig("prediction.png", bbox_inches="tight")
plt.close()

print(f"Predicted: {predicted_class}")
print(f"Actual:    {y_test[index]}")