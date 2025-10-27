# RealSense Tutorial for Raspberry Pi

ラズパイでIntel RealSenseカメラを使用するためのチュートリアルです。

## 📋 目次

- [必要なもの](#必要なもの)
- [セットアップ](#セットアップ)
- [使用方法](#使用方法)
- [ファイル説明](#ファイル説明)
- [トラブルシューティング](#トラブルシューティング)
- [パフォーマンス最適化](#パフォーマンス最適化)

## 🔧 必要なもの

### ハードウェア
- Raspberry Pi 4 (推奨) または Raspberry Pi 3B+
- Intel RealSense カメラ (D435, D435i, D415等)
- microSDカード (32GB以上推奨)
- USB 3.0ケーブル (データ転送対応)
- 外部電源アダプター (5V 3A以上推奨)

### ソフトウェア
- Raspberry Pi OS (64-bit推奨)
- Python 3.7以上

## 🚀 セットアップ

> **参考**: このセットアップ手順は [Raspberry Pi 4 and Intel RealSense D435](https://github.com/datasith/Ai_Demos_RPi/wiki/Raspberry-Pi-4-and-Intel-RealSense-D435) を参考にしています。

### 1. システムの更新と依存関係のインストール
```bash
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install automake libtool vim cmake libusb-1.0-0-dev libx11-dev xorg-dev libglu1-mesa-dev python3-pip python3-dev python3-numpy
```

### 2. ファイルシステムの拡張
```bash
sudo raspi-config
# Advanced Options → Expand filesystem → Yes → Reboot
```

### 3. スワップサイズの増加
```bash
# /etc/dphys-swapfile を編集
sudo vi /etc/dphys-swapfile
# CONF_SWAPSIZE=2048 に変更

# 変更を適用
sudo /etc/init.d/dphys-swapfile restart
swapon -s
```

### 4. RealSense udevルールの設定
```bash
cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/

# udevルールを適用
sudo su
udevadm control --reload-rules && udevadm trigger
exit
```

### 5. 環境変数の設定
```bash
# ~/.bashrc に追加
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib' >> ~/.bashrc
source ~/.bashrc
```

### 6. protobufのインストール
```bash
cd ~
git clone --depth=1 -b v3.10.0 https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j1
sudo make install
cd python
export LD_LIBRARY_PATH=../src/.libs
python3 setup.py build --cpp_implementation 
python3 setup.py test --cpp_implementation
sudo python3 setup.py install --cpp_implementation
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3
sudo ldconfig
```

### 7. Intel TBBライブラリのインストール
```bash
cd ~
wget https://github.com/PINTO0309/TBBonARMv7/raw/master/libtbb-dev_2018U2_armhf.deb
sudo dpkg -i ~/libtbb-dev_2018U2_armhf.deb
sudo ldconfig
rm libtbb-dev_2018U2_armhf.deb
```

### 8. librealsenseのビルドとインストール
```bash
cd ~/librealsense
mkdir build && cd build
cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=Release -DFORCE_LIBUVC=true
make -j1
sudo make install
```

### 9. pyrealsense2 Pythonバインディングのインストール
```bash
cd ~/librealsense/build
cmake .. -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=$(which python3)
make -j1
sudo make install
```

### 10. OpenGLの設定
```bash
# OpenGLのインストール
sudo apt-get install python-opengl
sudo -H pip3 install pyopengl
sudo -H pip3 install pyopengl_accelerate==3.1.3rc1

# OpenGLドライバーの有効化
sudo raspi-config
# "7. Advanced Options" → "A8 GL Driver" → "G2 GL (Fake KMS)"
```

### 11. GPU メモリの設定 (オプション)
```bash
# /boot/config.txt に追加
sudo nano /boot/config.txt
# gpu_mem=128 を追加
```

## 📖 使用方法

### 仮想環境のアクティベート
スクリプトを実行する前に、必ず仮想環境をアクティベートしてください：

```bash
# 仮想環境をアクティベート
source ./realsense_env/bin/activate

# アクティベートされたことを確認（プロンプトに (realsense_env) が表示される）
(realsense_env) murakami@raspberrypi:~/realsense_tutorial $
```

### 基本的な深度情報の取得
```bash
# 仮想環境をアクティベート後
python3 debug.py
```

### カラー + 深度画像の表示
```bash
# 仮想環境をアクティベート後
python3 realsense_test.py
```

### 仮想環境の非アクティベート
作業が終わったら、仮想環境を非アクティベートできます：

```bash
deactivate
```

## 📁 ファイル説明

### `debug.py`
- **目的**: 深度情報の基本的な取得と分析
- **特徴**: ラズパイ向けに最適化（低解像度、低フレームレート）
- **出力**: 深度値の統計情報（最小値、最大値、平均値等）

### `realsense_test.py`
- **目的**: カラー画像と深度画像の同時表示
- **特徴**: OpenCVを使用したリアルタイム表示
- **操作**: 'q'キーで終了

## 🔍 トラブルシューティング

### RealSenseが認識されない場合

#### 1. USB接続の確認
```bash
# USBデバイスの確認
lsusb | grep -i intel
```

#### 2. デバイス情報の確認
```bash
# RealSenseデバイスの詳細情報
rs-enumerate-devices
```

#### 3. 権限の確認
```bash
# udevルールの確認
ls -la /dev/video*
```

### パフォーマンスが悪い場合

#### 1. 温度の確認
```bash
# CPU温度を監視
watch -n 1 vcgencmd measure_temp
```

#### 2. CPU使用率の確認
```bash
# システムリソースの監視
htop
```

#### 3. 解像度の調整
`debug.py`の設定を変更：
```python
# より低い解像度に変更
config.enable_stream(rs.stream.depth, 160, 120, rs.format.z16, 10)
```

## ⚡ パフォーマンス最適化

### 推奨設定

#### 解像度とフレームレート
- **軽量**: 160x120, 10fps
- **標準**: 320x240, 15fps
- **高品質**: 640x480, 30fps (ラズパイ4推奨)

#### システム設定
```bash
# CPU ガバナーの設定
echo 'performance' | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# GPU メモリの確保
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt
```

### 電源管理
- 外部電源アダプターの使用を強く推奨
- USBハブ経由での電源供給も可能
- バッテリー使用時は解像度を下げる

## 📊 期待される出力例

### debug.py の出力
```
ラズパイ用深度情報取得開始...
解像度: 320x240, フレームレート: 15fps

--- フレーム 5 ---
深度画像サイズ: (240, 320)
有効な深度値の数: 65000
最小深度: 200 mm
最大深度: 5000 mm
平均深度: 1200.5 mm
中央点の深度: 1150 mm
```

## 🆘 よくある問題

### Q: "No module named 'pyrealsense2'" エラー
A: librealsense2が正しくインストールされていない可能性があります。
```bash
sudo apt install librealsense2-dev
pip3 install pyrealsense2
```

### Q: フレームレートが低い
A: 解像度を下げるか、フレームレートを調整してください。
```python
config.enable_stream(rs.stream.depth, 160, 120, rs.format.z16, 10)
```

### Q: カメラが認識されない
A: USBケーブルとポートを確認し、外部電源を使用してください。

## 📚 参考資料

- [Intel RealSense SDK 2.0 Documentation](https://github.com/IntelRealSense/librealsense)
- [Raspberry Pi Official Documentation](https://www.raspberrypi.org/documentation/)
- [OpenCV Python Documentation](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

バグ報告や機能追加の提案は、GitHubのIssuesページでお願いします。
