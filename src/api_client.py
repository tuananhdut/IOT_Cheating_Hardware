import aiohttp
import asyncio
from config import SERVER_URL, RTMP_URL

# create camera (output:cameraId, linkingCode)
async def fetch_camera_register_data():
    url = f"{SERVER_URL}/camera/register"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    cameraId = data["cameraId"]
                    linkingCode = data["linkingCode"]
                    print("link code :", linkingCode)
                    return data
                else:
                    print(f"Error: Received status code {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e}")
        return None


# detect report
async def fetch_detection_report(camera_id, begin_time, end_time, sensitivity):
    url = f"{SERVER_URL}/detect/report"
    params = {
        "cameraId": camera_id,
        "beginTime": begin_time,
        "endTime": end_time,
        "sensitivity": sensitivity
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
                return await response.json()  # Trả về dữ liệu JSON
    except aiohttp.ClientError as e:
        print(f"An error occurred: {e.message}")
        return {"error": str(e)}

async def send_video_request(path, action_id):
    url = f"{SERVER_URL}/detect/video"
    params = {"actionId": action_id}
    
    try:
        with open(path, "rb") as video_file:
            files = {"file": video_file}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, params=params, data=files) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return f"Failed! Status code: {response.status}, Response: {await response.text()}"
    except FileNotFoundError:
        return "Error: File not found. Please check the file path."
    except Exception as e:
        return f"Error: {str(e)}"

# async def main():
#     camera_data = await fetch_camera_register_data()
#     print(camera_data)
    
#     # report = await fetch_detection_report("camera123", "2024-11-01", "2024-11-02", "high")
#     # print(report)
    
#     # video_response = await send_video_request("./test.mp4", "3e20dc25-751d-4951-b265-f1907ccf6b2e")
#     # print(video_response)

# # Chạy asyncio event loop
# if __name__ == "__main__":
#     asyncio.run(main())
