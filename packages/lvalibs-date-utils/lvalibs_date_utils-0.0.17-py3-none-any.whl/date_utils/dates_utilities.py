from datetime import date, datetime
import dateutil.relativedelta
import pandas as pd
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)


def days_between_dates(from_date: date, to_date: date) -> Optional[int]:

    """Calculate the number of days between two dates, regardless of which is the greater.
    If any parameter is datetime, this functions change to date automatically
    Parameters:
        from_date:date - initial date consider in calculation
        to_date:date - final date consider in calculation
    return:
        :int days between date. None on Error
    """

    # check None for dates
    if from_date is None or to_date is None:
        return None

    f_date = from_date
    t_date = to_date

    # check date type
    if type(f_date) == datetime:
        f_date = f_date.date()
    if type(t_date) == datetime:
        t_date = t_date.date()

    # if from_date is greather than to_date, the calculation order is reversed
    if f_date > t_date:
        f_date = to_date
        t_date = from_date

    try:
        delta = t_date - f_date
    except Exception as e:
        logger.exception(e)
        return None
    else:
        return delta.days


def first_day_of_month(current_date: date) -> Optional[datetime.date]:
    """Calculate the first day of current_date.
    If any parameter is datetime, this functions change to date automatically
    Parameters:
        current_date:date - any day of month
    return:
        :date fisrt day of month. None on Error
    """

    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        return c_date.replace(day=1)
    except Exception as e:
        logger.exception(e)
        return None


def last_day_of_month(current_date: date) -> Optional[datetime.date]:
    """Calculate the last day of current_date.
    If any parameter is datetime, this functions change to date automatically
    Parameters:
        current_date:date - any day of month
    return:
        :date last day of month. None on Error
    """
    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        return (
            first_day_of_month(c_date)
            + dateutil.relativedelta.relativedelta(months=1)
            - dateutil.relativedelta.relativedelta(days=1)
        )
    except Exception as e:
        logger.exception(e)
        return None


def last_day_from_months_delta(current_date: date, months_delta: int) -> Optional[datetime.date]:
    """Calculate the last day of month considering current_date + months_delta.
    If any parameter is datetime, this functions change to date automatically.
    Exs:
        last_day_from_months_delta(current_date=date(2022,4,1),months_delta=-3) --> date(2022,1,31)
        last_day_from_months_delta(current_date=date(2022,4,1),months_delta=3) --> date(2022,7,31)
    Parameters:
        current_date:date - any day of month
        months_delta:int - months delta to consindering in calculation, this value could be positive or negative
    return:
        :date last day of month. None on Error
    """

    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        d = c_date + dateutil.relativedelta.relativedelta(months=months_delta)
        d = last_day_of_month(current_date=d)
        if type(d) == datetime:
            return d.date()
        else:
            return d
    except Exception as e:
        logger.exception(e)
        return None


def first_day_from_months_delta(current_date: date, months_delta: int) -> Optional[datetime.date]:
    """Calculate the first day of month considering current_date + months_delta.
    If any parameter is datetime, this functions change to date automatically.
    Exs:
        first_day_from_months_delta(current_date=date(2022,4,1),months_delta=3) --> date(2022,7,1)
        first_day_from_months_delta(current_date=date(2022,4,1),months_delta=-3) --> date(2022,1,1)
    Parameters:
        current_date:date - any day of month
        months_delta:int - months delta to consindering in calculation, this value could be positive or negative
    return:
        :date first day of month. None on Error
    """
    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()
    try:
        d = c_date + dateutil.relativedelta.relativedelta(months=months_delta)
        d = first_day_of_month(current_date=d)
        return d
    except Exception as e:
        logger.exception(e)
        return None


def last_day_from_years_delta(current_date: date, years_delta: int) -> Optional[datetime.date]:
    """Calculate the last day year of current_date + years_delta .
    If any parameter is datetime, this functions change to date automatically.
    Exs:
        last_day_from_years_delta(current_date=date(2022,4,1),years_delta=3) --> date(2025,12,31)
        last_day_from_years_delta(current_date=date(2022,4,1),years_delta=-3) --> date(2019,12,31)
    Parameters:
        current_date:date - any day of month
        years_delta:int - months delta to consindering in calculation, this value could be positive or negative
    return:
        :date last day of previous year (December 31). None on Error
    """
    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        d = c_date + dateutil.relativedelta.relativedelta(years=years_delta)
        return date(d.year, 12, 31)
    except Exception as e:
        logger.exception(e)
        return None


def first_day_from_years_delta(current_date: date, years_delta: int) -> Optional[datetime.date]:
    """Calculate the first day year of current_date + years_delta .
    If any parameter is datetime, this functions change to date automatically.
    Exs:
        first_day_from_years_delta(current_date=date(2022,4,1),years_delta=3) --> date(2025,1,1)
        first_day_from_years_delta(current_date=date(2022,4,1),years_delta=-3) --> date(2019,1,1)
    Parameters:
        current_date:date - any day of month
        years_delta:int - months delta to consindering in calculation, this value could be positive or negative
    return:
        :date first day of current year (January 1). None on Error
    """
    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        d = c_date + dateutil.relativedelta.relativedelta(years=years_delta)
        return date(d.year, 1, 1)
    except Exception as e:
        logger.exception(e)
        return None


def generate_dates_for_current_month(current_date: date) -> Optional[list[date]]:
    """Generate list of dates of current_month of current_date.
    If any parameter is datetime, this functions change to date automatically.
    Parameters:
        current_date:date - any day of month
    return:
        :list[date] list of dates for current month. None on Error
    """
    if current_date is None:
        return None

    c_date = current_date

    # check date type
    if type(c_date) == datetime:
        c_date = c_date.date()

    try:
        first_day_m = first_day_of_month(current_date=c_date)
        last_day_m = last_day_of_month(current_date=c_date)
        list_days = [d.date() for d in pd.date_range(first_day_m, last_day_m, freq="D")]
        return list_days
    except Exception as e:
        logger.exception(e)
        return None
