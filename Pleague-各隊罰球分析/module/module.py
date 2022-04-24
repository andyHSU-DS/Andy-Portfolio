import pandas as pd
import requests
import bs4

import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import re

class PLG:
    #定義隊名跟url
    def __init__(self,team_name):
        self.name = team_name
        if '勇士' in self.name:
            self.url = 'https://pleagueofficial.com/team/1'
        elif '攻城獅' in self.name:
            self.url = 'https://pleagueofficial.com/team/3'
        elif '鋼鐵人' in self.name:
            self.url = 'https://pleagueofficial.com/team/5'
        elif '國王' in self.name:
            self.url = 'https://pleagueofficial.com/team/6'
        elif '領航猿' in self.name:
            self.url = 'https://pleagueofficial.com/team/2'
        else:
            self.url = 'https://pleagueofficial.com/team/4'
    #得到資訊
    def get_team_info(self):
        all_data          = []
        table_titles_list = []
        table_datas_list  = []
        if self.url != None:
            team_info_web_obj = requests.get(self.url)
            team_info_soup    = bs4.BeautifulSoup(team_info_web_obj.text,'lxml')
            #大表
            table_record      = team_info_soup.find('table',class_='table fs12 col-md-12 bg-light table-hover')
            #表頭
            table_titles      = table_record.find('tr').find_all('th')
            for table_title in table_titles:
                table_titles_list.append(table_title.text)
            
            #表內資料，table_datas是每一行（每場）
            table_datas       = table_record.find('tbody').find_all('tr')
            for table_data in table_datas:
                each_matchup_data = []
                #每場的每筆資料
                for matchup_detail in table_data.find_all('td'):
                    each_matchup_data.append(matchup_detail.text)
                if each_matchup_data[2] == '':
                    pass
                else:
                    table_datas_list.append(each_matchup_data)
        else:
            pass
        
        all_data.extend(table_datas_list)
        return pd.DataFrame(all_data,columns = table_titles_list)

    #全聯盟的對戰內容
    def matchup_and_host_info(self,url = 'https://pleagueofficial.com/schedule-regular-season'):
        path   = r'/Users/andyhsu/Documents/GitHub/Andy-Portfolio/Pleague-各隊罰球分析/chromedriver'

        日程 = []
        客隊 = []
        主隊 = []
        driver = webdriver.Chrome(path)

        driver.get('https://pleagueofficial.com/schedule-regular-season')
        #即將開打取消
        driver.find_element_by_xpath('/html/body/section[3]/div/div[1]/h1/label/input').click()

        url = driver.page_source
        url_解析 = bs4.BeautifulSoup(url,'lxml')
        目標container = url_解析.find_all('div',class_='container')[1]
        全部對戰組合 = 目標container.find('div',class_='bg-white text-dark border-bottom border-top matches')
        每個對戰組合 = 全部對戰組合.find_all('div',class_ = re.compile('row justify-content-center pt-3 pb-0 pt-md-3 pb-md-3 match_row mx-0'))

        for num in 每個對戰組合:
            日期 = num.find('div',class_='col-lg-1 col-12 text-center align-self-center match_row_datetime').find('h5').text
            日程.append(日期)
            主客隊資訊 = num.find_all('div',class_=re.compile('col-lg-3 col-2 align-self-center'))
            for info in 主客隊資訊:
                主客隊文字資訊 = info.find_all('div',class_='text-center mt-md-2')
                for 文字資訊 in 主客隊文字資訊:
                    if 文字資訊.find('h6',class_='fs12 mb-2 PC_only').text == '客隊':
                        客隊.append(文字資訊.find('span',class_='PC_only fs14').text)
                    elif 文字資訊.find('h6',class_='fs12 mb-2 PC_only').text == '主隊':
                        主隊.append(文字資訊.find('span',class_='PC_only fs14').text)

        driver.close()
        賽程資訊 = pd.DataFrame({'客隊':客隊, '主隊':主隊},index=日程)
        return 賽程資訊

    #input是該隊賽程資料，對戰組合資料及我要看的球隊
    def match資訊(self,team_dataframe, match_up_dataframe):
        specific_match_up_dataframe       = match_up_dataframe[(match_up_dataframe['主隊'] == self.name) | (match_up_dataframe['客隊'] == self.name)]
        team_dataframe['比賽日期'] = team_dataframe['比賽日期'].apply(lambda x:x.replace('-','/')[5:])
        整理後資料 = team_dataframe.merge(specific_match_up_dataframe,left_on='比賽日期',right_index=True)
        return 整理後資料

    #將match資訊的return放入得到我要的資料
    def 資料處理(self,df):
        df['夢想家主場'] = df['主隊'].apply(lambda x: 'Y' if x == '夢想家' else 'N')
        df['罰球(進)']   = df['罰球'].apply(lambda x: int(x.split('-')[0]))
        df['罰球(出手)']   = df['罰球'].apply(lambda x: int(x.split('-')[1]))
        return df