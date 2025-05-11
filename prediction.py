import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
from datetime import datetime


def main():
    model_path = "model/best_model.keras"
    gray_dir = "data/test_gray"
    gt_dir = "data/ground_truth"
    out_csv = "submission.csv"

    model = load_model(model_path, compile=False)
    print(f"Loaded model: {model_path}")

    files = sorted(
        [f for f in os.listdir(gray_dir) if os.path.isfile(os.path.join(gray_dir, f))]
    )
    if not files:
        raise RuntimeError(f"No files found in {gray_dir}")

    mse_vals = []

    for fname in files:
        img_gray = (
            Image.open(os.path.join(gray_dir, fname))
            .convert("L")
            .resize((32, 32), Image.BILINEAR)
        )
        arr_gray = np.array(img_gray, dtype=np.float32) / 255.0
        arr_gray = arr_gray[..., None][None, ...]

        pred = model.predict(arr_gray, verbose=0)[0]

        img_gt = (
            Image.open(os.path.join(gt_dir, fname))
            .convert("RGB")
            .resize((32, 32), Image.BILINEAR)
        )
        arr_gt = np.array(img_gt, dtype=np.float32) / 255.0

        mse_vals.append(np.mean((pred - arr_gt) ** 2))

    mse_mean = np.mean(mse_vals)

    score = mse_mean * 100

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([{"date": date_str, "score": score}])
    df.to_csv(out_csv, index=False)
    print(f"Saved summary to {out_csv}")
    print(df)


if __name__ == "__main__":
    main()
