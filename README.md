# NanoHatOLED
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
