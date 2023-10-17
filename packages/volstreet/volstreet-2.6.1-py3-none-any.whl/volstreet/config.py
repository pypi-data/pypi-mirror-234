import urllib
import requests
import pandas as pd
import logging
from datetime import datetime
import joblib
from importlib.resources import files
from pathlib import Path
from threading import local
from bs4 import BeautifulSoup


def get_ticker_file():
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data = urllib.request.urlopen(url).read().decode()
    df = pd.read_json(data)
    return df


def fetch_holidays():
    url = "https://zerodha.com/marketintel/holiday-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.132 Safari/537.36"
    }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser")

    # Create empty lists to hold the extracted data in a targeted manner
    targeted_holiday_dates = []
    targeted_holiday_names = []
    targeted_holiday_tags = []
    targeted_holiday_exchanges = []

    # Directly look for elements that contain the holiday information by targeting specific child classes
    targeted_rows = soup.find_all("li", class_="row")

    # Loop through the targeted "row" elements to extract holiday information
    for row in targeted_rows:
        date_element = row.find(class_="holiday-date")
        name_element = row.find(class_="holiday-name")
        tag_element = row.find(class_="tag")

        if date_element and name_element and tag_element:
            if tag_element.text.strip() == "trading":
                targeted_holiday_dates.append(date_element.text.strip())
                targeted_holiday_names.append(name_element.text.strip())
                targeted_holiday_tags.append(tag_element.text.strip())

    # Convert the extracted data into a Pandas DataFrame
    targeted_holiday_df = pd.DataFrame(
        {
            "Date": targeted_holiday_dates,
            "Holiday Name": targeted_holiday_names,
            "Tag": targeted_holiday_tags,
        }
    )
    targeted_holiday_df["Date"] = pd.to_datetime(targeted_holiday_df["Date"])
    holidays = targeted_holiday_df["Date"].values
    holidays = holidays.astype("datetime64[D]")
    return holidays


def get_symbols():
    try:
        freeze_qty_url = "https://archives.nseindia.com/content/fo/qtyfreeze.xls"
        response = requests.get(freeze_qty_url, timeout=10)  # Set the timeout value
        response.raise_for_status()  # Raise an exception if the response contains an HTTP error status
        df = pd.read_excel(response.content)
        df.columns = df.columns.str.strip()
        df["SYMBOL"] = df["SYMBOL"].str.strip()
        return df
    except Exception as e:
        logger.error(f"Error while fetching symbols: {e}")
        return pd.DataFrame()


def load_iv_models():
    resource_path = files("volstreet").joinpath("iv_models")

    # noinspection PyTypeChecker
    curve_model_path = Path(resource_path.joinpath("iv_curve_adjuster.joblib"))
    # noinspection PyTypeChecker
    vix_to_iv_model_path = Path(resource_path.joinpath("vix_to_iv.joblib"))
    # noinspection PyTypeChecker
    atm_iv_on_expiry_day_model_path = Path(
        resource_path.joinpath("atm_iv_on_expiry_day.joblib")
    )

    models = []
    for model_path in [
        curve_model_path,
        vix_to_iv_model_path,
        atm_iv_on_expiry_day_model_path,
    ]:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
            models.append(model)
    return tuple(models)


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    today = datetime.now().strftime("%Y-%m-%d")

    # Create handlers

    # Info handler
    info_log_filename = f"info-{today}.log"
    info_handler = logging.FileHandler(info_log_filename)
    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
    )
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    # Error handler
    error_log_filename = f"error-{today}.log"
    error_handler = logging.FileHandler(error_log_filename)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    # Stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)  # Set the level as per your requirement
    logger.addHandler(stream_handler)

    return logger


# Set the default values for critical variables
NOTIFIER_LEVEL = "INFO"
LARGE_ORDER_THRESHOLD = 10
ERROR_NOTIFICATION_SETTINGS = {"url": None}
LIMIT_PRICE_BUFFER = 0.01

# Create logger
logger = create_logger("volstreet")

# Get the list of scrips
scrips = get_ticker_file()
scrips["expiry_dt"] = pd.to_datetime(
    scrips[scrips.expiry != ""]["expiry"], format="%d%b%Y"
)
scrips["expiry_formatted"] = scrips["expiry_dt"].dt.strftime("%d%b%y")
scrips["expiry_formatted"] = scrips["expiry_formatted"].str.upper()

# Create a dictionary of token and symbol
token_symbol_dict = dict(zip(scrips["token"], scrips["symbol"]))

# Create a dictionary of token and exchange segment
token_exchange_dict = dict(zip(scrips["token"], scrips["exch_seg"]))

# Get the list of holidays
try:
    holidays = fetch_holidays()
except Exception as e:
    logger.error(f"Error while fetching holidays: {e}")
    holidays = pd.to_datetime([])

# Get the list of symbols
symbol_df = get_symbols()

# Load the iv models
iv_curve_model, vix_to_iv_model, expiry_day_model = load_iv_models()

# Create a thread local object
thread_local = local()
