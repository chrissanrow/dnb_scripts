# dnb_scripts

## Installing necessary dependencies

Assuming you have installed python3 and pip3 already:

`pip3 install python3-discogs-client`

`pip3 install musicbrainzngs`

`pip3 install pandas`

## Obtaining API Keys

In order to run most of the scripts, you will need to add your own API keys to a .env file.

## discogs_script.py usage

Run script with `python3 discogs_script.py <YEAR_RANGE>` to generate dnb visualization JSONs

To geocode this data, run `python3 country_coords_script.py`

A similar process can be applied for `city_coords_script.py` and `discogs_script_local.py`