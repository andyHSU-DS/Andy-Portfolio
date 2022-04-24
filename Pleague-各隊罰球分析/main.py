import pandas as pd
import requests
import bs4
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re

from module.module import PLG

data_frame_list = []
for x in ['鋼鐵人','攻城獅','領航猿','國王','勇士']:
    team          = PLG(x)
    team_info     = team.get_team_info()
    matchup       = team.matchup_and_host_info()
    team_完整_info = team.match資訊(team_info, matchup)
    整理完成資料    = team.資料處理(team_完整_info)
    Dreamers_Home = 整理完成資料[整理完成資料['夢想家主場'] == 'Y']
    夢想家主場_FT = round((Dreamers_Home['罰球(進)'].sum()/Dreamers_Home['罰球(出手)'].sum())*100,2)
    data_frame_list.append(x,'夢主場',夢想家主場_FT)
    N_Dreamers_Home = 整理完成資料[整理完成資料['夢想家主場'] == 'N']
    N_Dreamers_Home['罰球(進)'].sum()/Dreamers_Home['罰球(出手)'].sum()
    非夢想家主場_FT = round((N_Dreamers_Home['罰球(進)'].sum()/N_Dreamers_Home['罰球(出手)'].sum())*100,2)
    data_frame_list.append(x,'非夢主場',非夢想家主場_FT)
