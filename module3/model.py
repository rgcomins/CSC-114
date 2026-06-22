"""
CSC 114 — Apply AI Frameworks
MNIST handwritten-digit classifier (Keras + PyTorch backend)

This script carries out the four-step build plan from
CSC114_Apply_AI_Frameworks_Notes.md:

    Step 1 — Build:   load MNIST and define the model architecture
    Step 2 — Compile: pick loss, optimizer, and metrics
    Step 3 — Fit:     train the model, printing every epoch + the error rate
    Step 4 — Predict: save the most accurate model, reload it, run a prediction

Every training epoch is printed to the screen together with the error rate
(error rate = 1 - accuracy). The single most accurate version of the model
(highest validation accuracy across all epochs) is saved to disk.
"""

import os

# Use PyTorch as the Keras backend (see "Decisions Made" in the notes).
# This MUST be set before keras is imported.
os.environ["KERAS_BACKEND"] = "torch"

import keras
from keras import layers


# Where the best model gets written. Keras infers the format from the
# extension; ".keras" is the recommended native format.
BEST_MODEL_PATH = "mnist_best_model.keras"
EPOCHS = 20
BATCH_SIZE = 128


class EpochReporter(keras.callbacks.Callback):
    """Prints a clean per-epoch summary including the error rate.

    Keras already prints a progress bar per epoch; this callback adds an
    explicit, easy-to-read line so the error rate is obvious at every step.
    """

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        acc = logs.get("accuracy", 0.0)
        val_acc = logs.get("val_accuracy", 0.0)
        loss = logs.get("loss", 0.0)
        val_loss = logs.get("val_loss", 0.0)

        # Error rate is simply the fraction of examples classified wrong.
        train_error = 1.0 - acc
        val_error = 1.0 - val_acc

        print(
            f"Epoch {epoch + 1:>2}/{EPOCHS}  "
            f"loss={loss:.4f}  acc={acc:.4f}  err={train_error:.4f}  |  "
            f"val_loss={val_loss:.4f}  val_acc={val_acc:.4f}  "
            f"val_err={val_error:.4f}"
        )


def build_model():
    """Step 1 — define the model architecture."""
    model = keras.Sequential([
        layers.Dense(512, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ])
    return model


def main():
    # ------------------------------------------------------------------
    # Step 1 — Build: load data & define the model architecture
    # ------------------------------------------------------------------
    print("Step 1 — Loading MNIST and building the model...")

    # MNIST comes pre-split into train/test, already labeled.
    (train_images, train_labels), (test_images, test_labels) = \
        keras.datasets.mnist.load_data()

    # Flatten each 28x28 image into one 784-number row, scale 0-255 -> 0-1.
    train_images = train_images.reshape((60000, 28 * 28)).astype("float32") / 255
    test_images = test_images.reshape((10000, 28 * 28)).astype("float32") / 255

    model = build_model()

    # ------------------------------------------------------------------
    # Step 2 — Compile: choose loss, optimizer, metrics
    # ------------------------------------------------------------------
    print("Step 2 — Compiling the model (adam + sparse categorical crossentropy)...")
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # ------------------------------------------------------------------
    # Step 3 — Fit: train the model
    # ------------------------------------------------------------------
    print(f"Step 3 — Training for up to {EPOCHS} epochs...\n")

    # Save ONLY the most accurate model seen so far, judged by validation
    # accuracy. save_best_only=True overwrites the file only when val_accuracy
    # improves, so the file on disk is always the single best version.
    checkpoint = keras.callbacks.ModelCheckpoint(
        filepath=BEST_MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1,
    )

    history = model.fit(
        train_images,
        train_labels,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(test_images, test_labels),
        callbacks=[EpochReporter(), checkpoint],
        verbose=1,
    )

    # Report the best epoch / accuracy / lowest error reached during training.
    val_accs = history.history["val_accuracy"]
    best_idx = max(range(len(val_accs)), key=lambda i: val_accs[i])
    best_val_acc = val_accs[best_idx]
    best_val_loss = history.history["val_loss"][best_idx]

    print("\n----- Training summary -----")
    print(f"Best epoch:            {best_idx + 1}")
    print(f"Best validation acc:   {best_val_acc:.4f}")
    print(f"Lowest error rate:     {1.0 - best_val_acc:.4f}")
    print(f"Loss at best epoch:    {best_val_loss:.4f}")
    print(f"Best model saved to:   {BEST_MODEL_PATH}")

    # ------------------------------------------------------------------
    # Step 4 — Predict: reload the best model and run a prediction
    # ------------------------------------------------------------------
    print("\nStep 4 — Reloading the best saved model and predicting on one test image...")
    best_model = keras.models.load_model(BEST_MODEL_PATH)

    sample = test_images[:1]                     # one image, shape (1, 784)
    probabilities = best_model.predict(sample, verbose=0)
    predicted_digit = int(probabilities.argmax(axis=1)[0])

    print(f"Predicted digit: {predicted_digit}")
    print(f"Actual digit:    {int(test_labels[0])}")
    print(f"Confidence:      {float(probabilities[0][predicted_digit]):.4f}")


if __name__ == "__main__":
    main()
