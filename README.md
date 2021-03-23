# pwm-controller
## これは何
JetsonNanoでラジコンカーのサーボモータとスロットル用のモータの制御をするプログラム

## ハードウェアの構成

本プログラムは以下のような構成のラジコンカーの制御をすることを前提としている
- サーボモータ: 3入力での制御をするもの(入力例:5V，PWM，GND)
- スロットル用モータ(モータドライバ): PWM, 方向指定入力(Dir)によって回転制御するもの(デバイス例: DROK DC 2-way H-Bridge Brush Motor Driver)
## How to use
### プログラムの起動
``` $ python3 server.py ```

### PWM制御
http://0.0.0.0:<Port>/<throttle|steer>/<0.0-1.0>
## config.iniについて
[Server]　<br>
- Port: サーバのポート

[Throttle] <br>
- PwmPin: スロットル用のモータ制御用PWMピンの番号
- Min/Max: PWMのDuty比．0-100%で指定
- DirectionPin: モータの回転方向を制御するピンの番号

[Steer] <br>
内容はThrottleと同じ
