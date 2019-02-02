# 電光掲示板
ラズパイ上で動かす

# What
- httpで受け取ったメッセージを電光掲示板に表示する
- 外部プログラムが定期的にニュースのRSSをHTTP POSTしてくる


# How
- 外部プログラム(show_news)をkickして電光掲示板に表示する


# 参考情報
というか全部これ  
https://github.com/hzeller/rpi-rgb-led-matrix



# 改造
- dequeue -> delete
- パラメータ詳細
  - 声ONOFF
  - 声その他params
  - 文字ONOFF
  - 文字その他params

