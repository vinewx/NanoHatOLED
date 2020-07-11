# NanoHatOLED
[1]: https://img.shields.io/badge/license-MIT-brightgreen.svg
[2]: /LICENSE
[3]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
[4]: https://github.com/vinewx/NanoHatOLED/pulls
[5]: https://img.shields.io/badge/Issues-welcome-brightgreen.svg
[6]: https://github.com/vinewx/NanoHatOLED/issues/new
[7]: https://img.shields.io/badge/version-v2.0.0-blue.svg?
[![license][1]][2]
[![PRs Welcome][3]][4]
[![Issue Welcome][5]][6]
![Version][7]

OpenWrt OLED display for NanoHatOLED.
## Depends / 依赖
- i2c-tools
- python3-pillow
- python3-requests
- python3-smbus

## Compile / 编译
1. 请在feeds.conf.default中下方添加
```bash
src-git NanoHatOLED https://github.com/vinewx/NanoHatOLED.git^547ec7e5d69455f000ba1987189999a3bee0b83f
```

2. 更新feeds
```bash
./scripts/feeds update NanoHatOLED
```
3. 修改`OpenWrt` 项目的 `feeds/NanoHatOLED/nanohatoled/files/NanoHatOLED` 目录下`bakebit_nanohat_oled.py`文件  
第121行`101010100`改为你所在地区的9位编码  
编码查询 -> [citycode.json](https://github.com/vinewx/NanoHatOLED/blob/weather/citycode.json)

4. 安装feeds
```bash
./scripts/feeds install nanohatoled
```

5. 选择要编译的包
```bash
# Extra packages -> nanohatoled
make menuconfig
```
## Thanks / 谢致
- Based on: [friendlyarm/NanoHatOLED](https://github.com/friendlyarm/NanoHatOLED)
- [Weather API](https://www.sojson.com/api/weather.html)
- [zpix-pixel-font](https://github.com/SolidZORO/zpix-pixel-font)
- ![caiyun](http://caiyunapp.com/imgs/logo/logo-website.png)

<img src="https://github.com/vinewx/NanoHatOLED/raw/weather/assets/k1.jpg" width="200" /> <img src="https://github.com/vinewx/NanoHatOLED/raw/weather/assets/k2_1.jpg" width="200" /> <img src="https://github.com/vinewx/NanoHatOLED/raw/weather/assets/k2_2.jpg" width="200" /> <img src="https://github.com/vinewx/NanoHatOLED/raw/weather/assets/k3.jpg" width="200" />
