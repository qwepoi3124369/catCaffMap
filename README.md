# 高雄貓咖地圖 (Kaohsiung Cat Cafes GIS)

> 個人 Side Project — 使用 GeoDjango + ArcGIS API for JavaScript (v4.x) 建置的 Web GIS，提供高雄市貓咪咖啡廳資訊查詢、環域分析(Buffer)、屬性搜尋，並含使用者登入與後台管理功能。可透過 Docker + uWSGI + Nginx + Cloudflare Tunnel 部署。

---

## 目標

1. 使用 GeoDjango + ArcGIS API for JavaScript (4.x) 建構互動式地圖介面。
2. 顯示高雄市貓咪咖啡廳資訊（地理位置 + 屬性資料）。
3. 支援環域分析（Buffer）：以點或線為中心查詢特定半徑內店家。
4. 支援基於屬性的店家查詢（例如：關鍵字、營業時間、是否接受預約等）。
5. 前端響應式設計 (RWD)。
6. 自建的登入機制（不是 Django 內建 admin 畫面），提供使用者登入與權限分級。
7. 後台 CRUD 功能：管理貓咪咖啡廳與公告訊息。
8. 提供 Docker 化部署，使用 uWSGI、Nginx，並示範搭配 Cloudflare Tunnel 暴露內網服務（或替換為其他反向代理）。
9. 把Docker化鏡像部屬於K3S中

---

## 技術棧

* 後端：Django + GeoDjango
* 資料庫：PostgreSQL + PostGIS
* 前端：ArcGIS API for JavaScript (4.x)、HTML/CSS (RWD)、Bootstrap
* 認證：Django 自訂認證
* 容器/部署：Docker, docker-compose, uWSGI, Nginx
* 暴露通道：Cloudflare Tunnel（cloudflared）或其他反向代理

---

相關介紹圖片:https://www.cake.me/portfolios/web-gis
