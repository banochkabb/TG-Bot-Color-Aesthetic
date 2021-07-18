import os

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver


def hex_to_rgb(code):
    code = code.lstrip('#')
    l = len(code)
    return tuple(int(code[i:i + l // 3], 16) for i in range(0, l, l // 3))


def make_table(r):
    html = BS(r.content, 'html.parser')
    colors = html.find_all('td')
    hex_c1 = [i.text.strip() for i in colors]
    table = pd.DataFrame(list(map(lambda x: x.split('('), hex_c1)))
    table.columns = ['name', 'hex_code']
    table['hex_code'] = table['hex_code'].apply(lambda x: x[:-1])
    table['rgb_code'] = table['hex_code'].apply(hex_to_rgb)
    return table


def driver_fun(col_url):
    chromrdriver = '/Users/varya/Downloads/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromrdriver
    driver = webdriver.Chrome(chromrdriver)
    driver.get(col_url)
    with open('images.html', 'w') as f:
        f.write(driver.page_source)
    driver.close()


def closest_color(code):
    red, green, blue = code
    color_diffs = []
    r = requests.get('https://xkcd.com/color/rgb/')
    table = make_table(r)
    rgb_val = table['rgb_code'].values
    for color in rgb_val:
        code_red, code_green, code_blue = color
        color_diff = (red - code_red) ** 2 + (green - code_green) ** 2 + (blue - code_blue) ** 2
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]
