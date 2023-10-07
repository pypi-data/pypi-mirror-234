import polars as pl
from typing import Any, List, Literal, Dict, Optional, Tuple


class FindSplit:
    def __init__(self):
        self.model = None
        self.seed: int = 0
        self.predictor_cols: List[Any] = []
        self.target_col: str = ""
        self.predictor_splits: List[Any] = []
        self.predictor_directions: List[Optional[Literal[">=", "<"]]] = []
        self.rows_evaled: int = 0
        self.running_tpr: float = 0.0

    def apply_splits(self, df: pl.DataFrame, target_col: str) -> Tuple[int, int]:
        for split_idx, split in enumerate(self.predictor_splits):
            if self.predictor_directions[split[split_idx]] == ">=":
                df = df.filter(df.filter(pl.col(split)) >= split[split_idx])
            elif self.predictor_directions[split[split_idx]] == "<":
                df = df.filter(df.filter(pl.col(split)) < split[split_idx])
        nb_pred_pos_labels: int = df.select(pl.count()).collect()[0,0]
        return nb_true_pos_labels, nb_pred_pos_labels

    def fit_predict(self, df: pl.DataFrame, target_col: str) -> pl.Series:
        self.target_col = target_col
        nb_true_pos_labels, nb_pred_pos_labels = self.apply_splits(df, target_col)
        preds = df[target_col]
        return preds

    def learn(self, df: pl.DataFrame, target_col: str):


class CausalBoost:
    def __init__(self):
        self.model = None
        self.seed: int = 0
        self.minmax_scaler: Dict[str, Optional[pl.Series]] = {"min": None, "max": None}

    def increase_seed(self) -> None:
        self.seed += 1

    def sample_row(self, df: pl.DataFrame) -> pl.DataFrame:
        df_sample = df.sample(n=1, with_replacement=True, seed=self.seed)
        return df_sample

    def min_max_scaler_fit(self, df: pl.DataFrame) -> pl.DataFrame:
        self.minmax_scaler["min"] = df.min()
        self.minmax_scaler["max"] = df.max()
        df_scaled = (df - self.minmax_scaler["min"]) / (self.minmax_scaler["max"] - self.minmax_scaler["min"])
        return df_scaled

    def min_max_scaler_predict(self, df: pl.DataFrame) -> pl.DataFrame:
        df_scaled = (df - self.minmax_scaler["min"]) / (self.minmax_scaler["max"] - self.minmax_scaler["min"])
        return df_scaled

    def fit(self, df: pl.DataFrame, target_col: str) -> None:
        df = self.min_max_scaler_fit(df)

    def predict(self, df: pl.DataFrame) -> pl.Series:
        df = self.min_max_scaler_predict(df)
        return preds
