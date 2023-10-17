import volstreet as vs
import volstreet.datamodule as dm
import threading
from datetime import time
from time import sleep


def get_user_data(client, user, pin, apikey, authkey, webhook_url):
    # Checking if either client or user, pin, apikey and authkey are provided
    if client is None and (
        user is None or pin is None or apikey is None or authkey is None
    ):
        raise ValueError(
            "Either client or user, pin, apikey and authkey must be provided"
        )

    # If client is provided, user, pin, apikey and authkey will be fetched from the environment variables
    if client:
        user = __import__("os").environ[f"{client}_USER"]
        pin = __import__("os").environ[f"{client}_PIN"]
        apikey = __import__("os").environ[f"{client}_API_KEY"]
        authkey = __import__("os").environ[f"{client}_AUTHKEY"]

        if webhook_url is None:
            try:
                webhook_url = __import__("os").environ[f"{client}_WEBHOOK_URL"]
            except KeyError:
                webhook_url = None

    return user, pin, apikey, authkey, webhook_url


def initialize_client_and_login(client, user, pin, apikey, authkey, webhook_url):
    user, pin, apikey, authkey, discord_webhook_url = get_user_data(
        client, user, pin, apikey, authkey, webhook_url
    )

    # If today is a holiday, the script will exit
    if vs.currenttime().date() in vs.holidays:
        vs.notifier("Today is a holiday. Exiting.", discord_webhook_url, "CRUCIAL")
        exit()

    vs.login(
        user=user,
        pin=pin,
        apikey=apikey,
        authkey=authkey,
        webhook_url=discord_webhook_url,
    )

    return user, pin, apikey, authkey, discord_webhook_url


def save_strategy_data(
    index,
    strategy_tag,
    user,
    notification_url,
    default_structure,
    file_name=None,
):
    if file_name is None:
        strategy_tag_for_file_name = strategy_tag.lower().replace(" ", "_")
        file_name = f"{index.name}_{strategy_tag_for_file_name}.json"

    try:
        vs.load_combine_save_json_data(
            new_data=index.strategy_log[strategy_tag],
            file_name=file_name,
            user_id=user,
            notification_url=notification_url,
            default_structure=default_structure,
        )
        vs.notifier(
            f"Appended data for {strategy_tag.lower()} on {index.name}.",
            notification_url,
        )
    except Exception as e:
        vs.notifier(
            f"Appending {strategy_tag.lower()} data failed for {index.name}: {e}",
            notification_url,
        )


def intraday_options_on_indices(
    parameters,
    indices=None,
    client=None,
    user=None,
    pin=None,
    apikey=None,
    authkey=None,
    webhook_url=None,
    shared_data=True,
    start_time=(9, 16),
    safe_indices=None,
    only_expiry=False,
    special_parameters=None,
    strategy_tag="Intraday strangle",
):
    """
    :param parameters: parameters for the strategy (refer to the strategy's docstring)
    :param indices: list of indices to trade (default: ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"])
    :param client:
    :param user:
    :param pin:
    :param apikey:
    :param authkey:
    :param webhook_url:
    :param shared_data:
    :param start_time:
    :param safe_indices: list of indices to be traded when no clear close expiry is available
    :param only_expiry: if True, will trade only if any index has expiry today
    :param special_parameters: special parameters for a particular index
    :param strategy_tag: tag for the strategy (get creative if you want)
    :return:
    """

    user, pin, apikey, authkey, discord_webhook_url = initialize_client_and_login(
        client, user, pin, apikey, authkey, webhook_url
    )

    if special_parameters is None:
        special_parameters = {}

    if indices is None:
        indices = ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]

    indices = [vs.Index(index) for index in indices]

    indices = vs.get_strangle_indices_to_trade(
        *indices, safe_indices=safe_indices, only_expiry=only_expiry
    )

    if len(indices) == 0:
        vs.notifier("No indices to trade. Exiting.", discord_webhook_url, "INFO")
        return

    parameters["quantity_in_lots"] = max(
        parameters["quantity_in_lots"] // len(indices), 1
    )
    parameters["notification_url"] = discord_webhook_url
    parameters["strategy_tag"] = strategy_tag

    # Setting the shared data
    if shared_data:
        shared_data = vs.SharedData()
        update_data_thread = threading.Thread(target=shared_data.update_data)
        parameters["shared_data"] = shared_data
    else:
        shared_data = None
        update_data_thread = None

    options_threads = []
    for index in indices:
        index_parameters = parameters.copy()
        index_parameters.update(special_parameters.get(index.name, {}))
        vs.logger.info(
            f"Trading {index.name} strangle with parameters {index_parameters}"
        )
        vs.notifier(f"Trading {index.name} strangle.", discord_webhook_url)
        thread = threading.Thread(
            target=index.intraday_strangle, kwargs=index_parameters
        )
        options_threads.append(thread)

    # Wait for the market to open
    while vs.currenttime().time() < time(*start_time):
        sleep(1)

    # Start the data updater thread
    if shared_data and update_data_thread is not None:
        update_data_thread.start()

    # Start the options threads
    for thread in options_threads:
        thread.start()

    for thread in options_threads:
        thread.join()

    # Stop the data updater thread
    if shared_data and update_data_thread is not None:
        shared_data.force_stop = True
        update_data_thread.join()

    # Call the data appender function on the traded indices
    for index in indices:
        save_strategy_data(
            index=index,
            strategy_tag=strategy_tag,
            user=user,
            notification_url=discord_webhook_url,
            default_structure=list,
        )


def intraday_trend_on_indices(
    parameters,
    indices,
    client=None,
    user=None,
    pin=None,
    apikey=None,
    authkey=None,
    webhook_url=None,
    special_parameters=None,
    strategy_tag="Intraday trend",
):
    """

    :param parameters: parameters for the strategy (refer to the strategy's docstring)
                       summary of parameters:
                       quantity_in_lots,
                       start_time=(9, 15, 58),
                       exit_time=(15, 27),
                       sleep_time=5,
                       threshold_movement=None,
                       seconds_to_avg=45,
                       beta=0.8,
                       max_entries=3
    :param indices: list of indices to trade
    :param client: client's name
    :param user: username
    :param pin: user's pin
    :param apikey: user apikey
    :param authkey: user authkey
    :param webhook_url: discord webhook url
    :param special_parameters: special parameters for a particular index
    :param strategy_tag: tag for the strategy (get creative if you want)

    """

    user, pin, apikey, authkey, discord_webhook_url = initialize_client_and_login(
        client, user, pin, apikey, authkey, webhook_url
    )

    if special_parameters is None:
        special_parameters = {}

    indices = [vs.Index(index) for index in indices]

    parameters["notification_url"] = discord_webhook_url
    parameters["strategy_tag"] = strategy_tag

    threads = []
    for index in indices:
        index_parameters = parameters.copy()
        index_parameters.update(special_parameters.get(index.name, {}))
        thread = threading.Thread(target=index.intraday_trend, kwargs=index_parameters)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Call the data appender function on the traded indices
    for index in indices:
        save_strategy_data(
            index=index,
            strategy_tag=strategy_tag,
            user=user,
            notification_url=None,
            default_structure=list,
        )


def overnight_straddle_nifty(
    quantity_in_lots,
    take_avg_price=True,
    avg_till=(15, 28),
    strike_offset=1,
    hedge_buy_quantity_in_lots=None,
    hedge_call_offset=0.997,
    hedge_put_offset=0.98,
    client=None,
    user=None,
    pin=None,
    apikey=None,
    authkey=None,
    webhook_url=None,
    strategy_tags=None,
):
    user, pin, apikey, authkey, discord_webhook_url = initialize_client_and_login(
        client, user, pin, apikey, authkey, webhook_url
    )

    nifty = vs.Index("NIFTY")

    if strategy_tags is None:
        strategy_tags = ["Overnight short straddle", "Weekly hedge"]

    # Rolling over the short straddle
    nifty.overnight_straddle(
        quantity_in_lots,
        strike_offset=strike_offset,
        take_avg_price=take_avg_price,
        avg_till=avg_till,
        notification_url=discord_webhook_url,
        strategy_tag=strategy_tags[0],
    )

    # Buying next week's hedge if it is expiry day
    if vs.time_to_expiry(nifty.current_expiry, in_days=True) < 1:
        nifty.buy_weekly_hedge(
            hedge_buy_quantity_in_lots or quantity_in_lots,
            call_offset=hedge_call_offset,
            put_offset=hedge_put_offset,
            notification_url=discord_webhook_url,
            strategy_tag=strategy_tags[1],
        )

    # Call the data appender function
    save_strategy_data(
        index=nifty,
        strategy_tag=strategy_tags[0],
        user=user,
        notification_url=discord_webhook_url,
        default_structure=list,
    )

    save_strategy_data(
        index=nifty,
        strategy_tag=strategy_tags[1],
        user=user,
        notification_url=discord_webhook_url,
        default_structure=list,
    )


def biweekly_vs_weekly_straddle(
    quantity_in_lots,
    indices,
    strike_offset=1.003,
    hedge_buy_quantity_in_lots=None,
    hedge_call_offset=1,
    hedge_put_offset=0.98,
    client=None,
    user=None,
    pin=None,
    apikey=None,
    authkey=None,
    webhook_url=None,
    strategy_tags=None,
):
    user, pin, apikey, authkey, discord_webhook_url = initialize_client_and_login(
        client, user, pin, apikey, authkey, webhook_url
    )

    if strategy_tags is None:
        strategy_tags = ["Biweekly hedge", "Biweekly straddle"]

    for index in indices:
        index = vs.Index(index)

        # Checking if it is the time to trade it or not (expiry day)
        if vs.time_to_expiry(index.current_expiry, in_days=True) < 1:
            # Buying weekly hedge
            index.buy_weekly_hedge(
                hedge_buy_quantity_in_lots or quantity_in_lots,
                call_offset=hedge_call_offset,
                put_offset=hedge_put_offset,
                notification_url=discord_webhook_url,
                strategy_tag=strategy_tags[0],
            )

            # Rolling over biweekly straddle (This function will square up any existing positions)
            index.biweekly_straddle(
                quantity_in_lots,
                strike_offset=strike_offset,
                notification_url=discord_webhook_url,
                strategy_tag=strategy_tags[1],
            )

            # Call the data appender function
            save_strategy_data(
                index=index,
                strategy_tag=strategy_tags[0],
                user=user,
                notification_url=discord_webhook_url,
                default_structure=list,
            )

            save_strategy_data(
                index=index,
                strategy_tag=strategy_tags[1],
                user=user,
                notification_url=discord_webhook_url,
                default_structure=list,
            )

        else:
            vs.notifier(
                f"Not trading {index.name} biweekly straddle as it is not expiry day.",
                discord_webhook_url,
            )


def check_eligibility_for_overnight_straddle(
    index: vs.Index,
    index_price: float,
    compare_iv: float,
    compare_vix: float,
    up_weight: float,
) -> tuple[vs.Straddle, float] | tuple[None, None]:
    # Expiry information
    time_to_expiry = vs.time_to_expiry(
        index.current_expiry, in_days=True, effective_time=True
    )

    # Returning None if the time to expiry if square off will be on expiry
    if time_to_expiry < 1.7:
        return None, None

    # Calculating the implied one-day movement from the adjusted vix
    atm_iv = index.fetch_atm_info()["avg_iv"]
    iv_multiple = atm_iv / compare_iv
    target_vix = compare_vix * iv_multiple
    target_vix = target_vix / 100 if target_vix > 2 else target_vix
    implied_movement_one_day = (
        target_vix / 24
    )  # 24 is implied daily factor based on previous study

    vs.logger.debug(
        f"Implied movement for {index.name} is {implied_movement_one_day} "
        f"based on atm iv {atm_iv}, benchmark vix {compare_vix} and benchmark iv {compare_iv}"
    )

    # Checking if the square off is going to be after a holiday
    tomorrow = (vs.currenttime() + vs.timedelta(days=1)).date()
    square_off_after_holiday_or_weekend = (
        tomorrow in vs.holidays or tomorrow.weekday() in [5, 6]
    )

    # Simulating the straddle price
    potential_strike = vs.findstrike(index_price, index.base)
    potential_straddles = index.get_range_of_strangles(
        potential_strike, potential_strike, 4
    )

    potential_profits = []

    for potential_straddle in potential_straddles:
        vs.logger.debug("-" * 50)

        vs.logger.debug(
            f"Simulating price for {potential_straddle} for {index.name} with "
            f"movement {implied_movement_one_day}, time delta {1 / 365} "
            f"and effective iv {square_off_after_holiday_or_weekend}"
        )

        # Calculating the potential profit points
        current_price_of_potential_straddle = potential_straddle.fetch_total_ltp()
        avg_simulated_price = potential_straddle.simulate_price_both_directions(
            atm_iv=0.2,
            movement=implied_movement_one_day,
            time_delta=1 / 365,
            effective_iv=square_off_after_holiday_or_weekend,
            return_total=True,
            up_weightage=up_weight,
            original_spot=index_price,
        )
        potential_profit_points = (
            current_price_of_potential_straddle - avg_simulated_price
        )

        vs.logger.debug(
            f"Potential profit points {potential_profit_points} "
            f"based on current price {current_price_of_potential_straddle} and "
            f"avg simulated price {avg_simulated_price}"
        )

        potential_profits.append(potential_profit_points)

    eligible_straddle = potential_straddles[
        potential_profits.index(max(potential_profits))
    ]
    vs.logger.debug(
        f"Eligible straddle for {index.name} is {eligible_straddle} "
        f"with potential profit points {max(potential_profits)}"
    )
    return eligible_straddle, max(potential_profits)


def overnight_straddles(
    client: str = None,
    user: str = None,
    pin: str = None,
    apikey: str = None,
    authkey: str = None,
    webhook_url: str = None,
    up_weightage: float = 0.55,
):
    """For now just supports Nifty and Banknifty"""

    def return_existing_position(
        existing_positions: dict, index: vs.Index
    ) -> tuple[vs.Straddle, int] | tuple[None, None]:
        index_existing_position = existing_positions.get(index.name, {})
        index_strike, index_quantity = index_existing_position.get(
            "strike"
        ), index_existing_position.get("quantity")
        if index_strike is None:
            return None, None
        else:
            return (
                vs.Straddle(
                    index_strike,
                    index.name,
                    index.current_expiry,
                ),
                index_quantity,
            )

    def handle_index_rollover(
        existing_positions: dict,
        index: vs.Index,
        index_avg_price: float,
        compare_iv: float,
        compare_vix: float,
        sell_qty: int,
    ):
        index_buy_straddle, index_buy_quantity = return_existing_position(
            existing_positions, index
        )
        index_sell_straddle, _ = check_eligibility_for_overnight_straddle(
            index, index_avg_price, compare_iv, compare_vix, up_weightage
        )

        if index_buy_straddle is None and index_sell_straddle is None:
            vs.notifier(
                f"No trade for {index.name} as no new or existing position to be opened.",
                discord_webhook_url,
            )

        elif index_sell_straddle is None:
            vs.notifier(
                f"No new position to be opened for {index.name}. "
                f"Only squaring off existing position {index_buy_straddle}",
                discord_webhook_url,
            )
            call_buy_avg, put_buy_avg = vs.place_option_order_and_notify(
                index_buy_straddle,
                "BUY",
                index_buy_quantity,
                "LIMIT",
                order_tag=order_tag,
                webhook_url=discord_webhook_url,
                return_avg_price=True,
            )

        elif index_buy_straddle is None:
            vs.notifier(
                f"No existing position for {index.name}. "
                f"Only opening new position {index_sell_straddle}",
                discord_webhook_url,
            )
            call_sell_avg, put_sell_avg = vs.place_option_order_and_notify(
                index_sell_straddle,
                "SELL",
                sell_qty,
                "LIMIT",
                order_tag=order_tag,
                webhook_url=discord_webhook_url,
                return_avg_price=True,
            )

        else:
            if index_buy_straddle == index_sell_straddle:
                vs.notifier(
                    f"Existing position for {index.name} is same as the new position {index_sell_straddle}. "
                    f"No trade required.",
                    discord_webhook_url,
                )
                call_ltp, put_ltp = index_sell_straddle.fetch_ltp()
                call_buy_avg, put_buy_avg, call_sell_avg, put_sell_avg = (
                    call_ltp,
                    put_ltp,
                    call_ltp,
                    put_ltp,
                )

    order_tag = "Overnight short straddle"

    # Getting user data and logging in
    user, pin, apikey, authkey, discord_webhook_url = initialize_client_and_login(
        client, user, pin, apikey, authkey, webhook_url
    )

    # Initializing indices
    nifty = vs.Index("NIFTY")
    bnf = vs.Index("BANKNIFTY")

    """
    # Loading existing positions
    existing_position_dict = vs.load_json_data(
        "overnight_straddle_positions.json",
        user,
        dict,
        discord_webhook_url,
    )
    """

    # Calculating avg price
    nifty_atm_info = nifty.fetch_atm_info()
    bnf_ltp = bnf.fetch_ltp()
    nifty_ltp = nifty_atm_info["underlying_price"]

    benchmark_vix = vs.get_current_vix()
    benchmark_vix = benchmark_vix / 100
    benchmark_iv = nifty_atm_info["avg_iv"]

    for index, index_ltp in zip([nifty, bnf], [nifty_ltp, bnf_ltp]):
        eligible_straddle, profit_points = check_eligibility_for_overnight_straddle(
            index, index_ltp, benchmark_iv, benchmark_vix, up_weightage
        )

        vs.notifier(
            f"Eligible straddle for {index.name} is {eligible_straddle} with profit points {profit_points}",
            discord_webhook_url,
        )


def index_vs_constituents(
    index_symbol,
    strike_offset=0,
    index_strike_offset=None,
    cutoff_pct=90,
    exposure_per_stock=10000000,
    expirys=None,
    ignore_last=0,
):
    index_strike_offset = (
        strike_offset if index_strike_offset is None else index_strike_offset
    )
    expirys = ("future", "current") if expirys is None else expirys

    # Fetch constituents
    constituent_tickers, constituent_weights = vs.get_index_constituents(
        index_symbol, cutoff_pct
    )
    total_weight, number_of_stocks = sum(constituent_weights), len(constituent_tickers)
    percent_weights = [weight / total_weight for weight in constituent_weights]
    total_exposure = exposure_per_stock * number_of_stocks

    # Fetch index info
    index = vs.Index(index_symbol)
    index_info = index.fetch_otm_info(index_strike_offset, expiry=expirys[0])
    index_iv, index_shares = (
        index_info["avg_iv"],
        int(total_exposure / (index.fetch_ltp() * index.lot_size)) * index.lot_size,
    )
    index_premium_value = index_info["total_price"] * index_shares
    index_break_even_points = (
        index_info["underlying_price"],
        index_info["call_strike"],
        index_info["put_strike"],
    )
    index_break_even_points += (
        index_info["call_strike"] + index_info["total_price"],
        index_info["put_strike"] - index_info["total_price"],
    )

    # Calculate movements to break even
    def _return_abs_movement(current_price, threshold_price):
        return abs((threshold_price / current_price - 1)) * 100

    index_break_even_points += tuple(
        _return_abs_movement(index_info["underlying_price"], bep)
        for bep in index_break_even_points[1:3]
    )
    index_call_break_even, index_put_break_even = index_break_even_points[-2:]

    # Fetch constituent info
    constituents = list(map(vs.Stock, constituent_tickers))
    constituent_infos = [
        stock.fetch_otm_info(strike_offset, expiry=expirys[1]) for stock in constituents
    ]
    constituent_ivs = [info["avg_iv"] for info in constituent_infos]
    constituent_ivs_weighted_avg = sum(
        iv * pw for iv, pw in zip(constituent_ivs, percent_weights)
    )
    weighted_exposures = [total_exposure * pw for pw in percent_weights]
    shares_per_stock = [
        int(exposure / (stock.fetch_ltp() * stock.lot_size)) * stock.lot_size
        for exposure, stock in zip(weighted_exposures, constituents)
    ]
    premium_per_stock = [info["total_price"] for info in constituent_infos]
    premium_values_per_stock = [
        premium * shares for premium, shares in zip(premium_per_stock, shares_per_stock)
    ]
    premium_difference = sum(premium_values_per_stock) - index_premium_value
    break_even_points_per_stock = [
        (
            info["underlying_price"],
            info["call_strike"],
            info["put_strike"],
            info["call_strike"] + premium,
            info["put_strike"] - premium,
        )
        for info, premium in zip(constituent_infos, premium_per_stock)
    ]
    break_even_points_per_stock = [
        (
            bep[0],
            bep[1],
            bep[2],
            bep[3],
            bep[4],
            _return_abs_movement(info["underlying_price"], bep[1]),
            _return_abs_movement(info["underlying_price"], bep[2]),
        )
        for bep, info in zip(break_even_points_per_stock, constituent_infos)
    ]

    # Average break evens
    break_evens_weighted_avg = [
        sum(
            bep[i] * pw for bep, pw in zip(break_even_points_per_stock, percent_weights)
        )
        for i in [3, 4]
    ]

    # Analyzing recent realized volatility
    recent_vols = dm.get_multiple_recent_vol(
        [index_symbol] + constituent_tickers,
        frequency="M-THU",
        periods=[2, 5, 7, 10, 15, 20],
        ignore_last=ignore_last,
    )
    period_vol_dict = {
        f"Last {period} period avg": {
            "index": recent_vols[index_symbol][period][0],
            "constituents_vols_weighted_avg": sum(
                ticker[period][0] * pw
                for ticker, pw in zip(list(recent_vols.values())[1:], percent_weights)
            ),
        }
        for period in recent_vols[index_symbol]
    }

    # Return the data
    return {
        "index_iv": index_iv,
        "constituents_iv_weighted": constituent_ivs_weighted_avg,
        "constituents_iv_unweighted": sum(constituent_ivs) / number_of_stocks,
        "index_shares": index_shares,
        "index_premium_value": index_premium_value,
        "constituent_tickers": constituent_tickers,
        "constituent_weights": constituent_weights,
        "shares_per_stock": shares_per_stock,
        "premium_values_per_stock": premium_values_per_stock,
        "total_constituents_premium_value": sum(premium_values_per_stock),
        "premium_value_difference": premium_difference,
        "total_exposure": total_exposure,
        "profit_percentage": premium_difference / total_exposure * 100,
        "index_trade_info": index_break_even_points,
        "constituent_trade_infos": break_even_points_per_stock,
        "index_call_break_even": index_call_break_even,
        "index_put_break_even": index_put_break_even,
        "call_side_break_evens_wtd_avg": break_evens_weighted_avg[0],
        "put_side_break_evens_wtd_avg": break_evens_weighted_avg[1],
        "recent_vols": period_vol_dict,
    }
