# NanoHatOLED
OpenWrt OLED display for NanoHatOLED.
## Depends / 依赖
- kmod-i2c-core
- kmod-i2c-gpio
- kmod-i2c-gpio-custom
- kmod-i2c-smbus
- python-pillow
- python-smbus

## Compile / 编译
```bash
# 请在feeds.conf.default中下方添加
src-git NanoHatOLED https://github.com/vinewx/NanoHatOLED.git

# 更新并安装feeds软件包
./scripts/feeds update -a
./scripts/feeds install -a

# 选择要编译的包 LuCI -> Applications -> nanohatoled
make menuconfig
```
## Thanks / 谢致
本项目代码基于：
- [friendlyarm/NanoHatOLED](https://github.com/friendlyarm/NanoHatOLED) 
- [Pi群固件](https://t.me/NewPiN1Channel/21) by [jerrykuku](https://github.com/jerrykuku)
- [raspberry-gpio-python](https://sourceforge.net/projects/raspberry-gpio-python) by [croston](https://sourceforge.net/u/croston)
