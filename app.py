from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient
import urllib.parse


app = Flask(__name__)

client = MongoClient('mongodb://test:test@13.125.185.68', 27017)
db = client.seoul_matjip

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

@app.route('/hotel/info', methods=['GET'])
def get_hotel():
    # gu_receive 라는 변수에 전달받은 구 이름을 저장합니다.
    gu_receive = request.args.get('gu_give')
    # 구 이름에 해당하는 모든 맛집 목록을 불러옵니다.
    matjip_list = list(db.matjip.find({'area': gu_receive}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/attraction/info', methods=['GET'])
def get_attraction():
    # gu_receive 라는 변수에 전달받은 구 이름을 저장합니다.
    gu_receive = request.args.get('gu_give')
    # 구 이름에 해당하는 모든 맛집 목록을 불러옵니다.
    attraction_list = list(db.attraction.find({'area': gu_receive}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'attraction_list': attraction_list})

@app.route('/restaurant/info', methods=['GET'])
def get_restaurant():
    # gu_receive 라는 변수에 전달받은 구 이름을 저장합니다.
    gu_receive = request.args.get('gu_give')
    # 구 이름에 해당하는 모든 맛집 목록을 불러옵니다.
    restaurant_list = list(db.restaurant.find({'area': gu_receive}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'restaurant_list': restaurant_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)