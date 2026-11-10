<!--
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  Zane Zhang · GitHub Profile README                                      │
  │                                                                          │
  │  本文件依赖同目录下的 assets/ 与 tools/，请一起提交：                      │
  │    README.md  assets/china-map-{light,dark}.svg                           │
  │               assets/satellite-{light,dark}.svg                          │
  │    tools/build_map.py  tools/build_satellite.py  geo/index.html          │
  │                                                                          │
  │  仓库名必须是 zhangyx0803（和你用户名同名），首页才会显示这份 README。      │
  │  需要你补的只有 2 处，正文里标了「改我」：① 邮箱 ② 项目链接。               │
  └──────────────────────────────────────────────────────────────────────────┘
-->

<p align="center">
  <a href="https://github.com/zhangyx0803">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=21&pause=1000&color=3BA55D&center=true&vCenter=true&width=700&lines=GISer+%2B+Researcher+%2B+Coder;%E5%86%99%E7%A7%91%E7%A0%94%E4%BB%A3%E7%A0%81%EF%BC%8C%E6%9B%B4%E5%86%99Bug;Coordinates+don%27t+lie%2C+but+my+projections+do.;%E5%9D%90%E6%A0%87%E4%B8%8D%E4%BC%9A%E8%AF%B4%E8%B0%8E%EF%BC%8C%E4%BD%86%E6%88%91%E7%9A%84%E6%8A%95%E5%BD%B1%E5%8F%98%E6%8D%A2%E6%80%BB%E5%87%BA%E9%94%99;Logging+the+journey+of+science.;%E8%AE%B0%E5%BD%95%E7%A7%91%E7%A0%94%E8%B7%AF%E4%B8%8A%E7%9A%84%E6%AF%8F%E4%B8%80%E6%AC%A1Debug%E3%80%82" alt="Typing SVG" />
  </a>
</p>

<h1 align="center">Hi there, I'm Zane Zhang 👋</h1>

<p align="center">
  <b>A GISer in Shanghai</b> 🌍 地理信息科学 · 空间分析 · 遥感与城市气候
</p>

<p align="center">
  <code>31.1650°N  121.4050°E</code> — <a href="https://www.openstreetmap.org/?mlat=31.1650&mlon=121.4050#map=15/31.1650/121.4050">上海 · 徐汇</a> · UTC+8 · 海拔 ≈ 4 m
</p>

<p align="center">
  <img alt="上海实时气温" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.open-meteo.com%2Fv1%2Fforecast%3Flatitude%3D31.165%26longitude%3D121.405%26current%3Dtemperature_2m%2Crelative_humidity_2m&query=%24.current.temperature_2m&label=%E5%BE%90%E6%B1%87%20%E5%AE%9E%E6%97%B6&suffix=%C2%B0C&color=3ba55d" />
  <img alt="实时相对湿度" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.open-meteo.com%2Fv1%2Fforecast%3Flatitude%3D31.165%26longitude%3D121.405%26current%3Dtemperature_2m%2Crelative_humidity_2m&query=%24.current.relative_humidity_2m&label=%E6%B9%BF%E5%BA%A6&suffix=%25&color=3ba55d" />
  <img alt="Profile views" src="https://komarev.com/ghpvc/?username=zhangyx0803&label=VISITORS&color=3ba55d&style=flat" />
</p>

<p align="center">
  <a href="https://www.openstreetmap.org/?mlat=31.1650&mlon=121.4050#map=4/34.5/108.0" title="在 OpenStreetMap 上打开这个位置">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/china-map-dark.svg">
      <img src="assets/china-map-light.svg" alt="徐汇在中国地图上的位置" width="700">
    </picture>
  </a>
</p>

<p align="center">
  <sub>33 个省级单元 · Albers 等积圆锥投影（25°N / 47°N，中央经线 105°E）· 由 <a href="tools/build_map.py">tools/build_map.py</a> 生成 · 点图跳 OSM</sub>
</p>

<p align="center">
  <a href="https://www.openstreetmap.org/?mlat=31.1650&mlon=121.4050#map=16/31.1650/121.4050" title="在 OpenStreetMap 上打开这个位置">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/satellite-dark.svg">
      <img src="assets/satellite-light.svg" alt="卫星链路面板：31.1650N 121.4050E" width="700">
    </picture>
  </a>
</p>

---

### 🕵️‍♂️ About Me / 关于我

> *Navigating the world of Geospatial Data. / 在空间数据的海洋里疯狂迷路。*

- 🎓 **Education:** Geographic Information Science.
  <br>**教育背景**：地理信息科学专业（本科）。
  <!-- 原来那句写了「上海师范大学」，按你这次的选择正文里先不写校名；想加回来就把上面这句改成「上海师范大学，地理信息科学专业」。 -->

- 🔭 **What I do here:** This repo is mainly for my **Research Codes** and **Daily/Academic Logs**.
  <br>**这个主页用来干嘛**：存放我的**科研代码**和**日常/学术日志**。欢迎交流，但请原谅我偶尔粗糙的代码质量。

- 🌱 **I'm currently learning:** Spatial Analysis, Machine Learning.
  <br>**我正在努力搞懂**：空间分析、机器学习算法。

- 🤔 **My daily confusion:** Why is this geographic coordinate always offset?!
  <br>**我的日常疑惑**：为什么这个地理坐标又偏移了？！为什么这段代码昨天还能跑，今天就不行了？

- 💬 **Ask me about:** GIS, Cartography, or Sci-Fi, Music.
  <br>**随时可以找我聊**：地理信息、地图制图、科幻小说、或者音乐。

- ⚡ **Fun fact:** I can read maps but can still get lost in the mall.
  <br>**一个冷知识**：我虽然会画地图、懂 GIS，但在商场里依然会迷路。

---

### 🛰 一次空间分析，长这样

从一张影像到一条结论，中间隔着这么几步（可以展开看）：

```mermaid
flowchart LR
  A["① 观测<br/>Landsat 8/9 TIRS<br/>辐射定标 · 大气校正"] --> B["② 反演<br/>地表温度 LST<br/>单窗 / 劈窗算法"] --> C["③ 分析<br/>热岛强度 UHI<br/>冷岛斑块 · 网络连通性"] --> D["④ 决策<br/>通风廊道<br/>蓝绿空间布局"]
```

<details>
<summary><b>▸ 展开：我最常用的技能树</b></summary>

<br/>

```mermaid
mindmap
  root((空间分析))
    遥感
      热红外地表温度
      土地覆盖分类
      NDVI 与不透水面
    GIS
      投影与专题制图
      空间统计
      网络与连通性
    数据工程
      自动化脚本
      批量出图管线
      可复现的图件
    学术工作流
      文献检索与证据化精读
      Markdown 知识库
      日志与踩坑记录
```

</details>

<details>
<summary><b>▸ 展开：这张地图是怎么画出来的（可复现）</b></summary>

<br/>

- 地图不是截图，是**脚本生成的 SVG**：读取省级行政区 GeoJSON → 手写 Albers 等积圆锥投影 → Douglas–Peucker 抽稀 → 输出浅色 / 深色两套，靠 `<picture>` 与 `prefers-color-scheme` 自动跟随 GitHub 的深浅色主题。
- 徐汇那个点不是贴上去的图标，而是按 `31.1650, 121.4050` 投影算出来的真实位置，外面套了一个 `<animate>` 呼吸环。
- 下面那块卫星面板原本是写在 README 里的内联 `<svg>`——GitHub 会把它过滤掉，所以现在改为独立文件 `assets/satellite-*.svg`，雷达才转得起来。
- 想换成别的坐标：只改 `tools/build_map.py` 与 `tools/build_satellite.py` 顶部的常量，重跑一次即可。

</details>

---

### 🧭 想要一张能拖动的？

`geo/index.html` 是一页单文件 Leaflet 地图：可切换街道 / 卫星 / 地形三种底图，鼠标移动实时读出经纬度，
点击任意位置落一个坐标点；徐汇外围画了 5 km 的圈，外加 30°N、120°E 两条准星线，用来看「一度到底有多远」。

部署：仓库 **Settings → Pages → Source: Deploy from a branch → main / root**，
然后访问 `https://zhangyx0803.github.io/zhangyx0803/geo/`。

---

### 🛠️ Tech Stack / 技能树

> *Weapons of choice for Geospatial Science. / 空间科学的趁手兵器。*

<p align="left">
  <img src="https://img.shields.io/badge/ArcGIS-0079C1?style=for-the-badge&logo=esri&logoColor=white" />
  <img src="https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white" />
  <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" />
</p>

---

### 📁 Repository Focus / 仓库内容

- 🧪 **Research Codes**：处理遥感影像、空间插值、或数据挖掘的脚本与算法。*(主要语言：R / C++)*
- 📝 **Logs**：记录踩过的坑、科研进展、或者突然迸发的灵感。
- 🗺 **Cartography**：做完的图、做废的图，以及它们之间的差别。 <!-- 改我 ②：有具体项目后在这里加 `- [项目名称](链接)` -->

---

### 📊 GitHub Stats / 战况面板

<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=zhangyx0803&show_icons=true&hide_border=true&title_color=3ba55d&icon_color=3ba55d&locale=cn" alt="GitHub Stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=zhangyx0803&layout=compact&hide_border=true&title_color=3ba55d&locale=cn" alt="Top Langs" />
</p>

<p align="center">
  <img src="https://streak-stats.demolab.com?user=zhangyx0803&hide_border=true&locale=zh_Hans&date_format=Y.n.j&ring=3ba55d&fire=3ba55d&currStreakLabel=3ba55d" alt="GitHub Streak" />
</p>

<!-- 两张 vercel 卡片偶尔会限流（很常见），加载不出来就删掉那一行，不影响其他内容 -->

---

### 🤝 Connect with me / 如何联系我

<p align="center">
  <a href="mailto:你的邮箱@example.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <!-- 改我 ①：把上面的 你的邮箱@example.com 换成真实邮箱 -->
</p>

<p align="center">
  <i>"Everything is related to everything else, but near things are more related than distant things."</i>
  <br>
  <i>"地理学第一定律：世间万物皆有联系，但距离近的事物联系更为紧密。 —— Waldo Tobler"</i>
</p>

<p align="center">
  <sub>地图由 <code>tools/</code> 下的脚本生成 · 数据：DataV 行政区划 · 投影：Albers 25°N/47°N</sub>
</p>
