# coins.py

import json
from pathlib import Path
import os
import shutil
from typing import Optional, Iterable, Dict, Union

from attrs import define

from represent import represent

import pandas as pd

from crypto_info.base import source, assets
from crypto_info.table import table_to_json

__all__ = [
    "raw_coins",
    "Coin",
    "load_coins",
    "load_coins_data",
    "extract_coins_data",
    "get_coins_logos",
    "save_coins_data",
    "COLOR_LOGO_CATEGORY",
    "BLACK_LOGO_CATEGORY",
    "LOGO_CATEGORIES",
    "ICON_LOGO_CATEGORY",
    "WHITE_LOGO_CATEGORY",
    "save_coins_logos",
    "load_coins_prices",
    "load_coins_table",
    "PRICE_USD_COLUMN",
    "NAME_COLUMN",
    "ID_COLUMN"
]

@define(repr=False, unsafe_hash=True)
@represent
class Coin:
    """A class to represent the data of a coin."""

    id: str
    name: str
# end Coin

CoinsDats = Dict[str, Dict[str, Union[str, float]]]

raw_coins: CoinsDats = {}

DATA_LOCATION = f"{source()}/data"
LOGOS_LOCATION = f"{assets()}/logos/coins"

PRICE_USD_COLUMN = "price_usd"
NAME_COLUMN = "name"
ID_COLUMN = "id"

def load_coins_table() -> pd.DataFrame:
    """
    Loads the table of coins.

    :return: The table of coin data.
    """

    df = pd.read_html("https://coinmarketcap.com/")[0]
    df = df[list(df.columns)[2:4]]

    names = []
    titles = []

    for i, text in enumerate(df["Name"], start=1):
        if str(i) in text:
            title = text[:text.find(str(i))]
            name = text[text.find(str(i)) + len(str(i)):]

        elif text == 'Binance USDBUSD':
            title = "Binance USD"
            name = "BUSD"

        elif text == "TRONTRX":
            title = "TRON"
            name = "TRX"

        elif text == "UNUS SED LEOLEO":
            title = "UNUS SED LEO"
            name = "name"

        elif text == "TrueUSDTUSD":
            title = "TrueUSD"
            name = "TUSD"

        elif text == "IOTAMIOTA":
            title = "IOTA"
            name = "MIOTA"

        elif text == "MultiversXEGLD":
            title = "MultiversX"
            name = "EGLD"

        elif text == "BitTorrent(New)BTT":
            title = "BitTorrent"
            name = "BTT"

        else:
            j = 0

            for j in range(len(text)):
                if text[j:] == text[j:].upper():
                    break
                # end if
            # end for

            title = text[:j]
            name = text[j:]

            if (
                (not title) and (len(name) >= 4) and
                (len(name) % 2 == 0) and
                (name[:len(name) // 2] == name[len(name) // 2:])
            ):
                name = title = name[:len(name) // 2]
            # end if

            if not title:
                title = name
            # end if
        # end if

        if not name:
            continue
        # end if

        if not title:
            title = name
        # end if

        if title == "Tether USDt":
            title = title[:-1]
        # end if

        if title == 'UNUS SED LEO':
            name = 'LEO'
            title = 'UNUS SED LEO'
        # end if

        titles.append(title)
        names.append(name.replace(" ", ""))
    # end for

    return pd.DataFrame(
        {
            ID_COLUMN: names,
            NAME_COLUMN: titles,
            PRICE_USD_COLUMN: [
                float(value[1:].replace(",", ""))
                for value in df["Price"]
            ]
        },
        index=df.index
    )
# end load_coins_table

def load_coins_data(
        coins: Optional[Iterable[str]] = None,
        reload: Optional[bool] = False,
        location: Optional[str] = None
) -> CoinsDats:
    """
    Loads the data of the coins.

    :param coins: The names of the assets.
    :param reload: The value to reload the data.
    :param location: The saving location.

    :return: The coins' data.
    """

    if location is None:
        location = DATA_LOCATION
    # end if

    path = f"{location}/coins.json"

    if os.path.exists(path) and not raw_coins:
        raw_coins.clear()

        with open(path, "r") as file:
            raw_coins.update(json.load(file))
        # end open
    # end if

    if reload or (not raw_coins):
        df = load_coins_table()

        raw_coins.update(
            {coin[ID_COLUMN]: coin for coin in table_to_json(df).values()}
        )

        for coin in raw_coins.values():
            coin.pop(PRICE_USD_COLUMN)
        # end for

        save_coins_data(data=raw_coins, destination=DATA_LOCATION)
    # end if

    data = json.loads(json.dumps(raw_coins))

    if coins is not None:
        data = {
            key: coin for key, coin in data.items()
            if key in coins
        }
    # end if

    return data
# end load_coins_data

def load_coins_prices(
        table: Optional[pd.DataFrame] = None,
        coins: Optional[Iterable[str]] = None
) -> Dict[str, float]:
    """
    Loads the data of the coins.

    :param table: The coins table to process.
    :param coins: The names of the assets.

    :return: The coins' data.
    """

    if table is None:
        table = load_coins_table()
    # end if

    data = {
        coin[ID_COLUMN]: coin[PRICE_USD_COLUMN]
        for coin in table_to_json(table).values()
        if coin[ID_COLUMN]
    }

    if coins is not None:
        data = {
            key: value for key, value in data.items()
            if key in coins
        }
    # end if

    return data
# end load_coins_prices

def save_coins_data(data: CoinsDats, destination: str) -> str:
    """
    Saves the logos of the coins.

    :param data: The coins' data.
    :param destination: The source location.

    :return: The paths to the logos of the coins.
    """

    os.makedirs(destination, exist_ok=True)

    path = f"{destination}/coins.json"

    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    # end open

    return path
# end save_coins_data

def save_coins_logos(coins: Iterable[str], destination: str) -> Dict[str, Dict[str, str]]:
    """
    Saves the logos of the coins.

    :param coins: The coins' data.
    :param destination: The saving location.

    :return: The paths to the logos of the coins.
    """

    os.makedirs(destination, exist_ok=True)

    paths: Dict[str, Dict[str, str]] = {}

    for category in LOGO_CATEGORIES:
        coins = get_coins_logos(coins=coins, category=category)

        for coin, path in coins.items():
            file_location = f"{destination}/{category}"

            os.makedirs(file_location, exist_ok=True)

            shutil.copy2(f"{file_location}/{coin}.png", path)

            paths.setdefault(coin, {}).setdefault(category, path)
        # end for
    # end for

    return paths
# end save_coins_logos

def load_coins(
        data: Optional[CoinsDats] = None,
        coins: Optional[Iterable[str]] = None,
        reload: Optional[bool] = False,
        location: Optional[str] = None
) -> Dict[str, Coin]:
    """
    Loads the data of the coins.

    :param data: The raw exchanges data.
    :param coins: The names of the assets.
    :param reload: The value to reload the data.
    :param location: The saving location.

    :return: The coins' data.
    """

    if data is None:
        data = load_coins_data(
            coins=coins, reload=reload, location=location
        )
    # end if

    return {key: Coin(**coin) for key, coin in data.items()}
# end load_coins

def extract_coins_data(coins: Union[Iterable[Coin], Dict[str, Coin]]) -> CoinsDats:
    """
    Extracts the data from the coins.

    :param coins: The coins to extract.

    :return: The extracted data of the coins.
    """

    if not isinstance(coins, dict):
        coins = {coin.id: coin for coin in coins}
    # end if

    return {
        key: coin.__dict__.copy()
        for key, coin in coins.items()
    }
# end extract_coins_data

WHITE_LOGO_CATEGORY = "white"
BLACK_LOGO_CATEGORY = "black"
ICON_LOGO_CATEGORY = "icon"
COLOR_LOGO_CATEGORY = "color"

LOGO_CATEGORIES = [
    WHITE_LOGO_CATEGORY, BLACK_LOGO_CATEGORY,
    ICON_LOGO_CATEGORY, COLOR_LOGO_CATEGORY
]

def get_coins_logos(
        coins: Optional[Iterable[str]] = None,
        category: Optional[str] = None,
        location: Optional[str] = None
) -> Dict[str, str]:
    """
    Returns the path to the logo files for each exchange.

    :param coins: The exchanges to search.
    :param category: The logo category.
    :param location: The saving location.

    :return: The exchanges and their logos.
    """

    if category is None:
        category = ICON_LOGO_CATEGORY
    # end if

    if coins is None:
        coins = load_coins_data().keys()
    # end if

    if category not in LOGO_CATEGORIES:
        raise ValueError(
            f"Coins logo category must be one of: "
            f"{','.join(LOGO_CATEGORIES)}, not: {category}"
        )
    # end if

    if location is None:
        location = LOGOS_LOCATION
    # end if

    return {
        coin: str(Path(f"{location}/{category}/{coin}.png"))
        for coin in coins
    }
# end get_exchanges_logos