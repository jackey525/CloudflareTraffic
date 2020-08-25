# CloudflareTraffic

## 參考
```
https://developers.cloudflare.com/analytics/graphql-api/
https://github.com/cloudflare/python-cloudflare
```

## 安裝

### via PyPI
```
$ sudo pip install cloudflare
```

## 使用方法
```
$ python3 traffic.py 起始日期 結束日期 domain(此為選填，不寫表示會將 帳號內所有的 domain 都計算一次)

範例 1
$ python3 traffic.py 2020-08-18T07:54:29Z 2020-08-25T07:54:29Z a.b.com

範例 2
$ python3 traffic.py 2020-08-18T07:54:29Z 2020-08-25T07:54:29Z

範例 3  自動設定 以今天現在時間為主  往前 7 天
$ python3 traffic.py
``` 

## 輸出 Output.csv
![image](https://github.com/jackey525/CloudflareTraffic/blob/master/screenshot.png)
