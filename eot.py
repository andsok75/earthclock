#!/usr/bin/env python

# This script obtains apparent solar time at location (0, 0) at 12:00:00 UTC for every day from 2000-01-01 until 2100-12-31
# and converts these data into equation of time (eot), the time difference between the mean and apparent sun expressed in traditional minutes.
# The equation of time is saved in json format with year as key and array of eot minutes for every day of the year as value.

import json
import sys
from collections import defaultdict

import requests

response = requests.get(
    "https://ssd.jpl.nasa.gov/api/horizons.api",
    params = {
        "format": "text",
        "COMMAND": "'10'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'coord@399'",
        "SITE_COORD": "'0,0,0'",
        "START_TIME": "'2000-01-01 12:00'",
        "STOP_TIME": "'2100-12-31 12:00'",
        "STEP_SIZE": "'1d'",
        "TIME_DIGITS": "'SECONDS'",
        "CSV_FORMAT": "'NO'",
        "QUANTITIES": "'34'",
    },
)
lines = response.text.split('\n')
eot_per_year = defaultdict(list)
for line in lines[lines.index('$$SOE')+1:lines.index('$$EOE')]:
    a = line.split()
    year = a[0].split('-')[0]
    s = float(a[-1])
    m = float(a[-2])
    h = float(a[-3])
    eot = (h + (m + s/60)/60 - 12)*60
    eot_per_year[year].append(round(eot, 2))

json.dump(eot_per_year, sys.stdout, separators=(',', ':'))


"""
The response from Horizons API should look as follows, with data contained between the lines marked with $$SOE and $$EOE.
More details on the API usage can be found at https://ssd-api.jpl.nasa.gov/doc/horizons.html.


```
API VERSION: 1.2
API SOURCE: NASA/JPL Horizons API



*******************************************************************************
Ephemeris / API_USER Sun Mar  3 19:48:12 2024 Pasadena, USA      / Horizons    
*******************************************************************************
Target body name: Sun (10)                        {source: DE441}
Center body name: Earth (399)                     {source: DE441}
Center-site name: (user defined site below)
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:00:00.0000 UT      
Stop  time      : A.D. 2100-Dec-31 12:00:00.0000 UT      
Step-size       : 1440 minutes
*******************************************************************************
Target pole/equ : IAU_SUN                         {East-longitude positive}
Target radii    : 696000.0, 696000.0, 696000.0 km {Equator_a, b, pole_c}       
Center geodetic : 0.0, 0.0, 0.0                   {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.0, 6378.137, 0.0              {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : ITRF93                          {East-longitude positive}
Center radii    : 6378.137, 6378.137, 6356.752 km {Equator_a, b, pole_c}       
Target primary  : Sun
Vis. interferer : MOON (R_eq= 1737.400) km        {source: DE441}
Rel. light bend : Sun                             {source: DE441}
Rel. lght bnd GM: 1.3271E+11 km^3/s^2                                          
Atmos refraction: NO (AIRLESS)
RA format       : HMS
Time format     : CAL 
Calendar mode   : Mixed Julian/Gregorian
EOP file        : eop.240301.p240525                                           
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2024-MAR-01. PREDICTS-> 2024-MAY-24
Units conversion: 1 au= 149597870.700 km, c= 299792.458 km/s, 1 day= 86400.0 s 
Table cut-offs 1: Elevation (-90.0deg=NO ),Airmass (>38.000=NO), Daylight (NO )
Table cut-offs 2: Solar elongation (  0.0,180.0=NO ),Local Hour Angle( 0.0=NO )
Table cut-offs 3: RA/DEC angular rate (     0.0=NO )                           
*******************************************************************************
 Date__(UT)__HR:MN:SS     L_Ap_SOL_Time
***************************************
$$SOE
 2000-Jan-01 12:00:00 *m  11 56 43.2074
 2000-Jan-02 12:00:00 *m  11 56 14.8592
...
 2100-Dec-30 12:00:00 *m  11 57 38.1239
 2100-Dec-31 12:00:00 *m  11 57 09.3426
$$EOE
*******************************************************************************
Column meaning:
 
TIME

  Times PRIOR to 1962 are UT1, a mean-solar time closely related to the
prior but now-deprecated GMT. Times AFTER 1962 are in UTC, the current
civil or "wall-clock" time-scale. UTC is kept within 0.9 seconds of UT1
using integer leap-seconds for 1972 and later years.

  Conversion from the internal Barycentric Dynamical Time (TDB) of solar
system dynamics to the non-uniform civil UT time-scale requested for output
has not been determined for UTC times after the next July or January 1st.
Therefore, the last known leap-second is used as a constant over future
intervals.

  Time tags refer to the UT time-scale conversion from TDB on Earth
regardless of observer location within the solar system, although clock
rates may differ due to the local gravity field and no analog to "UT"
may be defined for that location.

  Any 'b' symbol in the 1st-column denotes a B.C. date. First-column blank
(" ") denotes an A.D. date.
 
CALENDAR SYSTEM

  Mixed calendar mode was active such that calendar dates after AD 1582-Oct-15
(if any) are in the modern Gregorian system. Dates prior to 1582-Oct-5 (if any)
are in the Julian calendar system, which is automatically extended for dates
prior to its adoption on 45-Jan-1 BC.  The Julian calendar is useful for
matching historical dates. The Gregorian calendar more accurately corresponds
to the Earth's orbital motion and seasons. A "Gregorian-only" calendar mode is
available if such physical events are the primary interest.

  NOTE: "n.a." in output means quantity "not available" at the print-time.
 
SOLAR PRESENCE (OBSERVING SITE)
  Time tag is followed by a blank, then a solar-presence symbol:

       '*'  Daylight (refracted solar upper-limb on or above apparent horizon)
       'C'  Civil twilight/dawn
       'N'  Nautical twilight/dawn
       'A'  Astronomical twilight/dawn
       ' '  Night OR geocentric ephemeris

LUNAR PRESENCE (OBSERVING SITE)
  The solar-presence symbol is immediately followed by a lunar-presence symbol:

       'm'  Refracted upper-limb of Moon on or above apparent horizon
       ' '  Refracted upper-limb of Moon below apparent horizon OR geocentric
            ephemeris
 
 'L_Ap_SOL_Time' =
   Local Apparent SOLAR Time for observing site. This is the time indicated by
a sundial.  TOPOCENTRIC ONLY.  Units: HH MM SS.ffff (sexagesimal angular hours)

Computations by ...

    Solar System Dynamics Group, Horizons On-Line Ephemeris System
    4800 Oak Grove Drive, Jet Propulsion Laboratory
    Pasadena, CA  91109   USA

    General site: https://ssd.jpl.nasa.gov/
    Mailing list: https://ssd.jpl.nasa.gov/email_list.html
    System news : https://ssd.jpl.nasa.gov/horizons/news.html
    User Guide  : https://ssd.jpl.nasa.gov/horizons/manual.html
    Connect     : browser        https://ssd.jpl.nasa.gov/horizons/app.html#/x
                  API            https://ssd-api.jpl.nasa.gov/doc/horizons.html
                  command-line   telnet ssd.jpl.nasa.gov 6775
                  e-mail/batch   https://ssd.jpl.nasa.gov/ftp/ssd/hrzn_batch.txt
                  scripts        https://ssd.jpl.nasa.gov/ftp/ssd/SCRIPTS
    Author      : Jon.D.Giorgini@jpl.nasa.gov

*******************************************************************************


```
"""
