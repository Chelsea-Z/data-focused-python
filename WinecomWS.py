#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:26:22 2018

@author: liuziqi
"""

import bs4
from bs4 import BeautifulSoup
import os
import requests
import re
import csv
import pandas as pd
from pandas import DataFrame
import time


BASE_URL = 'https://www.wine.com/list/wine/7155/'
#PAGE_NUM = range(654) #max page number; starting from 1

MAX_PAGE_NUM = 654 #max page number; starting from 1

data = DataFrame(columns=['Title', 'Year', 'Varietal', 'Price', 'Region', 'Country','Score_WS','Score_RP','Score_W&S', 'Score_JH', 'Score_CG', 'Score_WE', 'Score_WW', 'Score_BH', 'Score_JS', 'Score_TP', 'Score_D', 'Score_V', 'Score_JD','StarRating','numRater', 'Shopping_Link', 'Img_src'])    

start_time = time.time()

for i in range(1, MAX_PAGE_NUM):
    URL = BASE_URL + str(i)
    res = requests.get(URL)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #Find all the products in current page
    product_list = soup.find_all("li", {"class":"prodItem"})

    for j in range(0, len(product_list)):
        #Get Title of a product
        indexNum = (i-1)*len(product_list) + j
        prodItemInfo_name = product_list[j].find("span", {"class":"prodItemInfo_name"})
        prodItem_name = prodItemInfo_name.text.strip()
        data = data.append({'Title': prodItem_name}, ignore_index=True)
        
        #Get Year
        year = ''
        year_list = re.findall("\d+", prodItem_name)
        for yr in year_list:
            if int(yr)>1900 and int(yr)<=2018: year = int(yr)
        data.ix[indexNum, 'Year'] = year
        
        #Get Varietal
        varietal = ""
        prodItemInfo_varietal = product_list[j].find("span", {"class":"prodItemInfo_varietal"})
        varietal = prodItemInfo_varietal.text.strip()
        data.ix[indexNum, 'Varietal'] = varietal 
        
        
        #Get Price
        price = ""
        Price_Whole = ""
        Price_Fractional = ""
        productPrice_price_regWhole = product_list[j].find("span", {"class":"productPrice_price-regWhole"})
        productPrice_price_regFractional = product_list[j].find("span", {"class":"productPrice_price-regFractional"})
        
        productPrice_price_saleWhole = product_list[j].find("span", {"class":"productPrice_price-saleWhole"})
        productPrice_price_saleFractional = product_list[j].find("span", {"class":"productPrice_price-saleFractional"})
        
        if productPrice_price_saleWhole:
            Price_Whole = productPrice_price_saleWhole.text.strip()
            Price_Whole = Price_Whole.replace(',', '')
            Price_Fractional = productPrice_price_saleFractional.text.strip()
        else:
            Price_Whole = productPrice_price_regWhole.text.strip()
            Price_Whole = Price_Whole.replace(',', '')
            Price_Fractional = productPrice_price_regFractional.text.strip()

        if Price_Fractional:
            price = int(Price_Whole) + 0.01*int(Price_Fractional)
        else:
            price = int(Price_Whole)
                
        data.ix[indexNum, 'Price'] = price
        
        
        #Get Region and Country
        region =""
        country = ""
        prodItem_origin = product_list[j].find("span", {"class":"prodItemInfo_originText"})
        origin = prodItem_origin.text.strip()
        originList = origin.split(',')
        if len(originList) > 0: country = originList[-1].strip()
        if len(originList) > 1: region = originList[-2].strip()
        
        data.ix[indexNum, 'Region'] = region
        data.ix[indexNum, 'Country'] = country
        
        
        #Get Star Rating
        starRating = ""
        prodItem_star = product_list[j].find("span", {"class":"averageRating_average"})
        starRating = prodItem_star.text.strip()
        if starRating: data.ix[indexNum, 'StarRating'] = float(starRating)
        
        numRater = ""
        prodItem_star_count = product_list[j].find("span", {"class":"averageRating_number"})
        numRater = prodItem_star_count.text.strip()
        if starRating: data.ix[indexNum, 'numRater'] = float(numRater)
        
        #Get Shopping Link
        sub_url = ""
        web_url = "https://www.wine.com"
        prodItem_URL = ""
        prodItem_subURL = product_list[j].find("a", {"class":"prodItemImage_link"})
        sub_url = prodItem_subURL['href']
        if sub_url:
            prodItem_URL = web_url + str(sub_url)
            data.ix[indexNum, 'Shopping_Link'] = prodItem_URL
        
        #Get Image Scr
        imgURL = ""
        prodItem_img = product_list[j].find("img", {"class":"prodItemImage_image-default"})
        sub_src = prodItem_img['src']
        if sub_src: 
            imgURL = web_url + str(sub_src)
            data.ix[indexNum, 'Img_src'] = imgURL
        
        #Get ratings by critics
        Score_WS = None
        Score_RP = None
        Score_W_S = None
        Score_JH = None
        Score_CG = None
        Score_WE = None
        Score_WW = None
        Score_BH = None
        Score_JS = None
        Score_TP = None
        Score_D = None
        Score_V = None
        Score_JD = None
        
        
        prodItem_scores_li = product_list[j].find_all("li", {"class":"wineRatings_listItem"})
        for m in range(0, len(prodItem_scores_li)):
            org = ""
            score = 0
            org = re.search('<span class="wineRatings_initials">(.+?)</span>', str(prodItem_scores_li[m])).group(1)
            score = re.search('<span class="wineRatings_rating">(.+?)</span>', str(prodItem_scores_li[m])).group(1)
            
            if org == 'WS': Score_WS = score
            elif org == 'RP': Score_RP = score
            elif org == 'W&S': Score_W_S = score
            elif org == 'JH': Score_JH = score
            elif org == 'CG': Score_CG = score
            elif org == 'WE': Score_WE = score
            elif org == 'WW': Score_WW = score
            elif org == 'BH': Score_BH = score
            elif org == 'JS': Score_JS = score
            elif org == 'TP': Score_TP = score
            elif org == 'D': Score_D = score
            elif org == 'V': Score_V = score
            elif org == 'JD': Score_JD = score
        
        if Score_WS: data.ix[indexNum, 'Score_WS'] = int(Score_WS)
        if Score_RP: data.ix[indexNum, 'Score_RP'] = int(Score_RP)
        if Score_W_S: data.ix[indexNum, 'Score_W&S'] = int(Score_W_S)
        if Score_JH: data.ix[indexNum, 'Score_JH'] = int(Score_JH)
        if Score_CG: data.ix[indexNum, 'Score_CG'] = int(Score_CG)
        if Score_WE: data.ix[indexNum, 'Score_WE'] = int(Score_WE)
        if Score_WW: data.ix[indexNum, 'Score_WW'] = int(Score_WW)
        if Score_BH: data.ix[indexNum, 'Score_BH'] = int(Score_BH)
        if Score_JS: data.ix[indexNum, 'Score_JS'] = int(Score_JS)
        if Score_TP: data.ix[indexNum, 'Score_TP'] = int(Score_TP)
        if Score_D: data.ix[indexNum, 'Score_D'] = int(Score_D)
        if Score_V: data.ix[indexNum, 'Score_V'] = int(Score_V)
        if Score_JD: data.ix[indexNum, 'Score_JD'] = int(Score_JD)
        

elapsed_time = round(time.time() - start_time, 2)
print("Seconds:")
print(elapsed_time)

#Write data to csv file
data.to_csv("scrappedData.csv")
        

        
        
        
        
        
        
        
        
        
        
        