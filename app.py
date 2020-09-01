from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbproject

# HTML 화면 보여주기
@app.route('/')
def localpage():
    return render_template('index.html')

@app.route('/hotel')
def hotelpage():
    return render_template('hotel_page.html')

@app.route('/attraction')
def attractionpage():
    return render_template('attraction_page.html')

@app.route('/restaurant')
def restaurantpage():
    return render_template('restaurant_page.html')

# 호텔 웹스크래핑
@app.route('/hotel/api', methods=['GET'])
def find_hotel():
    driver = webdriver.Chrome('/Users/gayoung/Downloads/chromedriver')
    driver.implicitly_wait(3)

    driver.get('https://hotel.naver.com/hotels/main')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    notices = soup.select('div.p_inr > div.p_info > a > span')

    for n in notices:
        print(n.text.strip())

    return jsonify({'result': 'success', 'hotelList': '연결'})

@app.route('/attraction/api', methods=['POST'])
def find_attraction():
    db.attraction.drop()
    # 전체 데이터 삭제
    destination_receive = request.form['destination_give']
    baseUrl = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query='
    plusUrl = destination_receive

    url = baseUrl + urllib.parse.quote_plus(plusUrl) + urllib.parse.quote_plus(' 가볼만한곳')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.find_all(class_='sh_blog_title')

    for i in title:
        attr = {
            'title': i.attrs['title'],
            'link': i.attrs['href']
        }
        db.attraction.insert_one(attr)

        # print(i.attrs['title'])
        # print(i.attrs['href'])
        # print('\n')

    return jsonify(({'result': 'success'}))

@app.route('/attraction/api', methods=['GET'])
def view_attraction():
    attraction = list(db.attraction.find({}, {'_id': 0}))
    return jsonify(({'result': 'success', 'attraction': attraction}))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)