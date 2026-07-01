import os
import json

import tensorflow as tf
from tensorflow.keras import layers, models


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATASET_DIR = os.getenv("DATASET_PATH", os.path.join(BASE_DIR, "dataset"))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "dent_cavity_cnn.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")
IMAGE_SIZE = (300, 300)
BATCH_SIZE = 16
EPOCHS = 12


def build_model():
    model = models.Sequential(
        [
            layers.Input(shape=(300, 300, 3)),
            layers.Rescaling(1.0 / 255),
            layers.Conv2D(32, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Conv2D(128, 3, activation="relu"),
            layers.MaxPooling2D(),
            layers.Dropout(0.25),
            layers.Flatten(),
            layers.Dense(128, activation="relu"),
            layers.Dropout(0.35),
            layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def main():
    if not os.path.exists(DATASET_DIR):
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
    )
    class_names = train_ds.class_names
    print("Class names:", class_names)
    print(f"Important: sigmoid output is probability of class index 1: {class_names[1]}.")
    if len(class_names) != 2:
        raise ValueError("This binary CNN expects exactly two dataset folders.")

    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.06),
            layers.RandomZoom(0.08),
        ]
    )
    train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y)).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    model = build_model()
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor="val_accuracy", save_best_only=True),
    ]
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
        json.dump({"class_names": class_names}, f, indent=2)
    model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)
    model.save(MODEL_PATH)
    print(f"Saved trained CNN model to {MODEL_PATH}")
    print(f"Saved class-name mapping to {CLASS_NAMES_PATH}")


if __name__ == "__main__":
    main()
