# -*- coding : utf-8 -*-
import time
import configparser
from flask import Flask

from pwm_controller import Steer
from pwm_controller import Throttle

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

steer_config = config['Steer']
steer = Steer(steer_config)

throttle_config = config['Throttle']
throttle = Throttle(throttle_config)

@app.route('/steer/<float:scale>/')
def update_steer_pwm(scale: float):
    text = "steer: %f" % scale
    steer.setScale(scale)
    return text

@app.route('/steer/-<float:scale>/')
def update_minus_steer_pwm(scale: float):
    text = "steer: %f" % -scale
    steer.setScale(-scale)
    return text

@app.route('/throttle/<float:scale>/')
def update_throttle_pwm(scale: float):
    text = "throttle: %f" % scale
    throttle.setScale(scale)
    return text

@app.route('/throttle/-<float:scale>/')
def update_minus_throttle_pwm(scale: float):
    text = "throttle: %f" % -scale
    throttle.setScale(-scale)
    return text

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=int(config['Server']['Port']))
    finally:
        import RPi.GPIO as gpio
        gpio.cleanup()
