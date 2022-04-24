import pandas as pd
import requests
import bs4
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re

from module.module import get_team_info
from module.module import matchup_and_host_info as match_info
from module.module import match資訊

Matchup_Info       = match_info()
Fubon_Braves_Info = get_team_info('https://pleagueofficial.com/team/1')
Fubon_Braves_Info_含主客場資訊 = match資訊(Fubon_Braves_Info,Matchup_Info,'勇士')

print(Fubon_Braves_Info_含主客場資訊)