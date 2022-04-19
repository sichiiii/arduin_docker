from flask import request, render_template
from main import SerialPortConnection
from database import SQL
from config import Configuration
from time import sleep
from app import app
import app_logger

config_path = './config.ini'
config = Configuration()
config.load(config_path)
arduino = SerialPortConnection()
logger = app_logger.get_logger(__name__)

sql = SQL()


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'GET':
            flats = sql.get_flats()
            return render_template('home.html', flats=flats)
        elif request.method == 'POST':
            max_weight = float(config.get('requirements', 'max_weight'))
            min_weight = float(config.get('requirements', 'min_weight'))
            weight = arduino.weight()
            logger.info(weight)
            logger.info('Run conveer 1s')
            arduino.conveer1s()
            arduino.conveer1s()
            arduino.conveer1s()
            arduino.conveer1s()
            arduino.conveer1s()
            sleep(2)
            if (weight < max_weight) and (weight > min_weight):
                logger.info(f'Weight min:{min_weight}, current:{weight}, max:{max_weight}')
                check = arduino.check()
                logger.info(f'Check:{check}')
                if check == 1 or check == '1':
                    flat = request.form['flat_button']
                    logger.info('Run conveer 3.5s')
                    arduino.conveer()
                    sleep(3.5)
                    # arduino.ejection()
                    logger.info('Run blade 5s')
                    arduino.blade()
                    sql.add_bottle(flat)
                    return render_template('index.html', title='Измельчение', json='Операция успешна')
                else:
                    logger.info(f'Weight min:{min_weight}, current:{weight}, max:{max_weight}')
                    arduino.escape()
                    return render_template('index.html', title='Измельчение', json='Бутылка отсуствует!')
            elif weight < 0.015:
                logger.info(f'Weight min:{min_weight}, current:{weight}, max:{max_weight}')
                arduino.escape()
                return render_template('index.html', title='Измельчение', json='Бутылка отсуствует!')
            else:
                # logger.info('Run conveer 1s')
                # arduino.conveer1s()
                # time.sleep(1)
                logger.info('Run ejection')
                arduino.escape()
                return render_template('index.html', title='Измельчение', json='Слишком большой вес!')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))


@app.route("/export", methods=['GET', 'POST'])
def export():
    try:
        sql.export()
        return render_template('index.html', title='Экспорт', json='Операция успешна')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))


@app.route("/update_flats", methods=['GET'])
def update_flats():
    try:
        start = config.get('house', 'start')
        end = config.get('house', 'end')
        sql.update_flats(int(start), int(end) + 1)
        return render_template('index.html', title='Добавление квартир', json='Операция успешна')
    except Exception as ex:
        logger.error(str(ex))


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
            return render_template('json.html', json=result, title='Резак')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))


@app.route("/ejection", methods=['GET', 'POST'])
def ejection():
    try:
        sleep(1)
        result = arduino.escape()
        if result['status'] == 'ok':
            result = 'Операция успешна'
        else:
            result = 'Операция не проведена'
        if request.method == 'GET':
            return render_template('json.html', json=result, title='Выброс')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))


@app.route("/weight", methods=['GET', 'POST'])
def weight():
    try:
        sleep(1)
        result = arduino.weight()
        return render_template('json.html', json=str(result) + ' грамм', title='Вес')
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))


@app.route("/check", methods=['GET', 'POST'])
def check():
    try:
        sleep(1)
        result = arduino.check()
        if result == 1 or result == "1":
            result = 'Бутылка в аппарате'
        else:
            result = 'Бутылка отсутствует'
        if request.method == 'GET':
            return render_template('json.html', json=result, title='Наличие')
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
            return render_template('json.html', json=result, title='Стоп')
        return result
    except Exception as ex:
        logger.error(str(ex))
        return render_template('error.html', text=str(ex))
