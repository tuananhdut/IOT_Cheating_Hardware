# cấu hình raspberry pi5
B1: update ban đầu cho raspberry  (putty)
- sudo apt update && sudo apt upgrade -y
- thêm các biến môi trường vào
B2: bật vnc
- sudo raspi-config
- interface option => VCN => Yes
B3: Liên kết với vs code
- cài extention: remote ssh
- (nếu có liên kết trước đó)  xóa key: ssh-keygen -R 192.168.46.198
- vào ssh: ssh admin@192.168.46.198
B4: cài thư viện cần thiết để chạy python
- lỗi không nhận thư viên nên chạy trực tiếp không sử dụng venv
B5: cấu hình rtmp
- sudo systemctl start nginx
- libcamera-vid -t 0 --inline --width 640 --height 480 --framerate 15 --codec yuv420 -o - | ffmpeg -fflags nobuffer -f rawvideo -pix_fmt yuv420p -s 640x480 -i - -c:v libx264 -preset veryfast -tune zerolatency -g 30 -b:v 1500k -f flv rtmp://192.168.46.198/live/stream1
- pip install mediapipe --break-system-packages

# Cấu hình chạy code
- chú ý: raspberry không nhận diện thư viện libcamera
B1: Cài các biến môi trường
- tạo file .env
- SERVER_URL, RTMP_URL, TOKEN 
B2: chạy code
- python -m src.main