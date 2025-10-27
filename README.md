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

### 1. システムの更新
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 2. 必要なライブラリのインストール
```bash
# 基本パッケージ
sudo apt install python3-pip python3-dev python3-numpy python3-opencv

# RealSense関連パッケージ
sudo apt install librealsense2-dkms librealsense2-utils librealsense2-dev
```

### 3. Pythonライブラリのインストール
```bash
pip3 install pyrealsense2 numpy opencv-python
```

### 4. GPU メモリの設定 (オプション)
```bash
# /boot/config.txt に追加
sudo nano /boot/config.txt

# 以下の行を追加
gpu_mem=128
```

## 📖 使用方法

### 基本的な深度情報の取得
```bash
python3 debug.py
```

### カラー + 深度画像の表示
```bash
python3 realsense_test.py
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
