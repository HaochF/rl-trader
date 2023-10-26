from flask import Flask, request
from flask import render_template
import requests
import time
import json
import jsonpickle
import funct_buyoffer
import funct_selloffer

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/get_offer_links/<item>/<morethan>/<lessthan>/<key>")
def get_subreddits(item, morethan, lessthan,  key):
    item = item.lower()
    with open('credits.json') as json_file1:
        global credit_list
        credit_list = json.load(json_file1)

    if key not in credit_list.keys():
        return jsonpickle.encode(['INVALID', 'INVALID'])

    output = [funct_buyoffer.get_buy_offers(item.replace('239483293', " "), int(morethan)), funct_selloffer.get_sell_offers(item.replace('239483293', " "), int(lessthan))]
    print(output)
    return jsonpickle.encode(output)

@app.route("/get_sell_offer_links/<item>/<lessthan>/<key>")
def get_subs(item, lessthan, key):
    item = item.lower()
    with open('/home/RFeng/rltrades/credits.json') as json_file1:
        global credit_list
        credit_list = json.load(json_file1)

    if key not in credit_list.keys():
        return jsonpickle.encode(['INVALID'])

    output = funct_selloffer.get_sell_offers(item.replace('239483293', " "), int(lessthan))
    print(output)
    return jsonpickle.encode(output)

if __name__ == "__main__":
    app.run()

