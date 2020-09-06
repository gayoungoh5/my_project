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
@app.route('/hotel/api', methods=['POST'])
def find_hotel():
    destination_receive = request.form['destination_give']

    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')  # 웹 브라우저를 띄우지 않는 headlss chrome 옵션 적용
    webdriver_options.add_argument('lang=ko_KR')  # 언어 설정
    chromedriver = '/Users/gayoung/Downloads/chromedriver'
    driver = webdriver.Chrome(chromedriver, chrome_options=webdriver_options)
    driver.implicitly_wait(3)

    driver.get('https://hotel.naver.com/hotels/main')
    driver.find_element_by_id('hotel_search').send_keys(destination_receive)
    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[2]/div[2]/ul/li/a').click()
    driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a').click()

    titles = driver.find_elements_by_css_selector('.hotel_name_ko')
    for t in titles:
        db.hotel.insert_one(t)
    return jsonify({'result': 'success', 'hotelList': '연결'})

@app.route('/hotel/api', methods=['GET'])
def show_hotel():
    hotels = list(db.hotel.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'hotel_list': hotels})

@app.route('/attraction/api', methods=['GET'])
def show_attraction():
    attractions = list(db.attraction.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'attraction': attractions})

@app.route('/attraction/api', methods=['POST'])
def find_attraction():

    destination_receive = request.form['destination_give']
    # # 오픈api 불러오기
    # baseUrl = 'https://search.naver.com/search.naver?where=post&sm=tab_jum&query='
    # plusUrl = destination_receive
    #
    # url = baseUrl + urllib.parse.quote_plus(plusUrl) + urllib.parse.quote_plus(' 가볼만한곳')
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url, headers=headers)
    #
    # soup = BeautifulSoup(data.text, 'html.parser')
    # title = soup.find_all(class_='sh_blog_title')
    #
    # for i in title:
    #     attr = {
    #         'title': i.attrs['title'],
    #         'link': i.attrs['href']
    #     }
    #     db.attraction.insert_one(attr)

        # print(i.attrs['title'])
        # print(i.attrs['href'])
        # print('\n')

    return jsonify(({'result': 'success'}))

@app.route('/attraction/api', methods=['GET'])
def view_attraction():
    # 전체 데이터 삭제
    open_api_key = 'UnDRW2qZhUsa9c42J%2F2hZNGAMwsVuXffmWIuuWCdR9Xp2qkOv%2FB888mhcz8EFJJRXHzxrEnsP%2FT6bv54wKkBiQ%3D%3D'
    params = '&arrange=A&listYN=Y&pageNo=1&numOfRows=5000&MobileOS=ETC&MobileApp=AppTesting'

    open_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchStay?ServiceKey=' + open_api_key + params

    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    data = soup.find_all()
    return jsonify(({'result': 'success', 'attraction': data}))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)