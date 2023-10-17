#!/opt/thefactory_venv/bin/python
import random
import socket
import time
from collections import ChainMap
from datetime import timedelta, datetime

import httplib2.error
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mysql.connector.errors import ProgrammingError as MysProgrammingError
from oauth2client.client import HttpAccessTokenRefreshError
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError as AlcProgrammingError

import thefactory.config as config

""" Holds the setup for google analytics
NB v4 for GA, for rt must use v3"""
__version__ = "3.0.4"

scope = "https://www.googleapis.com/auth/analytics.readonly"


def get_rept_data(svc, build_r, log):
    for n in range(0, 5):
        try:
            return svc.reports().batchGet(body=build_r).execute()

        except (socket.gaierror, httplib2.error.ServerNotFoundError, HttpError, HttpAccessTokenRefreshError) as err:
            if err.resp.reason in ['userRateLimitExceeded', 'quotaExceeded',
                                   'internalServerError', 'backendError']:
                time.sleep((2 ** n) + random.random())
                log.warning("Quota exceeded, backing off")
            else:
                break
        except Exception as e:
            log.warning(f'Error waiting for report build {e.args}, {str(e)}, possible timeout')
            break
    log.warning("Not able to retrieve GA due to probably, quota limits")
    return False


def get_realtime_data(svc, ga_kwargs, log):
    for n in range(0, 5):
        try:
            return svc.data().realtime().get(**ga_kwargs).execute()
        except (socket.gaierror, httplib2.error.ServerNotFoundError, HttpError) as err:
            if err.resp.reason in ['userRateLimitExceeded', 'quotaExceeded',
                                   'internalServerError', 'backendError']:
                time.sleep((2 ** n) + random.random())
                log.warning("Quota exceeded, backing off")
            else:
                break
    log.warning("Not able to retrieve GA due to probably, quota limits")
    return False


def process_daily_recs(svc, build_r, a_r, log, dbp, col_names, col_types, table):
    log.info(f"{a_r} records to table")
    if a_r == "replace":
        try:
            dbp.engine.execute(f"TRUNCATE {table}")
        except (MysProgrammingError, AlcProgrammingError) as e:
            log.info(f'Table {table} does not yet exist')
        a_r = 'append'

    init_run = True
    npt = False
    this_date = build_r['reportRequests'][0]['dateRanges']
    log.info(f'Processing records for {this_date}')
    while npt or init_run:
        # If it's our first run we've already got data
        # If it's not our first run, we need to get data
        # If npt is True, we have a next page token and need to do the next page
        if not init_run:
            if npt:
                build_r["reportRequests"][0]["pageToken"] = npt

        init_run = False
        n = 1
        dta = get_rept_data(svc, build_r, log)
        if not dta:
            break
        try:
            npt = dta["reports"][0]["nextPageToken"]
            log.info(f'We have a next page token, {npt}')
        except (KeyError, NameError):
            npt = False
            log.info('We do not have a next page token')

        for report in dta.get("reports", []):
            log.info(f"Inserting data for {this_date}")
            row_dat = [row["dimensions"] + row["metrics"][0]["values"] for row in
                       report.get("data", {}).get("rows", [])]
            do_data(
                data=row_dat,
                cols=col_names,
                types=col_types,
                dbp=dbp,
                table=table,
                app_rep=a_r,
                logger=log,
            )
            a_r = "append"
    return a_r


def do_data(data, cols, types, logger, dbp, table, app_rep):
    df = pd.DataFrame(data, columns=cols)
    for k, v in types.items():
        if v == "dateTime":
            df[k] = pd.to_datetime(df[k])
        elif v == "integer":
            df[k] = pd.to_numeric(df[k], downcast="signed")
        elif v == "float":
            df[k] = pd.to_numeric(df[k], downcast="float")
    logger.info(f"Inserting {len(df.index)} records into table")
    df.to_sql(con=dbp, name=table, if_exists="append", index=False)


def get_service(p_id, version=3):
    db = config.DBaseLive()
    sql = f"""SELECT key_file_location
FROM google_analytics.profiles
WHERE id = %(p_id)s"""
    db.curs.execute(sql, {"p_id": p_id})
    key_file_location = db.curs.fetchone()[0]
    db.conn.close()
    if version == 4:
        api_name = "analyticsreporting"
        api_version = "v4"
    else:
        api_name = "analytics"
        api_version = "v3"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scope
    )
    service = build(
        api_name, api_version, credentials=credentials, cache_discovery=False
    )
    return service


def run_ga_stats(db_name, table, fld_list, id, filt, countries, r_a, sd, ed, logger):
    """db_name = database. table = table, fld_list = dict of fields and types, id = ga_id, dim = dimensions list,
    met = metrics list, filt = filter list, countries = countries, r_a = Real/gA, sd = start_date, ed = end_date
    """
    if sd == "today":
        sd = datetime.today()
    elif sd == "yesterday":
        sd = datetime.today() - timedelta(days=1)
    else:
        sd = datetime.strptime(sd, "%Y-%m-%d")
    if ed == "today":
        # Return tomorrow's date
        ed = datetime.today() + timedelta(days=1)
    elif ed == "yesterday":
        # Also return tomorrow's date
        ed = datetime.today() + timedelta(days=1)
    else:
        # Returns a day one day more than ed
        ed = datetime.strptime(ed, "%Y-%m-%d") + timedelta(days=1)
    # Create a range with datetimes
    delta = ed - sd
    dt_ranges = [sd + timedelta(days=x) for x in range(delta.days)]
    app_rep = "replace"
    max_recs = 10000
    dbp = create_engine(config.create_sql_eng(db_name))
    q_pref = "ga:"
    col_names = [d["name"] for d in fld_list]
    filt_arg = ""
    col_types = dict(ChainMap(*[{g["name"]: g["format"]} for g in fld_list]))
    if countries:
        filt_arg = f"{q_pref}country=={f',{q_pref}country=='.join(countries)}"
    if filt:
        if countries:
            filt_arg = f"{filt_arg};{';'.join(filt)}"
        else:
            filt_arg = ";".join(filt)

    met = [{"expression": "ga:" + d["name"]} for d in fld_list if d["type"] == "metric"]
    dim = [{"name": q_pref + d["name"]} for d in fld_list if d["type"] == "dimension"]
    service = get_service(version=4, p_id=id)
    logger.info(f"Processing dates {sd} to {ed}")
    for dt in dt_ranges:
        tsd = dt.strftime("%Y-%m-%d")
        dr = [{"startDate": tsd, "endDate": tsd}]
        build_req = {
            "reportRequests": [
                {
                    "viewId": id,
                    "dateRanges": dr,
                    "metrics": met,
                    "dimensions": dim,
                    "filtersExpression": filt_arg,
                    "pageSize": max_recs,
                    "samplingLevel": "LARGE",
                }
            ]
        }
        n = 1
        app_rep = process_daily_recs(service, build_req, app_rep, logger, dbp, col_names, col_types, table, )


def run_rt_stats(db_name, table, fld_list, id, filt, countries, logger):
    logger.info(f"Running rt stats for {id = }")
    app_rep = "append"
    max_recs = 10000
    engine = create_engine(config.create_sql_eng(db_name))
    try:
        engine.execute(f"TRUNCATE {table}")
    except (MysProgrammingError, AlcProgrammingError) as e:
        logger.info(f'Table {table} does not yet exist')
    a_r = 'append'
    col_names = [d["name"] for d in fld_list]
    q_pref = "rt:"
    col_types = dict(ChainMap(*[{g["name"]: g["format"]} for g in fld_list]))
    filt_arg = ""
    if countries:
        filt_arg = f"{q_pref}country=={f',{q_pref}country=='.join(countries)}"
    if filt:
        if countries:
            filt_arg = f"{filt_arg};{';'.join(filt)}"
        else:
            filt_arg = ";".join(filt)
    version = 3
    num_rec = 1
    ids = f"ga:{id}"
    dim = ",".join([q_pref + d["name"] for d in fld_list if d["type"] == "dimension"])
    met = ",".join([q_pref + d["name"] for d in fld_list if d["type"] == "metric"])
    service = get_service(version=version, p_id=id)
    ga_kwargs = dict(ids=ids, dimensions=dim, metrics=met, filters=filt_arg)
    mydat = get_realtime_data(service, ga_kwargs, logger)
    if mydat:
        tot_recs = mydat.get("totalResults")
        while num_rec <= tot_recs:
            if num_rec != 1:
                ga_kwargs["start_index"] = num_rec
                mydat = service.data().ga().get(**ga_kwargs).execute()
            logger.info(
                f"Getting records {num_rec} to {min(num_rec + 999, tot_recs)} of total of {tot_recs} records"
            )
            row_dat = mydat.get("rows")
            do_data(
                data=row_dat,
                cols=col_names,
                types=col_types,
                logger=logger,
                dbp=engine,
                table=table,
                app_rep=app_rep,
            )
            num_rec += max_recs
