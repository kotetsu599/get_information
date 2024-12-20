
import datetime
import requests
from bs4 import BeautifulSoup
import os

def is_prime(num):
    if num == 2:
        return True
    if num%2 == 0 or num%5==0:
        return False
    
    for i in range(int(num**0.5)+1):
        if i != 0 and i != 1:
            if num%i == 0:
                return False
    return True

now = datetime.datetime.now()
nums_str = list(str(now.month) + str(now.day))

added_num = 0
for num in nums_str:
    added_num += int(num)
print(f"今日の日付 {str(now.month)}月{str(now.day)}日の数字をそれぞれ加算した数は{str(added_num)}で、その数は{"素数"if is_prime(added_num)else "非素数"}です。")
print("情報取得中...")

with open('居住地.txt', 'r', encoding='utf-8') as file:
    first_line = file.readline().strip() 

items = first_line.split()

residence_prefecture = items[0]
residence_city = items[1]
residence_prefecture_url = ""
residence_city_url = "" #最終的なURL

r=requests.get("https://tenki.jp/")
soup_prefectures = BeautifulSoup(r.text,"html.parser")

prefectures_links = []#{県名:リンク}
for a_tag in soup_prefectures.find_all("a",class_="pref-link"):
    prefecture_link = {
        "pref":a_tag.text,
        "link":f"https://tenki.jp{a_tag["href"]}"#/forecast/a/b/
    }
    prefectures_links.append(prefecture_link)

if residence_prefecture != "北海道":
    for prefecture_link in prefectures_links:
        if prefecture_link["pref"] == residence_prefecture:
            residence_prefecture_url = prefecture_link["link"]
else:
    Hokkaido_links = []
    prefectures_for_Hokkaido = ["道央","道北","道東","道南"]
    for prefecture_for_Hokkaido in prefectures_for_Hokkaido:
        for prefecture_link in prefectures_links:
            if prefecture_link["pref"] == prefecture_for_Hokkaido:
                Hokkaido_links.append(prefecture_link["link"])
                
if residence_prefecture_url == "" and residence_prefecture != "北海道":
    input("都道府県が見つかりませんでした。")
    os._exit(0)
if residence_prefecture != "北海道":
    r=requests.get(residence_prefecture_url)
    soup_cities = BeautifulSoup(r.text,"html.parser")

    for a_tag in soup_cities.find_all("a"):
        if a_tag.text == residence_city:#だるかった
            residence_city_url = f"https://tenki.jp{a_tag["href"]}"
else:
    for Hokkaido_link in Hokkaido_links:
        r = requests.get(Hokkaido_link)
        soup_cities = BeautifulSoup(r.text, "html.parser")

        for a_tag in soup_cities.find_all("a"):
            if a_tag.text == residence_city:
                residence_city_url = f"https://tenki.jp{a_tag['href']}"
                break
        else:
            continue
        break

if residence_city_url == "":
    input("市区町村が見つかりませんでした。")
    os._exit(0)
        
r=requests.get(residence_city_url)
soup_tenki = BeautifulSoup(r.text,"html.parser")
r=requests.get("https://www.nikkei.com/markets/worldidx/chart/usdjpy/")
soup_kawase = BeautifulSoup(r.text,"html.parser")
r=requests.get("https://www.nikkei.com/markets/worldidx/chart/nk225/")
soup_nikkei = BeautifulSoup(r.text,"html.parser")
r=requests.get("https://news.goo.ne.jp/")
soup_news = BeautifulSoup(r.text,"html.parser")
news_items = []
for a_tag in soup_news.find_all('a', href=True):
    headline = a_tag.find('span', class_='list-title-topics')
    if headline:
        news_items.append({
            'headline': headline.get_text(strip=True),
            'url': f"https://news.goo.ne.jp{a_tag['href']}"
        })
        if len(news_items) > 10:
            news_items = news_items[:10]
            
os.system("cls")#日付を加算した数が素数であるかみたいなのを消すため。

print(f"""___天気___
天気　　:{soup_tenki.find('p', class_='weather-telop').text}
最高気温:{soup_tenki.find("dd",class_="high-temp temp").find('span',class_='value').text}℃
最低気温:{soup_tenki.find("dd",class_="low-temp temp").find('span',class_='value').text}℃
        """)
print(f"""___経済___
為替　　:{soup_kawase.find("span",class_="economic_value_now a-fs26").text}円
日経平均:{soup_nikkei.find("span",class_="economic_value_now a-fs26").text}円
        """)
print("___記事___")
for news_item in news_items:
    print(f"・{news_item["headline"]}..{news_item["url"]}")
input()
