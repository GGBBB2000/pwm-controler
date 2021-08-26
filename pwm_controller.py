# -*- coding : utf-8 -*-
import RPi.GPIO as gpio
from abc import *

##
# @file pwm_controller.py
# @brief PWM制御用の抽象クラスと、スロットル、ステアリング制御用クラス


##
# @class PWMController
# @brief PWM制御クラス作成用の抽象クラス
class PWMController(metaclass=ABCMeta):
    ##
    # PWM制御クラスの初期化
    # @details PWMの最大、最小値および出力ピンの設定を行う. それぞれの値はconfig.ini内の'Min'、'Max'、'PwmPin'パラメータによって変更する。
    def __init__(self, config):
        pwm_min = int(config['Min'])
        pwm_max = int(config['Max'])
        pin = int(config['PwmPin'])

        gpio.setmode(gpio.BOARD)
        gpio.setup(pin, gpio.OUT)

        self.current_value = 10.0
        self.pwm = gpio.PWM(pin, 60)
        self.pwm.start(0)
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max
        print("PIN=%d" % (pin), end=" ")
        print("MIN=%d" % (self.pwm_min), end=" ")
        print("MAX=%d" % (self.pwm_max), end=" ")
        print("")

    @abstractmethod
    def setScale(self, scale: float):
        """
        convert a scale(-1 to 1) to a duty cycle
        """
        pass

##
#@brief ステアリングPWM出力制御クラス
class Steer(PWMController):
    def __init__(self, config):
        print("Steer   :", end=" ")
        super().__init__(config)

    ##
    #@brief 受け取った-1.0~1.0のスケール値をPWMのdutyサイクルに変換する。
    #@warning 入力したスケール値の絶対値が1.0を上回った場合、値の絶対値が0になるように調整される。
    #@param float scale -1.0~1.0の小数値で指定
    def setScale(self, scale: float):
        if self.current_value == scale:
            return
        self.current_value = scale
        # -1 -> 1 to pwm_max -> pwm_min
        if scale > 1:
            scale = 1
        elif scale < -1:
            scale = -1
        scale_width = 2 # left to right -1 -> 1
        pwm_width = self.pwm_max - self.pwm_min
        upscale_ratio = pwm_width / scale_width
        duty = (scale + 1) * upscale_ratio + self.pwm_min
        self.pwm.ChangeDutyCycle(duty)
        print(duty)


##
#@brief スロットルPWM出力制御クラス
class Throttle(PWMController):
    def __init__(self, config):
        dir_pin = int(config['DirectionPin'])
        gpio.setmode(gpio.BOARD)
        gpio.setup(dir_pin, gpio.OUT)
        self.dir_pin = dir_pin
        print("Throttle:", end=" ")
        print("DIR_PIN=%d" % dir_pin, end=" ")

        super().__init__(config)

    ##
    #@brief 受け取った-1.0~1.0のスケール値をPWMのdutyサイクルに変換する.
    #@details config.ini内の'DirectionPin'で設定したピンに方向の出力と'PWM_PIN'で指定したピンにPWMを出力する
    #@warning 入力したスケール値の絶対値が1.0を上回った場合、値の絶対値が0になるように調整される。
    #@param  float scale -1.0~1.0の小数値で指定
    def setScale(self, scale: float):
        if self.current_value == scale:
            return
        self.current_value = scale
        dir_out = gpio.LOW
        if scale < 0:
            dir_out = gpio.HIGH
        scale = abs(scale)
        scale_width = 1 # forward(backward) 0 -> (-)1
        pwm_width = self.pwm_max - self.pwm_min
        upscale_ratio = pwm_width / scale_width
        duty = scale * upscale_ratio + self.pwm_min
        self.pwm.ChangeDutyCycle(duty)
        gpio.output(self.dir_pin, dir_out)
        print(duty)

#import time
#import configparser
#if __name__ == "__main__":
#    try:
#        config = configparser.ConfigParser()
#        config.read('config.ini')
#
#        steer_config = config['Steer']
#        steer = Steer(steer_config)
#
#        throttle_config = config['Throttle']
#        throttle = Throttle(throttle_config)
#
## test
#        steer.setScale(0)
#        time.sleep(1)
#        for i in range(2):
#            for offset in range(11):
#                steer.setScale(i - 1 + offset / 10)
#                time.sleep(0.2)
#
#        steer.setScale(0)
#        time.sleep(2)
#
#        #throttle.setScale(0)
#        #time.sleep(1)
#
#        #for i in range(1):
#        #    for offset in range(11):
#        #        throttle.setScale(i + offset / 10)
#        #        time.sleep(1)
#        #throttle.setScale(0)
#        #time.sleep(1)
#
#        #for i in range(1):
#        #    for offset in range(11):
#        #        throttle.setScale(-1 * (i + offset / 10))
#        #        time.sleep(1)
#        #throttle.setScale(0)
### test end
#
#    finally:
#        gpio.cleanup()
