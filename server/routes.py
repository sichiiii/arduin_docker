from random import weibullvariate
from typing import Text
from flask import request, json, render_template, redirect, url_for, flash
from app import app
from main import SerialPortConnection
from config import Configuration
from time import sleep

import app_logger

config_path = './config.ini'
config = Configuration()
config.load(config_path)
arduino = SerialPortConnection()
logger = app_logger.get_logger(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        sleep(1)
        max_weight = float(config.get('requirements', 'max_weight'))
        weight = arduino.weight()
        print(weight)
        if weight < max_weight:  # поменять макс. вес в конфиге
            arduino.ejection()
            sleep(1)  # поменять таймер между операциями
            arduino.blade()
            return render_template('index.html',  title = 'Измельчение', json='Операция успешна')
        elif weight < 10:
            return render_template('index.html', title = 'Измельчение', json='Бутылка отсуствует!')
        else:
            return render_template('index.html', title = 'Измельчение', json='Слишком большой вес!')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/remoter", methods=['GET', 'POST'])
def remoter():
    try:
        sleep(1)
        return render_template('remoter.html')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/conveer", methods=['GET', 'POST'])
def conveer():
    try:
        sleep(1)
        result = arduino.conveer()
        if result['status'] == 'ok':
            result = 'Операция успешна'
        else:
            result = 'Операция не проведена'
        return render_template('json.html', json=result)
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/blade", methods=['GET', 'POST'])
def blade():
    try:
        sleep(1)
        result = arduino.blade()
        if result['status'] == 'ok':
            result = 'Операция успешна'
        else:
            result = 'Операция не проведена'
        if request.method == 'GET':
            return render_template('json.html', json=result, title = 'Резак')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/ejection", methods=['GET', 'POST'])
def ejection():
    try:
        sleep(1)
        result = arduino.ejection()
        if result['status'] == 'ok':
            result = 'Операция успешна'
        else:
            result = 'Операция не проведена'
        if request.method == 'GET':
            return render_template('json.html', json=result, title = 'Выброс')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/weight", methods=['GET', 'POST'])
def weight():
    try:
        sleep(1)
        result = arduino.weight()
        return render_template('json.html', json=str(result)+' грамм', title = 'Вес')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/check", methods=['GET', 'POST'])
def check():
    try:
        sleep(1)
        result = arduino.check()
        if result == "True":
            result = 'Бутылка в аппарате'
        else:
            result = 'Бутылка отсутствует'
        if request.method == 'GET':
            return render_template('json.html', json=result, title = 'Наличие')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/stop", methods=['GET', 'POST'])
def stop():
    try:
        sleep(1)
        result = arduino.stop()
        if result['status'] == 'ok':
            result = 'Операция успешна'
        else:
            result = 'Операция не проведена'
        if request.method == 'GET':
            return render_template('json.html', json=result, title = 'Стоп')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))
