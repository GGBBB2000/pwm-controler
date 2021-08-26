# -*- coding : utf-8 -*-
import time
import configparser
from flask import Flask

from pwm_controller import Steer
from pwm_controller import Throttle

##
# @file server.py
# @brief ネットワーク経由でPWM制御をするためのサーバプログラムです

app = Flask(__name__)

##
# コンフィグ解析用の変数。readメソッドに*.iniファイルを指定
config = configparser.ConfigParser()
config.read('config.ini')

steer_config = config['Steer']
steer = Steer(steer_config)

throttle_config = config['Throttle']
throttle = Throttle(throttle_config)

@app.route('/steer/<float:scale>/')
##
# @brief ステアリング制御用(右方向)の関数
# @details http://localhost.local:<PORT>/steer/<scale>/ の<scale>に値を設定して、httpリクエストを送ることで呼び出しされる関数。呼び出しに成功するとステアリング用に設定したGPIOピンから、PWM出力が行われる。
# @param[in] float scale ステアリングのスケール値を0.0~1.0(正面方向~右方向)で指定。
def update_steer_pwm(scale: float):
    text = "steer: %f" % scale
    steer.setScale(scale)
    return text

@app.route('/steer/-<float:scale>/')
##
# @brief ステアリング制御用(左方向)の関数
# @details http://localhost.local:<PORT>/steer/-<scale>/ の<scale>に値を設定して、httpリクエストを送ることで呼び出しされる関数。呼び出しに成功するとステアリング用に設定したGPIOピンから、PWM出力が行われる。
# @warning httpリクエストする際は, スケールの部分に"-"をつけるのを忘れないように
# @param[in] float scale ステアリングのスケール値を0.0~1.0(正面方向~左方向)で指定。
def update_minus_steer_pwm(scale: float):
    text = "steer: %f" % -scale
    steer.setScale(-scale)
    return text

@app.route('/throttle/<float:scale>/')
##
# @brief スロットル制御用(前進)の関数
# @details http://localhost.local:<PORT>/throttle/<scale>/ の<scale>に値を設定して、httpリクエストを送ることで呼び出しされる関数。呼び出しに成功するとスロットル用に設定したGPIOピン, 方向制御用のGPIOピンから、PWM出力が行われる。
# @param[in] float scale スロットルのスケール値を0.0~1.0(停止~前進)で指定。
def update_throttle_pwm(scale: float):
    text = "throttle: %f" % scale
    throttle.setScale(scale)
    return text

@app.route('/throttle/-<float:scale>/')
##
# @brief スロットル制御用(後進)の関数
# @details http://localhost.local:<PORT>/throttle/-<scale>/ の<scale>に値を設定して、httpリクエストを送ることで呼び出しされる関数。呼び出しに成功するとスロットル用に設定したGPIOピン, 方向制御用のGPIOピンから、PWM出力が行われる。
# @warning httpリクエストする際は, スケールの部分に"-"をつけるのを忘れないように
# @param[in] float scale スロットルのスケール値を0.0~1.0(停止~後進)で指定。
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
