import RPi.GPIO as GPIO
import os
import time
from nc_py_api import Nextcloud

# GPIO 引腳設置
D0_PIN = 7
RELAY_PIN = 17

# Nextcloud 配置
nc_url = "http://192.168.123.51/nextcloud"
nc_user = "root"
nc_pw = "123456"
data_dir = "/home/LSA/testdata/"  # 請確保目錄已存在或程式會自動創建
if not os.path.exists(data_dir) :
    os.makedirs(data_dir)

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(D0_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial = GPIO.LOW)

# 登錄 Nextcloud
def login_to_nextcloud() :
    try :
        nc = Nextcloud(
            nextcloud_url = nc_url,
            nc_auth_user = nc_user,
            nc_auth_pass = nc_pw
        )
        print("成功登錄 Nextcloud。")
        return nc
    except Exception as e :
        print(f"登錄 Nextcloud 失敗: {e}")
        return None

# 上傳檔案到 Nextcloud
def upload_file(nc, file_path) :
    file_name = os.path.basename(file_path)
    remote_path = f"/testdata/{file_name}"
    try :
        with open(file_path, "rb") as file :
            nc.files.upload_stream(remote_path, file)
            print(f"成功上傳檔案 {file_name} 到 Nextcloud。")
            os.remove(file_path)  # 刪除本地檔案
    except Exception as e :
        print(f"上傳過程中發生錯誤: {e}")

print("系統啟動，開始土壤溼度監測。\n 按下 Ctrl + C 可跳出程式。")

def main() :
    nc = login_to_nextcloud()
    if not nc :
        return
    try :
        while True :  # 讀取感測器狀態
            if GPIO.input(D0_PIN) == GPIO.HIGH :
                print("土壤乾燥，啟用馬達澆水。")
                status = "乾燥"
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # 啟動馬達
            else :
                print("土壤濕潤，停止馬達澆水。")
                status = "濕潤"
                GPIO.output(RELAY_PIN, GPIO.LOW)  # 停止馬達
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            date = time.strftime("%Y-%m-%d")
            file_path = os.path.join(data_dir, f"{date}.txt")
            log = f"{timestamp}: {status}\n"
            print(log.strip())
            with open(file_path, "a") as file :
                file.write(log)
            with open(file_path, "r") as file : # 檢查是否需要上傳數據
                lines = file.readlines()
                if len(lines) >= 144 :  # 已經記錄滿一天的數據 ##########
                    print(f"開始上傳數據檔案 {file_path} 到 Nextcloud 中。")
                    upload_file(nc, file_path)
            time.sleep(600)  # 每 10 分鐘執行一次
    except KeyboardInterrupt :
        print("偵測到 Ctrl + C，終止程式中。")
    finally :
        GPIO.cleanup()

if __name__ == "__main__" :
    main()