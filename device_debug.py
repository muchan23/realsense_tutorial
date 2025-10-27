import pyrealsense2 as rs
import numpy as np

print("=== RealSense Device Debug ===")

try:
    # コンテキストを作成
    ctx = rs.context()
    
    # デバイス一覧を取得
    devices = ctx.query_devices()
    
    print(f"Found {len(devices)} device(s)")
    
    if len(devices) == 0:
        print("❌ No RealSense devices found!")
        print("\nTroubleshooting steps:")
        print("1. Check USB connection (use data cable, not charging cable)")
        print("2. Try different USB port")
        print("3. Check if device is powered on")
        print("4. Run: lsusb | grep -i intel")
        exit(1)
    
    # 各デバイスの情報を表示
    for i, device in enumerate(devices):
        print(f"\n--- Device {i} ---")
        print(f"Name: {device.get_info(rs.camera_info.name)}")
        print(f"Serial: {device.get_info(rs.camera_info.serial_number)}")
        print(f"Firmware: {device.get_info(rs.camera_info.firmware_version)}")
        
        # センサー情報を取得
        sensors = device.query_sensors()
        print(f"Sensors: {len(sensors)}")
        
        for j, sensor in enumerate(sensors):
            print(f"  Sensor {j}: {sensor.get_info(rs.camera_info.name)}")
            
            # ストリームプロファイルを取得
            profiles = sensor.get_stream_profiles()
            print(f"    Stream profiles: {len(profiles)}")
            
            for k, profile in enumerate(profiles):
                if profile.stream_type() == rs.stream.depth:
                    print(f"      Depth Profile {k}:")
                    print(f"        Resolution: {profile.as_video_stream_profile().width()}x{profile.as_video_stream_profile().height()}")
                    print(f"        Format: {profile.format()}")
                    print(f"        FPS: {profile.as_video_stream_profile().fps()}")
                elif profile.stream_type() == rs.stream.color:
                    print(f"      Color Profile {k}:")
                    print(f"        Resolution: {profile.as_video_stream_profile().width()}x{profile.as_video_stream_profile().height()}")
                    print(f"        Format: {profile.format()}")
                    print(f"        FPS: {profile.as_video_stream_profile().fps()}")

    # パイプラインを作成してテスト
    print(f"\n=== Testing Pipeline ===")
    pipeline = rs.pipeline()
    config = rs.config()
    
    # 利用可能な深度プロファイルを確認
    depth_profiles = []
    for sensor in sensors:
        profiles = sensor.get_stream_profiles()
        for profile in profiles:
            if profile.stream_type() == rs.stream.depth:
                depth_profiles.append(profile)
    
    if not depth_profiles:
        print("❌ No depth profiles available!")
        exit(1)
    
    # 最初の深度プロファイルを使用
    first_depth_profile = depth_profiles[0]
    print(f"Using depth profile: {first_depth_profile.as_video_stream_profile().width()}x{first_depth_profile.as_video_stream_profile().height()} @ {first_depth_profile.as_video_stream_profile().fps()}fps")
    
    # 設定を追加
    config.enable_stream(rs.stream.depth, 
                        first_depth_profile.as_video_stream_profile().width(),
                        first_depth_profile.as_video_stream_profile().height(),
                        first_depth_profile.format(),
                        first_depth_profile.as_video_stream_profile().fps())
    
    # パイプラインを開始
    print("Starting pipeline...")
    pipeline.start(config)
    print("✅ Pipeline started successfully!")
    
    # 数フレーム取得してテスト
    for i in range(3):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if depth_frame:
            print(f"Frame {i+1}: Got depth frame {depth_frame.get_width()}x{depth_frame.get_height()}")
        else:
            print(f"Frame {i+1}: No depth frame")
    
    pipeline.stop()
    print("✅ Test completed successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # より詳細なエラー情報
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
