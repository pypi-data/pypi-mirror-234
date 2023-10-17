"""Train a model using sklearn."""

import pathlib
import pickle

import pandas as pd
import sklearn.dummy  # type: ignore
import sklearn.neural_network  # type: ignore
import typer


def main(split_dataset_dir: pathlib.Path = typer.Option(...), output_dir: pathlib.Path = typer.Option(...)) -> None:
    """Read data from the split dataset step and train a model using Auto ML."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # Read data from the split dataset step
    train_df = pd.read_parquet(split_dataset_dir / "train.parquet")

    # train model
    model = sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(100, 100, 100), max_iter=500)

    model.fit(train_df.drop("target", axis=1), train_df["target"])

    # Save the model as a pickle file
    with open(output_dir / "model.pkl", "wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    typer.run(main)
