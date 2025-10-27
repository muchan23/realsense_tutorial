import pyrealsense2 as rs
import numpy as np
import time

# RealSenseパイプラインを作成
pipeline = rs.pipeline()
config = rs.config()

# ラズパイ向けの設定（解像度とフレームレートを下げる）
# ラズパイの処理能力を考慮して、より軽い設定に
config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 15)  # 解像度とフレームレートを下げる

# ストリーミング開始
pipeline.start(config)

try:
    print("ラズパイ用深度情報取得開始...")
    print("解像度: 320x240, フレームレート: 15fps")
    print("(Ctrl+Cで停止)")
    
    frame_count = 0
    start_time = time.time()
    
    for i in range(20):  # 20フレーム分のデータを取得
        # フレームを待機
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        if not depth_frame:
            print("深度フレームが取得できませんでした")
            continue
        
        frame_count += 1
        
        # 深度データをnumpy配列に変換
        depth_image = np.asanyarray(depth_frame.get_data())
        
        # ラズパイ向けの軽量な分析
        if frame_count % 5 == 0:  # 5フレームごとに情報表示（処理負荷軽減）
            print(f"\n--- フレーム {frame_count} ---")
            print(f"深度画像サイズ: {depth_image.shape}")
            
            # 有効な深度値のみを分析（0と65535を除外）
            valid_depths = depth_image[(depth_image > 0) & (depth_image < 10000)]
            
            if len(valid_depths) > 0:
                print(f"有効な深度値の数: {len(valid_depths)}")
                print(f"最小深度: {valid_depths.min()} mm")
                print(f"最大深度: {valid_depths.max()} mm")
                print(f"平均深度: {valid_depths.mean():.1f} mm")
                
                # 中央点の深度値を取得
                center_y, center_x = depth_image.shape[0] // 2, depth_image.shape[1] // 2
                center_depth = depth_image[center_y, center_x]
                print(f"中央点の深度: {center_depth} mm")
            else:
                print("有効な深度データがありません")
        
        # ラズパイの処理負荷を考慮して少し待機
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n停止しました")
except Exception as e:
    print(f"エラーが発生しました: {e}")
finally:
    pipeline.stop()
    end_time = time.time()
    print(f"パイプラインを停止しました")
    print(f"実行時間: {end_time - start_time:.2f}秒")
    print(f"処理フレーム数: {frame_count}")