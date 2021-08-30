# Accounting System with PostegreSQL

## Contents

- [簡介](#簡介)
- [使用軟體](#使用軟體)
- [URL](#URL)
- [API spec](#API-spec)
- [DB index](#DB-index)
- [心得](#心得)

## 簡介

從帳務資料取出所需統整資訊：usage amount, cost, reserved instance

## 使用軟體
- Visual Studio Code
- Jupyter Lab
- PostgreSQL 13
- GitHub
- Heroku (include Heroku Postgres)

## URL
- GitHub repo URL
    - https://github.com/yali860208/aws-bill-test
- Heroku app URL (開啟網頁可能需要數十秒的 heroku 開機時間)
    - https://test-bill.herokuapp.com/

## API spec
推薦測試 ID
Usage Account ID :504119000000
Subscription ID :3107027728
|Route|HTML file|Parameters|
|-|-|-|
|/|index.html||
|/cost|cost.html|uid=(在index中 cost 框輸入的 Usage Account ID ) |
|/amount|amount.html|uid_am=(在index中 amount 框輸入的 Usage Account ID )|
|/amountproduct|amountproduct.html|uid_pro=(在amount中 product 框輸入的 product)|
|/risid|risid.html|uid_sid=(在index中RI框輸入的 Usage Account ID)|
|/risidinfo|risidinfo.html|sid_info=(在index或risid中Subscription ID框輸入的 Subscription ID )|
 

|Route|說明|
|-|-|
|/|可輸入想查詢的 Usage Account ID 或 Subscription ID|
|/cost|列出各 Product 的總 cost 和佔比圓餅圖|
|/amount|列出各 Product 的開始時間和各日期總 amount，若有 instance 大小差異則列出 normalized amount|
|/amountproduct|列出此ID中此 Product 的 amount 和長條圖|
|/risid|列出此 Account ID 使用的 Reserved Instance 的 Subscription ID 和基本資訊|
|/risidinfo|列出此 Subscription ID 的詳細資訊、不同機器大小使用資訊和圓餅圖|
    
## DB index
> 增加 Usage Account ID 和 Subscription ID 加快索引速度

![](https://i.imgur.com/72cJTU4.png)

## 心得
面試完給自己幾個目標在一個月內完成
1. 把半成品的面試作業改進
    - 成功將 Flask 部屬至 Heroku 並使用 Heroku Postgres
    - 增加圖表 : pie chart、bar plot
    - 研究更多 AWS billing 欄位 : 尤其是 Reservation
    - 更站在 user 角度思考 : 介面設計、需要哪些資訊等...
3. 將資料結構複習並用 Python 實作 (時間.空間複雜度、Tree、Graph、Linked List、Stack、Sort、Search等...)
    - https://github.com/yali860208/DS-practice.git
4. 心得 :
    為自己上次交出的半成品感到慚愧，這次花最多時間的地方是資料分析，了解每個欄位跟其他欄位的關係，例如 : 每筆 reservation 的 subscription ID都有一筆 RIFee 資料，紀錄 reserve 的量。對 dataframe 的使用也因此變得更熟悉。意外的發現了很好的學習資源，期許自己持續的成長，學以致用。
