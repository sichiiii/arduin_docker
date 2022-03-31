import serial, app_logger, json
from config import Configuration
from time import sleep


config_path = './config.ini'


class SerialPortConnection():
    def __init__(self):
        self.config = Configuration()
        self.config.load(config_path)
        self.params = self.config.get('arduino', 'params')
        self.port_name = self.config.get('arduino', 'port')
        self.baudrate = self.config.get('arduino', 'baudrate')
        self.pause = self.config.get('arduino', 'pause')
        self.ser = serial.Serial(self.port_name, self.baudrate, timeout=int(self.pause)) 
        self.logger = app_logger.get_logger(__name__) 


    def conveer(self):
        try:
            data = 'conveer'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status':'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}


    def blade(self):
        try:
            data = 'blade'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}


    def ejection(self):
        try:
            data = 'escape'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}


    def weight(self):
        try:
            data = self.ser.readline().decode("utf-8")
            final_string = ''
            for i in data:
                final_string = final_string + i
                if i == '}':
                    break
            final = json.loads(final_string)
            return final['weight']
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}


    def check(self):
        try:
            data = self.ser.readline().decode("utf-8")
            final_string = ''
            for i in data:
                final_string = final_string + i
                if i == '}':
                    break
            final = json.loads(final_string)
            return final['check']
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}


    def stop(self):
        try:
            data = 'stop'
            data = json.dumps(data)
            self.ser.write(data.encode('ascii'))
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}


    def get_config_params(self):
        try:
            start = self.config.get('house', 'start')
            end = self.config.get('house', 'end')
            house_number = self.config.get('house', 'house_number')
            return start, end, house_number
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status:': 'error'}