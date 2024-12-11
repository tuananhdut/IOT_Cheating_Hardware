import threading
import time
import subprocess
import cv2
import datetime
import pytz
from picamera2 import Picamera2
from config import RTMP_URL
import mediapipe as mp

picam2 = Picamera2()

mp_pose = mp.solutions.pose
pose_detector = mp_pose.Pose(static_image_mode=False, model_complexity=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

config = picam2.create_video_configuration(main={"size": (640, 480), "format": "YUV420"})
picam2.configure(config)
picam2.set_controls({"FrameDurationLimits": (66666, 66666)})  # 15 FPS
picam2.start()

timezone = pytz.timezone('Etc/GMT-7')
ffmpeg_cmd = [
    'ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'yuv420p',
    '-s', '640x480',
    '-r', '15',
    '-i', '-',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-tune', 'zerolatency',
    '-b:v', '1000k',
    '-bufsize', '500k',
    '-f', 'flv',
    RTMP_URL
]




# Tạo process để truyền dữ liệu qua FFmpeg
process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

def draw_datetime_to_frame(frame):
    current_time = datetime.datetime.now(pytz.utc).astimezone(timezone).strftime('%d-%m-%Y %H:%M:%S')
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.5
    font_color = (255, 255, 255)
    font_thickness = 1
    (text_width, text_height), _ = cv2.getTextSize(current_time, font, font_scale, font_thickness)
    top_left_corner_x = 0
    top_left_corner_y = 0
    bottom_right_corner_x = top_left_corner_x + text_width + 4
    bottom_right_corner_y = top_left_corner_y + text_height + 4
    cv2.rectangle(frame, (top_left_corner_x, top_left_corner_y), (bottom_right_corner_x, bottom_right_corner_y), (0, 0, 0), -1)
    text_x = top_left_corner_x + 2
    text_y = bottom_right_corner_y - 2
    cv2.putText(frame, current_time, (text_x, text_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    return frame

def extract_pose_landmarks(frame):
    # Chuyển đổi khung hình sang RGB cho MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Phát hiện các đặc trưng trên cơ thể
    results = pose_detector.process(rgb_frame)
    
    # Nếu có phát hiện các khớp cơ thể, vẽ các điểm đặc trưng
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)  # Vẽ các điểm đặc trưng lên cơ thể
    
    return frame

def write_to_ffmpeg():
    while True:
        frame = picam2.capture_array("main")
        frame = draw_datetime_to_frame(frame)
        frame = extract_pose_landmarks(frame)
        # cv2.imshow('Camera', frame)
        process.stdin.write(frame.tobytes())  # Ghi dữ liệu vào FFmpeg

def run():
    thread = threading.Thread(target=write_to_ffmpeg, daemon=True)
    thread.start()

    try:
        while True:
            # frame = picam2.capture_array("main")
            # frame = draw_datetime_to_frame(frame)
            # cv2.imshow('Camera', frame)

            # Thoát khi nhấn 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Stream ended.")
    finally:
        picam2.close()
        process.stdin.close()
        process.wait()
        cv2.destroyAllWindows()
