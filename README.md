# LSA_waterplant_LazyFarmer
## 目錄 
1. [簡介](#簡介)
2. [成員](#成員)
3. [使用設備](#使用設備)
4. [使用軟體](#使用軟體)
5. [製作過程](#製作過程)
6. [參考資料來源](#參考資料來源)

## 簡介 Itroduction:
有一位農夫日日夜夜辛勤的在田間耕種，但是人工種植的方式費時又費力，<br>
農夫也想要子早點下班去打Game, 追劇，所以突發奇想使用 Raspberry Pi3<br>
加上土壤濕度檢測器和澆水馬達，製作出一套全自動的植物澆水系統。<br>
透過樹梅派主機上的Python程式設定每十分鐘偵測和讀取當前植物所在土壤的<br>
乾濕度，並判斷在乾燥時澆水。同時將一整天的澆水次數和乾濕度數據紀錄<br>
並上傳到用Nextcloud建立的雲端資料庫，農夫便能在家就能隨時用手機查看<br>
植物的生長狀況 => 於是便能偷懶-躺著賺錢

## 成員 Team Member:
* 組長:  梁灝   [寫程式]+[上台報告]
* 組員1: 陳彥熏 [簡報製作]+[上台報告]
* 組員2: 黃士瀚 [硬體線路連接]
* 組員3: 王瑞呈 [主題構想]+[材料購買]
* 組員4: 陳厚駪 [寫程式]

## 使用設備 Hardware Implementation:
* Raspberry Pi3(本課助教提供)
* 土壤濕度檢測器(自行購買)
* 澆水馬達(自行購買)
* 繼電器(自行購買)
* 受試植物(~~自願~~自備)
* 電焊槍(管237 Moli實驗室借用)

## 使用軟體 Software Implementation:
* Nextcloud
  <br>

## 製作過程 Process

![messageImage_1736182405846](https://github.com/user-attachments/assets/dd6b0101-8aa3-4784-af23-bbdab0acef1a)
### 硬體電路:
1. 將土壤濕度檢測器接上Pi的3V3 power, GROUND, GPIO 7(CE1) 腳位
2. 將繼電器接上Pi的5V power, GROUND, GPIO 17 腳位
3. 將澆水馬達的正極接上繼電器/負極接上Pi的GROUND 腳位
4. 由於馬達的接口是裸線設計，所以我們使用電焊槍將裸線與杜邦線針腳焊接固定

### 軟體程式:
![messageImage_1735751484024](https://github.com/user-attachments/assets/c662a6f7-cf59-4dbb-9249-74078d3a4894)
1. 首先在Pi中創建nc_getsoil.py程式檔，並import RPi.GPIO 和 Nextcloud => 完成初始化設定
2. 在def main()中，透過感測器回傳的高低電壓判斷土壤是濕潤或乾燥，並同時決定是否開啟馬達
3. 由於過量的澆水也會導致植物掛掉，所以我們設定每10分鐘偵測土壤濕度，每次澆水5秒鐘
4. 當資料筆數達到144筆(也就是剛好過完一天時)就將資料上傳到Nextcloud的共享資料夾同步
5. 接著定義login_to_nextcloud()函式，判斷是否成功登入Nextcloud
6. 最後在upload_file()函式將資料nc以.txt檔上傳至指定路徑file_path，並刪掉樹梅派上記錄檔(避免佔用空間)

## 參考資料來源 References
https://absorbed-toaster-205.notion.site/NextCloud-16e29288588080b7acd2da254b46425a
[學長姐報告](https://github.com/NCNU-OpenSource/WaterPlant)
[]()
