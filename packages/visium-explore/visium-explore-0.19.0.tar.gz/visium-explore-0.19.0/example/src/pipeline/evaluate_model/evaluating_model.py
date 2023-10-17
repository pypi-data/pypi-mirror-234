"""Evaluate the model using test data."""
import pathlib
import pickle

import pandas as pd
import typer


def main(
    train_model_dir: pathlib.Path = typer.Option(...),
    split_dataset_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Evaluate the model using test data."""
    # Read data from the split dataset step
    test_df = pd.read_parquet(split_dataset_dir / "test.parquet")

    # Read the model from the train model step
    with open(train_model_dir / "model.pkl", "rb") as file:
        model = pickle.load(file)

    # Evaluate the model
    accuracy = model.score(test_df.drop("target", axis=1), test_df["target"])

    # Save the accuracy as a json file
    with open(pathlib.Path("metrics/metrics.json"), "w", encoding="utf-8") as file:
        file.write(f'{{"accuracy": {accuracy}}}')


if __name__ == "__main__":
    typer.run(main)
