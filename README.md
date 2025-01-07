# LSA_waterplant_LazyFarmer

## Concept Development
有一位農夫日日夜夜辛勤的在田間耕種，但是人工種植的方式費時又費力，<br>
農夫也想要子早點下班去打Game, 追劇，所以突發奇想使用 Raspberry Pi3<br>
加上土壤濕度檢測器和澆水馬達，製作出一套全自動的植物澆水系統。<br>
透過樹梅派主機上的Python程式設定每十分鐘偵測和讀取當前植物所在土壤的<br>
乾濕度，並判斷在乾燥時澆水。同時將一整天的澆水次數和乾濕度數據紀錄<br>
並上傳到用Nextcloud建立的雲端資料庫，農夫便能在家就能隨時用手機查看<br>
植物的生長狀況 => 於是便能偷懶-躺著賺錢


## Implementation Resources
* Raspberry Pi3 x1(本課助教提供)
* 土壤濕度檢測器 x1(自行購買)
* 澆水馬達      x1(自行購買)
* 繼電器        x1(自行購買)
* 受試植物      x1(~~自願~~自備)
* 寶特瓶        x1(自備)
* 電焊槍        x1(管237 Moli實驗室借用)

## Existing Library/Software
<details> 
<summary><h3> Nextcloud </h3></summary> 
以下是NextCloud的安裝步驟:<br>
1. <strong>更新</strong><br> <i>$ sudo apt-get update && sudo apt-get upgrade</i> <br><br>
2. <strong>安裝Apache2 和 PHP</strong><br> 
  <i>$ sudo apt-get install apache2 -y</i> <br>
  <i>$ sudo apt-get install php</i><br><br>
3. <strong>安裝 NextCloud</strong><br>
  <i>$ cd /**var**/www/html</i><br>
  <i>$ curl https://download.nextcloud.com/server/releases/nextcloud-18.0.3.tar.bz2 | sudo tar -jxv</i><br><br>
4. <strong>建立同步資料夾</strong><br>
  <i>$ sudo mkdir -p /var/www/html/nextcloud/data</i><br>
  <i>$ sudo chown -R www-data:www-data /var/www/html/nextcloud/</i><br>
  <i>$ sudo chmod 750 /var/www/html/nextcloud/data </i><br><br>
5. <strong>用瀏覽器打開Nextcloud管理介面，設定帳號密碼</strong>
</details>
<br>

## Implementation Process

![messageImage_1736182405846](https://github.com/user-attachments/assets/dd6b0101-8aa3-4784-af23-bbdab0acef1a)
### 1.硬體電路:
1. 將土壤濕度檢測器接上Pi的3V3 power, GROUND, GPIO 7(CE1) 腳位
2. 將繼電器接上Pi的5V power, GROUND, GPIO 17 腳位
3. 將澆水馬達的正極接上繼電器/負極接上Pi的GROUND 腳位
4. 由於馬達的接口是裸線設計，所以我們使用電焊槍將裸線與杜邦線針腳焊接固定

### 2.軟體程式:
![messageImage_1735751484024](https://github.com/user-attachments/assets/c662a6f7-cf59-4dbb-9249-74078d3a4894)
1. 首先在Pi中創建nc_getsoil.py程式檔，並import RPi.GPIO 和 Nextcloud => 完成初始化設定
2. 在def main()中，透過感測器回傳的高低電壓判斷土壤是濕潤或乾燥，並同時決定是否開啟馬達
3. 由於過量的澆水也會導致植物掛掉，所以我們設定每10分鐘偵測土壤濕度，每次澆水5秒鐘
4. 當資料筆數達到144筆(也就是剛好過完一天時)就將資料上傳到Nextcloud的共享資料夾同步
5. 接著定義login_to_nextcloud()函式，判斷是否成功登入Nextcloud
6. 最後在upload_file()函式將資料nc以.txt檔上傳至指定路徑file_path，並刪掉樹梅派上記錄檔(避免佔用空間)

## Knowledge from Lecture
* 查詢Host-Server IP: ip addr show
* 更改目錄的所有者: sudo chown
* 更改目錄的權限:sudo chmod
* Raspberry Pi3 的針腳, 構造知識
* 使用vim在Pi中編輯Python程式碼

## Installation
1. 將土壤濕度感測器插入植物種植的土壤中
2. 準備一個寶特瓶大小的容器裝水
3. 將澆水馬達放入裝水的容器內並接上軟管，另一端則通向植物
4. 依照上方指示在樹梅派上安裝Nextcloud
5. 透過外接式螢幕或個人電腦用PUTTY打開樹梅派命令列
6. 成品應如下圖範例所示
   ![S__14868539](https://github.com/user-attachments/assets/3b219268-8202-4f5e-a946-973e645df686)

## Usage
1. 確認安裝過程無誤
2. 在樹梅派命令列執行nc_getsoil.py
3. 接著澆水系統便會自動運行
4. ~~可以開始放心偷懶~~

## Job Assignment
* 組長:  梁灝   [寫程式]+[上台報告]
* 組員1: 陳彥熏 [簡報製作]+[上台報告]
* 組員2: 黃士瀚 [硬體線路連接]
* 組員3: 王瑞呈 [主題構想]+[材料購買]
* 組員4: 陳厚駪 [寫程式]

## References
1. https://absorbed-toaster-205.notion.site/NextCloud-16e29288588080b7acd2da254b46425a
2. [學長姐報告](https://github.com/NCNU-OpenSource/WaterPlant)
3. [在Raspberry pi安裝Nextcloud](https://atceiling.blogspot.com/2020/03/raspberry-pi-70-nextcloud-talk.html#google_vignette)
4. [How to Setup a Raspberry Pi Nextcloud Server](https://pimylifeup.com/raspberry-pi-nextcloud-server/)
5. [安裝Apache Web Server及PHP](https://atceiling.blogspot.com/2020/03/raspberry-pi-60apache-web-serverphp.html)
6. [焊接電子電路](https://www.youtube.com/watch?v=UUIHBjsaMeM&ab_channel=%E9%BB%83%E4%BF%A1%E6%83%A0%E7%9A%84%E7%98%8B%E7%8B%82%E6%95%99%E5%AE%A4)
7. [Arduino控制微型水泵(繼電器模組)](https://www.youtube.com/watch?v=V3daz51JeoE&ab_channel=%E5%90%B3%E6%9F%8F%E5%BB%B7)
