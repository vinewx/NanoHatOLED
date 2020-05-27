# NanoHatOLED
[1]: https://img.shields.io/badge/license-MIT-brightgreen.svg
[2]: /LICENSE
[3]: https://img.shields.io/badge/PRs-welcome-brightgreen.svg
[4]: https://github.com/vinewx/NanoHatOLED/pulls
[5]: https://img.shields.io/badge/Issues-welcome-brightgreen.svg
[6]: https://github.com/vinewx/NanoHatOLED/issues/new
[7]: https://img.shields.io/github/downloads/vinewx/NanoHatOLED/total
[8]: https://github.com/vinewx/NanoHatOLED/releases
[![license][1]][2]
[![PRs Welcome][3]][4]
[![Issue Welcome][5]][6]
[![Release Count][7]][8]

OpenWrt OLED display for NanoHatOLED.
## Depends / 依赖
- i2c-tools
- python-pillow
- python-smbus

## Compile / 编译
```bash
# 请在feeds.conf.default中下方添加
src-git NanoHatOLED https://github.com/vinewx/NanoHatOLED.git

# 更新并安装feeds软件包
./scripts/feeds update -a
./scripts/feeds install -a

# 选择要编译的包 Extra packages -> nanohatoled
make menuconfig
```
## Thanks / 谢致
Based on: 
- [friendlyarm/NanoHatOLED](https://github.com/friendlyarm/NanoHatOLED) 

<img src="https://github.com/vinewx/NanoHatOLED/raw/master/assets/k1.jpg" width="250" /> <img src="https://github.com/vinewx/NanoHatOLED/raw/master/assets/k2.jpg" width="250" /> <img src="https://github.com/vinewx/NanoHatOLED/raw/master/assets/k3.jpg" width="250" />
