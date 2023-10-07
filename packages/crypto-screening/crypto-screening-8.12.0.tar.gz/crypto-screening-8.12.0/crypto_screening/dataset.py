# dataset.py

import os
import datetime as dt
import json
from pathlib import Path
from typing import (
    Union, Optional, Tuple, Iterable,
    Any, Callable, Dict, List
)

import numpy as np
import pandas as pd
from pandas.core.resample import Resampler

from crypto_screening.interval import interval_total_time

__all__ = [
    "row_to_dataset",
    "save_dataset",
    "load_dataset",
    "update_dataset",
    "split_dataset",
    "strip_dataset",
    "validate_dataset",
    "OHLCV_COLUMNS",
    "OHLC_COLUMNS",
    "OPEN",
    "CLOSE",
    "HIGH",
    "LOW",
    "VOLUME",
    "DATE_TIME",
    "BIDS",
    "ASKS",
    "find_column",
    "validate_file_extension",
    "dataset_to_json",
    "dataset_from_json",
    "EXTENSIONS",
    "validate_file_path",
    "is_valid_location",
    "prepare_saving_location",
    "BIDS_VOLUME",
    "ASKS_VOLUME",
    "CSV_EXTENSION",
    "JSON_EXTENSION",
    "DEFAULT_EXTENSION",
    "bid_ask_to_ohlcv",
    "create_dataset",
    "ORDERBOOK_COLUMNS",
    "TRADES_COLUMNS",
    "PRICE",
    "SIDE",
    "BUY",
    "SELL",
    "TICKERS_COLUMNS",
    "AMOUNT",
    "adjust_series",
    "interval_adjuster",
    "index_to_datetime",
    "new_dataset_index",
    "bid_ask_to_tickers",
    "trades_to_tickers",
    "trades_to_bid_ask"
]

DATE_TIME = 'DateTime'

OPEN = "Open"
CLOSE = "Close"
HIGH = "High"
LOW = "Low"
VOLUME = "Volume"

BIDS = "Bids"
ASKS = "Asks"
BIDS_VOLUME = "BidsVolume"
ASKS_VOLUME = "AsksVolume"

AMOUNT = "Amount"
PRICE = "Price"
SIDE = "Side"
BUY = 'buy'
SELL = 'sell'

OHLC_COLUMNS = (OPEN, HIGH, LOW, CLOSE)
OHLCV_COLUMNS = (*OHLC_COLUMNS, VOLUME)
ORDERBOOK_COLUMNS = (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME)
TRADES_COLUMNS = (AMOUNT, PRICE, SIDE)
TICKERS_COLUMNS = (BIDS, ASKS)

def index_to_datetime(index: Any, adjust: Optional[bool] = True) -> dt.datetime:
    """
    Converts the index into a datetime object.

    :param index: The value to convert.
    :param adjust: The value to adjust the process for errors.

    :return: The datetime object.
    """

    try:
        if isinstance(index, str):
            index = dt.datetime.fromisoformat(index)

        elif isinstance(index, (int, float)):
            index = dt.datetime.fromtimestamp(index)

        elif isinstance(index, pd.Timestamp):
            index = index.to_pydatetime()

        elif isinstance(index, np.datetime64):
            index = index.astype(dt.datetime)
        # end if

    except (TypeError, ValueError) as e:
        if adjust:
            pass

        else:
            raise e
        # end if
    # end try

    return index
# end index_to_datetime

def row_to_dataset(
        dataset: Union[pd.DataFrame, pd.Series],
        index: Optional[int] = None
) -> pd.DataFrame:
    """
    Creates a dataframe from the row.

    :param dataset: The base dataset from witch the row came.
    :param index: The index of the row to create a dataset for.

    :return: The dataset from the row.
    """

    if isinstance(dataset, pd.DataFrame):
        if index is None:
            raise ValueError(
                f"Index must an int when dataset "
                f"is of type {pd.DataFrame}."
            )
        # end if

        return pd.DataFrame(
            {
                column: [value] for column, value in
                dict(dataset.iloc[index]).items()
            },
            index=[dataset.index[index]]
        )

    elif isinstance(dataset, pd.Series):
        return pd.DataFrame(
            {
                column: [value] for column, value in
                dict(dataset).items()
            },
            index=[index or 0]
        )

    else:
        raise TypeError(
            f"Dataset must be either of type {pd.DataFrame}, "
            f"or {pd.Series}, not {type(dataset)}."
        )
    # end if
# end row_to_dataset

def update_dataset(base: pd.DataFrame, new: pd.DataFrame) -> None:
    """
    Updates the ba se dataframe with new columns from the new dataframe.

    :param base: The base dataframe to update.
    :param new: The new dataframe with the new columns.
    """

    if not len(base) == len(new):
        raise ValueError(
            f"DataFrames lengths must match "
            f"(got {len(base)} and {len(new)} instead)."
        )
    # end if

    for column in new.columns:
        if column not in base.columns:
            base[column] = new[column]
        # end if
    # end for
# end update_dataset

def split_dataset(
        dataset: Union[pd.DataFrame, pd.Series],
        size: Optional[Union[int, float]] = None,
        length: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the new_dataset into to parts at the point of the given size.

    :param dataset: The new_dataset to split.
    :param size: The size of the first part.
    :param length: The length of the split.

    :return: The two datasets.
    """

    if (size is None) and (length is None):
        raise ValueError(
            "Cannot split the dataset when neither "
            "size nor length parameters are defined."
        )
    # end if

    length = length or int(len(dataset) * size)

    return dataset[:length], dataset[length:]
# end split_dataset

def strip_dataset(dataset: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """
    Strips the columns from the new_dataset.

    :param dataset: The new_dataset to remove features from.
    :param columns: The columns to validate.

    :return: The new new_dataset.
    """

    return dataset.drop(
        [
            column for column in columns
            if column in dataset.columns
        ], axis=1
    )
# end strip_dataset

def validate_dataset(
        dataset: pd.DataFrame,
        columns: Optional[Iterable[str]] = None,
        length: Optional[int] = None
) -> None:
    """
    Validates the new_dataset to have the columns.

    :param dataset: The new_dataset to validate.
    :param columns: The columns to validate.
    :param length: The length of the valid dataset.
    """

    if (
        (columns is not None) and
        not all(column in dataset.columns for column in columns)
    ):
        missing = [
            column for column in columns
            if column not in list(dataset.columns)
        ]

        redundant = [
            column for column in list(dataset.columns)
            if column not in columns
        ]

        raise ValueError(
            f"DataFrame must include the "
            f"columns by the names: {columns}.\n"
            f"Given columns: {', '.join(dataset.columns)}.\n"
            f"Missing columns: {missing}.\n"
            f"Redundant columns: {redundant}."
        )
    # end if

    if (length is not None) and len(dataset) != length:
        raise ValueError(
            f"Dataset must have length of {length}, "
            f"not: {len(dataset)}."
        )
    # end if
# end validate_dataset

def dataset_to_json(dataset: pd.DataFrame) -> List[Union[str, Dict[str, Any]]]:
    """
    Converts the data of the dataset to json.

    :param dataset: The dataset to process.

    :return: The json representation of the data.
    """

    return list(json.loads(dataset.to_json(orient='index')).items())
# end dataset_to_json

def dataset_from_json(
        data: Union[Dict[str, Dict[str, Any]], List[Union[str, Dict[str, Any]]]]
) -> pd.DataFrame:
    """
    Converts the data from json format into a dataframe object.

    :param data: The json data to process.

    :return: The data frame object.
    """

    if isinstance(data, list):
        data = dict(data)
    # end if

    return pd.read_json(json.dumps(data), orient="index")
# end dataset_from_json

CSV_EXTENSION = "csv"
JSON_EXTENSION = "json"
DEFAULT_EXTENSION = CSV_EXTENSION

EXTENSIONS = (CSV_EXTENSION, JSON_EXTENSION)

def validate_file_extension(
        path: Union[str, Path],
        extension: Optional[str] = None
) -> str:
    """
    Validates the file formatting.

    :param path: The path to the file.
    :param extension: The data formatting.

    :return: The valid formatting.
    """

    path = str(path)

    if extension is None:
        if "." not in path:
            raise ValueError(
                f"Cannot infer file type and data "
                f"format from path: {path} and undefined formatting. "
                f"You may need to specify file extension in the path "
                f"or pass the 'formatting' parameter ({', '.join(EXTENSIONS)})."
            )
        # end if

        extension = path[path.rfind(".") + 1:]
    # end if

    if extension not in EXTENSIONS:
        raise ValueError(
            f"Invalid formatting value: {extension}. "
            f"value formatting options are: {', '.join(EXTENSIONS)}."
        )
    # end if

    return extension
# end validate_file_extension

def is_valid_location(path: Union[str, Path]) -> bool:
    """
    Prepares the saving location.

    :param path: The path for the file to save.

    :return: The value of creating the location directory.
    """

    location = os.path.split(path)[0]

    return (
        ((not location) and path) or
        (location and os.path.exists(location))
    )
# end is_valid_location

def validate_file_path(
        path: Union[str, Path],
        create: Optional[bool] = True,
        override: Optional[bool] = True
) -> None:
    """
    Validates the file formatting.

    :param path: The path to the file.
    :param create: The value to create the path location.
    :param override: The value to override an existing file.

    :return: The valid formatting.
    """

    if create:
        prepare_saving_location(path=path)

    elif not is_valid_location(path=path):
        raise ValueError(
            f"Invalid file saving "
            f"location: {os.path.split(path)[0]} of {path}."
        )
    # end if

    if os.path.exists(path) and not override:
        raise FileExistsError(
            f"Attempting to override an existing file: "
            f"{path} while 'override' is set to {override}."
        )
    # end if
# end validate_file_path

def prepare_saving_location(path: Union[str, Path]) -> bool:
    """
    Prepares the saving location.

    :param path: The path for the file to save.

    :return: The value of creating the location directory.
    """

    location = os.path.split(path)[0]

    if location:
        value = os.path.exists(location)

        os.makedirs(location, exist_ok=True)

        return value

    else:
        return False
    # end if
# end prepare_saving_location

def save_dataset(
        dataset: pd.DataFrame,
        path: Union[str, Path],
        headers: Optional[bool] = None,
        create: Optional[bool] = True,
        override: Optional[bool] = True,
        append: Optional[bool] = False,
        extension: Optional[str] = None
) -> None:
    """
    Saves the data.

    :param dataset: The dataset to save.
    :param create: The value to create the path location.
    :param headers: The value to include headers.
    :param override: The value to override an existing file.
    :param path: The saving path.
    :param append: The value to append data to the file.
    :param extension: The formatting of the data.
    """

    if extension is None:
        extension = DEFAULT_EXTENSION
    # end if

    if headers is None:
        headers = not append
    # end if

    path = str(path)

    extension = validate_file_extension(path=path, extension=extension)

    validate_file_path(path=path, create=create, override=override)

    if extension == CSV_EXTENSION:
        dataset.to_csv(path, mode='a' if append else "w", header=headers)

    elif extension == JSON_EXTENSION:
        with open(path, "w") as file:
            json.dump(dataset_to_json(dataset), file)
        # end open
    # end if
# end save_dataset

def load_dataset(
        path: Union[str, Path],
        extension: Optional[str] = None,
        index_column: Optional[Union[int, bool]] = 0,
        time_index: Optional[bool] = True
) -> pd.DataFrame:
    """
    Loads the dataset from the path.

    :param path: The saving path.
    :param extension: The formatting of the data.
    :param index_column: The value to set the index for the column.
    :param time_index: The value to se the index as datetime.

    :return: The loaded dataset.
    """

    if extension is None:
        extension = DEFAULT_EXTENSION
    # end if

    path = str(path)

    extension = validate_file_extension(path=path, extension=extension)

    if extension == CSV_EXTENSION:
        dataset = pd.read_csv(path)

    elif extension == JSON_EXTENSION:
        with open(path, "r") as file:
            dataset = dataset_to_json(json.load(file))
        # end open
    # end if

    if index_column is True:
        index_column = 0
    # end if

    if index_column is not None or index_column is False:
        index_column_name = list(dataset.columns)[index_column]
        dataset.index = (
            pd.DatetimeIndex(dataset[index_column_name])
            if time_index else dataset[index_column_name]
        )
        del dataset[index_column_name]
        dataset.index.name = DATE_TIME
    # end if

    return dataset
# end load_dataset

def find_column(
        dataset: pd.DataFrame,
        columns: Iterable[Any],
        validation: Optional[Callable[[pd.Series], bool]] = None
) -> Optional[pd.Series]:
    """
    Finds the first valid column and returns it.

    :param dataset: The dataset to search.
    :param columns: The column names to search from, by order.
    :param validation: The validation function.

    :return: The valid column.
    """

    for column in columns:
        if column not in dataset:
            continue
        # end if

        if (
            (validation is None) or
            (callable(validation) and validation(dataset[column]))
        ):
            return dataset[column]
        # end if
    # end for
# end find_column

def interval_adjuster(interval: str) -> str:
    """
    Creates the adjuster for the interval.

    :param interval: The interval to adjust data with.

    :return: The adjusted interval.
    """

    return f'{interval_total_time(interval).total_seconds()}S'
# end interval_adjuster

def adjust_series(data: pd.Series, interval: str) -> Resampler:
    """
    Converts the dataset into a dataset with an interval.

    :param data: The source data.
    :param interval: The interval for the new dataset.

    :return: The returned dataset.
    """

    return data.resample(interval_adjuster(interval))
# end adjust_dataset

def bid_ask_to_ohlcv(dataset: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Converts the BID/ASK spread dataset into a OHLCV dataset.

    :param dataset: The source data.
    :param interval: The interval for the new dataset.

    :return: The returned dataset.
    """

    if not all(column in ORDERBOOK_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(ORDERBOOK_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )
    # end if

    adjuster = interval_adjuster(interval)

    ohlcv_dataset = dataset[BIDS].resample(adjuster).ohlc()
    ohlcv_dataset.columns = list(OHLC_COLUMNS)
    ohlcv_dataset[VOLUME] = dataset[BIDS_VOLUME].resample(adjuster).mean()

    return ohlcv_dataset
# end bid_ask_to_ohlcv

def bid_ask_to_tickers(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the BID/ASK spread dataset into a tickers' dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    if not all(column in TICKERS_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(TICKERS_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )
    # end if

    return dataset.copy()[list(TICKERS_COLUMNS)]
# end bid_ask_to_ohlcv

def trades_to_bid_ask(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the trades spread dataset into a BID/ASK dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    if not all(column in TRADES_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(TRADES_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )
    # end if

    bid = None
    ask = None
    bid_volume = None
    ask_volume = None

    results = create_dataset(ORDERBOOK_COLUMNS)

    for index, data in dataset.iterrows():
        if data[SIDE] == BUY:
            ask = data[PRICE]
            ask_volume = data[VOLUME]

        elif data[SIDE] == SELL:
            bid = data[PRICE]
            bid_volume = data[VOLUME]

        else:
            continue
        # end if

        if None in (bid, ask, bid_volume, ask_volume):
            continue
        # end if

        results[index] = {
            BIDS: bid, ASKS: ask,
            BIDS_VOLUME: bid_volume, ASKS_VOLUME: ask_volume
        }
    # end for

    return results
# end trades_to_bid_ask

def trades_to_tickers(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the trades spread dataset into a tickers' dataset.

    :param dataset: The source data.

    :return: The returned dataset.
    """

    return bid_ask_to_tickers(trades_to_bid_ask(dataset))
# end trades_to_tickers

def create_dataset(columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns or []}, index=[]
    )
    market.index.name = DATE_TIME

    return market
# end create_dataset

def new_dataset_index(index: dt.datetime, dataset: pd.DataFrame) -> bool:
    """
    Checks if the index is new and valid to the dataset.

    :param index: The index to check.
    :param dataset: The dataset to validate the index for.

    :return: The validation of the index as new.
    """

    return (
        (len(dataset.index) == 0) or
        (
            isinstance(dataset.index[-1], dt.datetime) and
            (dataset.index[-1] < index)
        ) or
        (index not in dataset.index)
    )
# end new_dataset_index