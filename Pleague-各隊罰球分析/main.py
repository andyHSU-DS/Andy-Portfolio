import pandas as pd
import requests
import bs4
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re

from module.module import PLG

data_frame_list = pd.DataFrame()
for x in ['鋼鐵人','攻城獅','領航猿','國王','勇士']:
    team          = PLG(x)
    team_info     = team.get_team_info()
    matchup       = team.matchup_and_host_info()
    team_完整_info = team.match資訊(team_info, matchup)
    整理完成資料    = team.資料處理(team_完整_info)
    各隊最終資料    = team.資料彙整(整理完成資料)
    data_frame_list = data_frame_list.append(各隊最終資料)
