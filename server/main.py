import app_logger
import json
import serial

from config import Configuration

config_path = './config.ini'


class SerialPortConnection:
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
            data = '1'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}

    def blade(self):
        try:
            data = '3'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}

    def conveer1s(self):
        try:
            data = '2'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}

    def escape(self):
        try:
            data = '4'
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            return {'status': 'ok'}
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}

    def weight(self):
        try:
            data = self.ser.readline().decode("utf-8")
            final_string = ''
            for i in data:
                final_string = final_string + i
            final = final_string[:-2].split(',')
            self.logger.info(f'final_string:{final_string}; final:{final}')
            return float(final[1])
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status': 'error'}

    def check(self):
        try:
            data = self.ser.readline().decode("utf-8")
            final_string = ''
            for i in data:
                final_string = final_string + i
            final = final_string[:-2].split(',')
            self.logger.info(f'final_string:{final_string}; final:{final}')
            return final[0]
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
