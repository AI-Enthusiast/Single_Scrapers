import configparser
import os

from Media.radio import radio_update
from Media.podcasts import podcast_update

config = configparser.ConfigParser()
config.read("config.ini")

test = True

if __name__ == "__main__":
    # radio_update(config["PATHS"]["radio"])
    podcast_update(config["PATHS"]["podcasts"], test)