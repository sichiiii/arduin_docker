from typing import Text
from flask import request, json, render_template, redirect, url_for, flash
from app import app
from main import SerialPortConnection
from config import Configuration

import app_logger

config_path = './config.ini'
config = Configuration()
config.load(config_path)
arduino = SerialPortConnection()
logger = app_logger.get_logger(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Загрузить':
                weight = float(arduino.weight())
                max_weight = float(config.get('requirements', 'max_weight'))
                if weight < max_weight:
                    arduino.conveer(1)
                    return render_template('index.html', text='ОПЕРАЦИЯ УСПЕШНА')
                elif weight < 10:
                    return render_template('index.html', text='Бутылка отсуствует!')
                else:
                    return render_template('index.html', text='Слишком большой вес!')
        return render_template('index.html', text='Положите бутылку в аппарат и нажмите кнопку')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/remoter", methods=['GET', 'POST'])
def remoter():
    try:
        return render_template('remoter.html')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/conveer", methods=['GET', 'POST'])
def conveer():
    try:
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
        result = arduino.weight()
        return render_template('json.html', json=str(result)+' грамм', title = 'Вес')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))

@app.route("/check", methods=['GET', 'POST'])
def check():
    try:
        result = arduino.check()
        if result == True:
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
