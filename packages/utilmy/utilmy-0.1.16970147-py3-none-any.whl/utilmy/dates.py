# -*- coding: utf-8 -*-
"""  dates utilities
Doc::
"""
import os, sys, time, datetime,inspect, json, yaml, gc, numpy as np, pandas as pd
from typing import Union
#############################################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help        
    """
    from utilmy import help_create
    print(  help_create(__file__) )


####################################################################################################
def test_all():
    """function test_all        
    """
    test1()
    test2()


def test1():    
    log("Testing dates.py ...")

    df = pd.DataFrame(columns=['Birthdate'])
    df['Birthdate'] = pd_random_daterange(start=pd.to_datetime('2000-01-01'), end=pd.to_datetime('2022-01-01'), size=10)
    print(df)
    assert not df.empty, 'FAILED, generate df data'


    df2 = pd_date_split(df, coldate='Birthdate', sep='-')
    print(df2)
    assert not df2.empty, 'FAILED, pd_date_split'

    import datetime
    res =  date_to_timezone(datetime.datetime.now())
    print(res)
    assert res, 'FAILED, date_to_timezone'

    res = date_is_holiday([pd.to_datetime('2000-01-01')])
    print(res)
    assert res, 'FAILED, date_is_holiday'

    res = date_weekmonth2(datetime.datetime.now())
    print(res)
    assert res, 'FAILED, date_weekmonth2'

    # date_weekyear2
    res = date_weekyear2(datetime.datetime.now())
    print(res)
    assert res, 'FAILED, date_weekyear2'

    # date_weekday_excel
    res = date_weekday_excel("20220223")
    print(res)
    assert res, 'FAILED, date_weekday_excel'

    # date_weekyear_excel
    res = date_weekyear_excel("20220223")
    print(res)
    assert res, 'FAILED, date_weekyear_excel'


    date_ = date_generate(start='2021-01-01', ndays=100)
    print(date_)
    assert date_, 'FAILED, date_generate'

    date_weekyear_excel('20210317')
    date_weekday_excel('20210317')


def test2():
    # test date_now()
    res = date_now()
    log(res)
    assert res, 'FAILED, date_now'

    # test date_now with add more days
    res = date_now(add_days=5, timezone='Asia/Tokyo')
    log(res)
    assert res, 'FAILED, date_now'

    # test date_now with new format
    res = date_now(fmt="%d/%m/%Y", add_days=12)
    log(res)
    assert res, 'FAILED, date_now'

    assert date_now(timezone='Asia/Tokyo')    #-->  "20200519"   ## Today date in YYYMMDD
    assert date_now(timezone='Asia/Tokyo', fmt='%Y-%m-%d')    #-->  "2020-05-19"

    res = date_now('2020-12-10', fmt='%Y%m%d', add_days=-5, returnval='int')
    log(res )
    assert res == 20201205, 'FAILED, date_now'

    res = date_now(20211005, fmt='%Y-%m-%d', fmt_input='%Y%m%d', returnval='str')  #-->  '2021-10-05'
    log(res )
    assert res == '2021-10-05', 'FAILED, date_now'




def pd_random_daterange(start, end, size):
    """pd_random_daterange is used to get random dates between start and end date.

    Docs::

        Args:
            Start (pd.to_datetime):   Starting date
            End (pd.to_datetime):     Ending date
            Size (int):    Number of random dates we want to generate.
        Returns: Return the "n" random dates between start and end dates
        Example: from utilmy.dates import pd_random_daterange
                 df = pd.DataFrame(columns=['Birthdate'])
                 df['Birthdate'] = pd_random_daterange(start=pd.to_datetime('2000-01-01'), end=pd.to_datetime('2022-01-01'), size=3)
                 print(df)

                 Output:        Birthdate
                             0 2010-08-12
                             1 2009-05-22
                             2 2021-09-22


    """
    divide_by = 24 * 60 * 60 * 10**9
    print(".value", start.value)
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")



####################################################################################################
##### Utilities for date  ##########################################################################
def test_datenow():
    import utilmy as m, time

    log("\n####", m.date_now)
    assert m.date_now(timezone='Asia/Tokyo')    #-->  "20200519"   ## Today date in YYYMMDD
    assert m.date_now(timezone='Asia/Tokyo', fmt='%Y-%m-%d')    #-->  "2020-05-19"

    x = m.date_now('2020-12-10', fmt='%Y%m%d', add_days=-5, returnval='int')
    assert not log( x ) and x == 20201205, x   #-->  20201205

    x = m.date_now(20211005,     fmt_input='%Y%m%d', returnval='unix')
    assert   not log(x ) and  int(x)  > 1603424400, x  #-->  1634324632848

    x = m.date_now(20211005,     fmt='%Y-%m-%d', fmt_input='%Y%m%d', returnval='str')  #-->  '2021-10-05'
    assert   not log(x ) and  x  == '2021-10-05' , x                                   #-->  1634324632848

    
    assert date_now('2020-05-09', add_months=-2, fmt='%Y-%m-%d') == "2020-03-09" #Test adding -2 months
    assert date_now('2012-12-06 12:00:00',returnval='datetime',add_mins=20,fmt_input="%Y-%m-%d %H:%M:%S") == date_now('2012-12-06 12:20:00',returnval='datetime',fmt_input="%Y-%m-%d %H:%M:%S") #Test adding 20 minutes
    assert date_now('2012-12-06 12:00:00',returnval='datetime',add_hours=11,fmt_input="%Y-%m-%d %H:%M:%S") == date_now('2012-12-06 23:00:00',returnval='datetime',fmt_input="%Y-%m-%d %H:%M:%S") #Test adding 11 hours
    assert date_now('2012-12-06 12:00:00',returnval='datetime',add_days=5,fmt_input="%Y-%m-%d %H:%M:%S") == date_now('2012-12-11 12:00:00',returnval='datetime',fmt_input="%Y-%m-%d %H:%M:%S") #Test adding 5 days
    # assert date_now('2012-12-06 19:00:00',returnval='datetime',force_dayofweek=0,fmt_input="%Y-%m-%d %H:%M:%S") == date_now('2012-12-03 19:00:00',returnval='datetime',fmt_input="%Y-%m-%d %H:%M:%S") #Test forcing day 3 of the week

    x = date_now( time.time(), returnval='datetime')
    x = date_now( time.time(), returnval='datetime', timezone='utc')
    x = date_now( int(time.time()), returnval='datetime')

    log("check unix epoch timezone time.time() ")
    assert abs(int(time.time()) - date_now( int(time.time()), returnval='unix', timezone='utc')) < 1e-2, ""

    ts  = time.time()
    datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    dtu = datetime.datetime.fromtimestamp(ts) #.strftime('%Y-%m-%d %H:%M:%S')
    datetime.datetime.timestamp(dtu )  

    log("Testing the argument timezone_input")
    # Testing adding minutes, hours, and months
    assert date_now(datenow='2023-02-16 21:56:00',returnval="unix",timezone_input="America/Santiago",timezone="Europe/Paris",add_mins = 52,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 01:56:00',returnval="unix",timezone="Europe/Paris",add_mins = 52,fmt_input="%Y-%m-%d %H:%M:%S")
    assert date_now(datenow='2023-02-16 21:56:00',returnval="unix",timezone_input="America/Santiago",timezone="Europe/Paris",add_hours = 2,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 01:56:00',returnval="unix",timezone="Europe/Paris",add_hours = 2,fmt_input="%Y-%m-%d %H:%M:%S")
    assert date_now(datenow='2023-02-16 21:56:00',returnval="unix",timezone_input="America/Santiago",timezone="Europe/Paris",add_months=10,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 01:56:00',returnval="unix",timezone="Europe/Paris",add_months=10,fmt_input="%Y-%m-%d %H:%M:%S")
    
    log("Testing the argument datenow with a datetime object as value")
    datetime_obj = datetime.datetime(2023,2,16,21,56,0,0)
    assert date_now(datenow = datetime_obj,timezone="Europe/Paris", returnval = "datetime", fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-16 21:56:00',returnval="datetime",timezone="Europe/Paris",fmt_input="%Y-%m-%d %H:%M:%S")
    
    log("Testing the argument datenow with a timestamp value and with different timezone")
    random_timestamp = 1621583040
    assert abs(random_timestamp - date_now(random_timestamp, returnval='unix',timezone_input="UTC", timezone="Europe/Paris")) < 1e-2, ""

    assert date_now(datenow='2023-02-16 23:56:00',returnval="unix",timezone_input="Europe/Paris",timezone="Asia/Tokyo",add_mins = 52,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 07:56:00',returnval="unix",timezone="Asia/Tokyo",add_mins = 52,fmt_input="%Y-%m-%d %H:%M:%S")
    assert date_now(datenow='2023-02-16 23:56:00',returnval="unix",timezone_input="Europe/Paris",timezone="Asia/Tokyo",add_hours= 17,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 07:56:00',returnval="unix",timezone="Asia/Tokyo",add_hours =17,fmt_input="%Y-%m-%d %H:%M:%S")
    assert date_now(datenow='2023-02-16 23:56:00',returnval="unix",timezone_input="Europe/Paris",timezone="Asia/Tokyo",add_months=10,fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-17 07:56:00',returnval="unix",timezone="Asia/Tokyo",add_months=10,fmt_input="%Y-%m-%d %H:%M:%S")
    
    log("Testing with double conversion")
    #Testing first the return values unix and datetime, because, return value int needs another format
    for first_rval in ["unix","datetime"]:
        first_conv = date_now(datenow='2023-02-16 21:56:00',returnval=first_rval,timezone_input="Asia/Tokyo",timezone="America/Santiago",fmt="%Y-%m-%d %H:%M:%S",fmt_input="%Y-%m-%d %H:%M:%S")
        for second_rval in ["unix","datetime","int"]:
            assert date_now(first_conv, returnval=second_rval,timezone_input="America/Santiago",timezone="Asia/Tokyo",fmt_input="%Y-%m-%d %H:%M:%S") == date_now(datenow='2023-02-16 21:56:00',returnval=second_rval,timezone="Asia/Tokyo",fmt_input="%Y-%m-%d %H:%M:%S")
    
    # Testing the return value int with its correct format
    first_conv = date_now(datenow='2023-02-16 21:56:00',returnval="int",timezone_input="Asia/Tokyo",timezone="America/Santiago",fmt_input="%Y-%m-%d %H:%M:%S", fmt ="%Y%m%d%H%M%S")
    for rval in ["unix", "datetime", "int"]:
        assert date_now(str(first_conv), returnval=rval,timezone_input="America/Santiago",timezone="Asia/Tokyo",fmt_input="%Y%m%d%H%M%S") == date_now(datenow='2023-02-16 21:56:00',returnval=rval,timezone_input="Asia/Tokyo",timezone="Asia/Tokyo",fmt_input="%Y-%m-%d %H:%M:%S")


def test_date_now_range():
    # This test tests the function date_now_range
    from pytz import timezone as tzone

    log("Testing date_now_range")
    #Testing date_now_range with days
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D')
    assert len(date_list) == 31, "FAILED, date_now_range"
    
    #Testing date_now_range with weeks
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='2W')
    assert len(date_list) == 3, "FAILED, date_now_range"
    
    #Testing date_now_range with months
    date_list = date_now_range(start='20210101', end='20220131',fmt_input="%Y%m%d",freq='1M')
    assert len(date_list) == 13, "FAILED, date_now_range"
    
    #Testing date_now_range with years
    date_list = date_now_range(start='20210101', end='20220131',fmt_input="%Y%m%d",freq='1Y')
    assert len(date_list) == 2, "FAILED, date_now_range"

    #Testing date_now_range with quarters
    date_list = date_now_range(start='20210101', end='20220131',fmt_input="%Y%m%d",freq='1Q')
    assert len(date_list) == 5, "FAILED, date_now_range"

    #Testing date_now_range with random
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='random freq type')
    assert len(date_list) == 31, "FAILED, date_now_range"

    # Testing date_now_range with the parameter timezone
    date_list = date_now_range(start='20210101', end='20210131',timezone_input='Asia/Tokyo',timezone="America/Argentina/Buenos_Aires",fmt_input="%Y%m%d",freq='random freq type')
    assert len(date_list) == 31, "FAILED, date_now_range"

    # Testing date_now_range with the parameter fmt different
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",fmt="%d-%m-%Y",freq='2D')
    assert len(date_list) == 16, "FAILED, date_now_range"

    #Testing date_now_range with the parameter add_days
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D',add_days=1)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-02', "FAILED, date_now_range"

    #Testing date_now_range with the parameter add_months
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D',add_months=1)
    assert len(date_list) == 28, "FAILED, date_now_range"
    assert date_list[0] == '2021-02-01', "FAILED, date_now_range"

    #Testing date_now_range with the parameter add_weeks
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D',add_weeks=1)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-08', "FAILED, date_now_range"

    #Testing date_now_range with the parameter add_mins
    date_list = date_now_range(start='2021-01-01 00:00', end='2021-01-31 00:00',fmt_input="%Y-%m-%d %H:%M",fmt="%Y-%m-%d %H:%M",freq='1D',add_mins=30)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-01 00:30', "FAILED, date_now_range"

    #Testing date_now_range with the parameter add_hours
    date_list = date_now_range(start='2021-01-01 00:00', end='2021-01-31 00:00',fmt_input="%Y-%m-%d %H:%M",fmt="%Y-%m-%d %H:%M",freq='1D',add_hours=2)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-01 02:00', "FAILED, date_now_range"

    #Testing date_now_range with the parameter force_dayofmonth
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D',force_dayofmonth=2)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-02', "FAILED, date_now_range"

    #Testing date_now_range with the parameter force_dayofmonth
    date_list = date_now_range(start='20210101', end='20210331',fmt_input="%Y%m%d",freq='1D',force_dayofmonth=31)
    log(date_list)
    assert len(date_list) == 90, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-31', "FAILED, date_now_range"

    #Testing date_now_range with the parameter force_dayofweek
    date_list = date_now_range(start='20210101', end='20210131',fmt_input="%Y%m%d",freq='1D',force_dayofweek=1)
    assert len(date_list) == 29, "FAILED, date_now_range"
    assert date_list[0] == '2020-12-29', "FAILED, date_now_range"

    #Testing date_now_range with the parameter force_hourofday
    date_list = date_now_range(start='2021-01-01 00:00', end='2021-01-31 00:00',fmt_input="%Y-%m-%d %H:%M",fmt="%Y-%m-%d %H:%M",freq='1D',force_hourofday=5)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-01 05:00', "FAILED, date_now_range"

    #Testing date_now_range with the parameter force_minofhour
    date_list = date_now_range(start='2021-01-01 00:00', end='2021-01-31 00:00',fmt_input="%Y-%m-%d %H:%M",fmt="%Y-%m-%d %H:%M",freq='1D',force_minofhour=35)
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == '2021-01-01 00:35', "FAILED, date_now_range"

    #Testing date_now_range with the parameter returnval to int
    date_list = date_now_range(start='20210101', end='20210131',fmt="%Y%m%d",fmt_input="%Y%m%d",freq='1D',returnval="int")
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == 20210101, "FAILED, date_now_range"

    #Testing date_now_range with the parameter returnval to unix
    date_list = date_now_range(start='20210101', end='20210131',fmt="%Y%m%d",fmt_input="%Y%m%d",freq='1D',returnval="unix")
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert date_list[0] == 1609426800.0, "FAILED, date_now_range"

    #Testing date_now_range with the parameter returnval to datetime
    date_list = date_now_range(start='20210101', end='20210131',fmt="%Y-%m-%d",fmt_input="%Y%m%d",freq='1D',returnval="datetime")
    assert len(date_list) == 31, "FAILED, date_now_range"
    assert str(date_list[0].date()) == "2021-01-01", "FAILED, date_now_range"


def is_date(dt:str):
    """
    Check if input is a date

    Args:

    Returns:
        bool: True if the inpute is a date.
    """
    pass 


def date_now(datenow:Union[str,int,float,datetime.datetime]="", fmt="%Y%m%d",
             add_days=0,  add_mins=0, add_hours=0, add_months=0,add_weeks=0,
             timezone_input=None,
             timezone='Asia/Tokyo', fmt_input="%Y-%m-%d",
             force_dayofmonth=-1,   ###  01 first of month
             force_dayofweek=-1,
             force_hourofday=-1,
             force_minofhour=-1,
             returnval='str,int,datetime/unix'):
    """ One liner for date Formatter
    Doc::

        datenow: 2012-02-12  or ""  emptry string for today's date.
        fmt:     output format # "%Y-%m-%d %H:%M:%S %Z%z"
        date_now(timezone='Asia/Tokyo')    -->  "20200519"   ## Today date in YYYMMDD
        date_now(timezone='Asia/Tokyo', fmt='%Y-%m-%d')    -->  "2020-05-19"
        date_now('2021-10-05',fmt='%Y%m%d', add_days=-5, returnval='int')    -->  20211001
        date_now(20211005, fmt='%Y-%m-%d', fmt_input='%Y%m%d', returnval='str')    -->  '2021-10-05'
        date_now(20211005,  fmt_input='%Y%m%d', returnval='unix')    -->

        date_now(' 21 dec 1012',  fmt_input='auto', returnval='unix')    -->

         integer, where Monday is 0 and Sunday is 6.


        date_now(1634324632848, fmt='%Y-%m-%d', fmt_input='%Y%m%d', returnval='str')    -->  '2021-10-05'

    """
    from pytz import timezone as tzone
    import datetime, time

    if timezone_input is None:
        timezone_input = timezone

    sdt = str(datenow)

    #if isinstance(datenow, int) and len(str(datenow)) == 13:
    #    # convert timestamp from miliseconds to seconds
    #    datenow = datenow / 1000


    if isinstance(datenow, datetime.datetime):
        now_utc = datenow

    elif (isinstance(datenow, float) or isinstance(datenow, int))  and  datenow > 1600100100 and str(datenow)[0] == "1"  :  ### Unix time stamp
        ## unix seconds in UTC
        # fromtimestamp give you the date and time in local time
        # utcfromtimestamp gives you the date and time in UTC.
        #  int(time.time()) - date_now( int(time.time()), returnval='unix', timezone='utc') == 0
        now_utc = datetime.datetime.fromtimestamp(datenow, tz=tzone("UTC") )   ##

    elif len(sdt) > 7 and fmt_input != 'auto':  ## date in string
        now_utc = datetime.datetime.strptime(sdt, fmt_input)

    elif fmt_input == 'auto' and sdt is not None:  ## dateparser
        import dateparser
        now_utc = dateparser.parse(sdt)

    else:
        now_utc = datetime.datetime.now(tzone('UTC'))  # Current time in UTC
        # now_new = now_utc.astimezone(tzone(timezone))  if timezone != 'utc' else  now_utc.astimezone(tzone('UTC'))
        # now_new = now_utc.astimezone(tzone('UTC'))  if timezone in {'utc', 'UTC'} else now_utc.astimezone(tzone(timezone))

    if now_utc.tzinfo == None:
        now_utc = tzone(timezone_input).localize(now_utc)

    now_new = now_utc if timezone in {'utc', 'UTC'} else now_utc.astimezone(tzone(timezone))

    ####  Add months
    now_new = now_new + datetime.timedelta(days=add_days + 7*add_weeks, hours=add_hours, minutes=add_mins,)
    if add_months!=0 :
        from dateutil.relativedelta import relativedelta
        now_new = now_new + relativedelta(months=add_months)


    #### Force dates
    if force_dayofmonth >0 :

        if force_dayofmonth == 31:
            mth = now_new.month 
            if   mth in {1,3,5,7,8,10,12} : day = 31
            elif mth in {4,6,9,11}        : day = 30
            else :
                day = 28             
            now_new = now_new.replace(day=day)

        else :    
            now_new = now_new.replace(day=force_dayofmonth)

    if force_dayofweek >0 :
        actual_day = now_new.weekday()
        days_of_difference = force_dayofweek - actual_day
        now_new = now_new + datetime.timedelta(days=days_of_difference)

    if force_hourofday >0 :
        now_new = now_new.replace(hour=force_hourofday)

    if force_minofhour >0 :
        now_new = now_new.replace(minute=force_minofhour)


    if   returnval == 'datetime': return now_new ### datetime
    elif returnval == 'int':      return int(now_new.strftime(fmt))
    elif returnval == 'unix':     return datetime.datetime.timestamp(now_new)  #time.mktime(now_new.timetuple())
    else:                         return now_new.strftime(fmt)


# A function that takes a min date and a max date then it returns a list of date in that range, it accepts a attribute called "freq" that is the frequency of the date list that will return
def date_now_range(start, 
                   end, 
                   fmt="%Y-%m-%d", 
                   add_days=0,
                   add_mins=0,
                   add_hours=0,
                   add_months=0,
                   add_weeks=0,
                   timezone_input=None,
                   timezone='Asia/Tokyo',
                   fmt_input="%Y-%m-%d",
                   force_dayofmonth=-1, 
                   force_dayofweek=-1, 
                   force_hourofday=-1, 
                   force_minofhour=-1, 
                   returnval='str,int,datetime/unix', 
                   freq='1D') :
    """Function to generate a list of dates in a given range with a specified frequency.
    
    Docs::

        Args:
            start (str): Starting date in the format of fmt_input.
            end (str): Ending date in the format of fmt_input.
            fmt (str): Format of the generated dates (default='%Y-%m-%d').
            add_days (int): Days to add to each generated date (default=0).
            add_mins (int): Minutes to add to each generated date (default=0).
            add_hours (int): Hours to add to each generated date (default=0).
            add_months (int): Months to add to each generated date (default=0).
            add_weeks (int): Weeks to add to each generated date (default=0).
            timezone_input (str): Timezone of the input dates (default=None).
            timezone (str): Timezone of the generated dates (default='Asia/Tokyo').
            fmt_input (str): Format of the input dates (default='%Y-%m-%d').
            force_dayofmonth (int): Day of the month for each generated date (default=-1).
            force_dayofweek (int): Day of the week for each generated date (default=-1).
            force_hourofday (int): Hour of the day for each generated date (default=-1).
            force_minofhour (int): Minute of the hour for each generated date (default=-1).
            returnval (str): Format of the return value (default='str,int,datetime/unix').
            freq (str): Frequency of the date list (default='1D').
        
        Returns:
            list: List of dates.

    """
    from dateutil.relativedelta import relativedelta
    import math,re
    start_date = date_now(datenow = start,
                      fmt = fmt,
                      add_days = add_days,
                      add_mins = add_mins,
                      add_hours=add_hours,    
                      add_months = add_months,
                      add_weeks = add_weeks,
                      timezone_input = timezone_input,
                      timezone = timezone,
                      fmt_input = fmt_input,
                      force_dayofweek = force_dayofweek,
                      force_hourofday = force_hourofday,
                      force_minofhour = force_minofhour,
                      returnval = "datetime")

    end_date = date_now(datenow = end,
                      fmt = fmt,
                      add_days = add_days,
                      add_mins = add_mins,
                      add_hours=add_hours,    
                      add_months = add_months,
                      add_weeks = add_weeks,
                      timezone_input = timezone_input,
                      timezone = timezone,
                      fmt_input = fmt_input,
                      force_dayofweek = force_dayofweek,
                      force_hourofday = force_hourofday,
                      force_minofhour = force_minofhour,
                      returnval = "datetime")
    
    matches = re.match(r'(\d+)([A-Za-z])', freq)
    if matches:
        freq = int(matches.group(1))
        freq_type = matches.group(2)
    else:
        freq = 1
        freq_type = "D"

    if freq_type == 'D':
        limit = math.floor((end_date - start_date).days / freq) +1
        date_list = [start_date + relativedelta(days=x*freq) for x in range(0, limit)]
    elif freq_type == 'W':
        limit = math.floor((end_date - start_date).days / (freq*7)) + 1
        date_list = [start_date + relativedelta(weeks=x * freq) for x in range(0, limit)]
    elif freq_type == 'M':
        months_between = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        limit = months_between // freq + 1
        date_list = [start_date + relativedelta(months=x * freq) for x in range(limit)]
    elif freq_type == 'Y':
        years_between = end_date.year - start_date.year
        limit = years_between // freq + 1
        date_list = [start_date + relativedelta(years=x * freq) for x in range(limit)]
    elif freq_type == 'Q':
        quarters_between = (end_date.year - start_date.year) * 4 + (end_date.month - start_date.month) // 3
        limit = quarters_between // freq + 1
        date_list = [start_date + relativedelta(months=x * freq * 3) for x in range(limit)]
    else :
        limit = math.floor((end_date - start_date).days / freq) +1
        date_list = [start_date + relativedelta(days=x*freq) for x in range(0, limit)]

    return [ date_now(datenow = ti,
                      fmt = fmt,
                      timezone_input = timezone_input,
                      timezone = timezone,
                      fmt_input = fmt_input,
                      force_dayofmonth = force_dayofmonth,
                      force_dayofweek = force_dayofweek,
                      force_hourofday = force_hourofday,
                      force_minofhour = force_minofhour,
                      returnval = returnval) for ti in date_list]



####################################################################################################3
def pd_date_split(df, coldate =  'time_key', prefix_col ="",sep="/" ,verbose=False ):
    """function pd_date_split to split date into different formate.

    Docs::

        Args:
            df (pd):          df is the random date
            coldate (str):    The name we want to give to the random date. (Ex: 'Birthdate')
            prefix_col (str): The space we leave in prefix of each date.
            sep (str):         separation between (Year,week), (year,Month), (year, quarter)
                         (Ex: year quarter 2021/3, '/' is separation)
            verbose (bool):   If True, print the output.
        Returns: Return date in different formate.

        Example:    from utilmy.dates import pd_date_split

                    df2= pd_date_split(df, coldate ='Birthdate', sep='/')
                    print(df2)


                    Output:      Birthdate        date     year   month   day   weekday   weekmonth   weekmonth2   weekyeariso   weekyear2   quarter   yearweek   yearmonth  yearqarter   isholiday
                                2021-11-26  2021-11-26     2021      11    26         4           4            4            47          48         3    2021/47     2021/11      2021/3          0



        
    """
    import pandas as pd

    df = df.drop_duplicates(coldate)
    df['date'] =  pd.to_datetime( df[coldate] )

    ############# dates
    df['year']          = df['date'].apply( lambda x : x.year   )
    df['month']         = df['date'].apply( lambda x : x.month   )
    df['day']           = df['date'].apply( lambda x : x.day   )
    df['weekday']       = df['date'].apply( lambda x : x.weekday()   )
    df['weekmonth']     = df['date'].apply( lambda x : date_weekmonth(x)   )
    df['weekmonth2']    = df['date'].apply( lambda x : date_weekmonth2(x)   )
    df['weekyeariso']   = df['date'].apply( lambda x : x.isocalendar()[1]   )
    df['weekyear2']     = df['date'].apply( lambda x : date_weekyear2( x )  )
    df['quarter']       = df.apply( lambda x :  int( x['month'] / 4.0) + 1 , axis=1  )

    def merge1(x1,x2):
        if sep == "":
            return int(str(x1) + str(x2))
        return str(x1) + sep + str(x2)

    df['yearweek']      = df.apply(  lambda x :  merge1(  x['year']  , x['weekyeariso'] )  , axis=1  )
    df['yearmonth']     = df.apply( lambda x : merge1( x['year'] ,  x['month'])         , axis=1  )
    df['yearquarter']   = df.apply( lambda x : merge1( x['year'] ,  x['quarter'] )         , axis=1  )

    df['isholiday']     = date_is_holiday(df['date'])

    exclude = [ 'date', coldate]
    df.columns = [  prefix_col + x if not x in exclude else x for x in df.columns]
    if verbose : log( "holidays check", df[df['isholiday'] == 1].tail(15)  )
    return df


def date_to_timezone(tdate,  fmt="%Y%m%d-%H:%M", timezone='Asia/Tokyo'):
    """ date_to_timezone is used to get date and time for particular timezone

        Docs::

            Args:
                tdate (datetime):    date to convert to timezone
                fmt (str):      formate of date and time (Ex: YYYYMMDD-HH:MM)
                timezone (str): timezone for which we want to find time and date (Ex: 'Asia/Tokyo')

            Returns: return date and time according to timezone

            Example:   from utilmy.dates import date_to_timezone
                       import datetime
                       res= date_to_timezone(datetime.datetime.now())
                       print(res)

                       Output:   20221027-15:04
    """
    from pytz import timezone as tzone
    import datetime
    # Convert to US/Pacific time zone
    now_pacific = tdate.astimezone(tzone('Asia/Tokyo'))
    return now_pacific.strftime(fmt)


##def date_now(fmt="%Y-%m-%d %H:%M:%S %Z%z", add_days=0, timezone='Asia/Tokyo'):
#from utilmy.utilmy_base import date_now




def date_is_holiday(array):
    """function date_is_holiday to check the holiday on array of pd.date format.

        Docs::

            Args:
                array (list):   array of pd.date format to check weather it is holiday or not
                                ( Ex. date_is_holiday([ pd.to_datetime("2015/1/1") ]) )

            Returns:    1 if the date is holiday
                        0 if the date is not holiday

            Example:    from utilmy.dates import  date_is_holiday
                        res = date_is_holiday([pd.to_datetime('2000-01-01')])
                        print(res)

                        Output: [1]

    """
    import holidays , numpy as np
    jp_holidays = holidays.CountryHoliday('JP')
    return np.array( [ 1 if x in jp_holidays else 0 for x in array]  )


def date_weekmonth2(d):
     """function date_weekmonth2 to get the week of the month on given date.

    Docs::

        Args:
             d(datetime):   date to find the week of the month (Ex: datetime.datetime(2020, 5, 17))
        Returns:   week of the month on given date

        Example:    from utilmy.dates import  date_weekmonth2
                    res = date_weekmonth2(datetime.datetime(2020, 5, 17))
                    print(res)

                    Output: 3
        """
     w = (d.day-1)//7+1
     if w < 0 or w > 5 :
         return -1
     else :
         return w


def date_weekmonth(date_value):
     """  Incorrect """
     w = (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)
     if w < 0 or w > 6 :
         return -1
     else :
         return w


def date_weekyear2(dt) :
    """function date_weekyear2 to get the week of the year on given date.

    Docs::

        Args:
            dt (datetime):  date to get the week of the year (Ex: datetime.datetime(2020, 5, 17))
        Returns: return week of that date in that year

        Example:    from utilmy.dates import  date_weekyear2
                    res = date_weekyear2(datetime.datetime(2020, 5, 17))
                    print(res)

                    Output: 20
        """
    return ((dt - datetime.datetime(dt.year,1,1)).days // 7) + 1


def date_weekday_excel(x) :
    """method returns the day of the week as an integer, where Monday is 1 and Sunday is 7

    Docs::

        Args:
            x (str):   date in string format (Ex: '20200517')
        Returns: weekday of the date
        """
    import datetime
    date = datetime.datetime.strptime(x,"%Y%m%d")
    wday = date.weekday()
    if wday != 7 : return wday+1
    else :    return 1


def date_weekyear_excel(x) :
    """function is used to return a ISO Week Number.

    Docs::
    
        Args:
              x (str): date in string format (Ex: '20200517')
        Returns: ISO Week Number
    """
    import datetime
    date = datetime.datetime.strptime(x,"%Y%m%d")
    return date.isocalendar()[1]


def date_generate(start='2018-01-01', ndays=100) :
    """function to generate list of n(ndays) consecutive days from the start date.

    Docs::

        Args:
            start (str):   Starting Date default to '2018-01-01'
            ndays (int):   Number of dates to generate (default to 100)
        Returns: List of generated dates

        """
    from dateutil.relativedelta import relativedelta
    start0 = datetime.datetime.strptime(start, "%Y-%m-%d")
    date_list = [start0 + relativedelta(days=x) for x in range(0, ndays)]
    return date_list


###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()