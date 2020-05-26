include $(TOPDIR)/rules.mk

PKG_NAME:=NanoHatOLED
PKG_VERSION:=1.0.1
PKG_RELEASE:=2
PKG_DATE:=20200526

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
	TITLE:=Support for NanoHatOLED.
	PKGARCH:=all
	DEPENDS:=+kmod-i2c-core +kmod-i2c-gpio +kmod-i2c-gpio-custom +kmod-i2c-smbus +python-pillow +python-smbus
endef

define Package/$(PKG_NAME)/description
OpenWrt OLED display for NanoHatOLED.
endef

define Build/Compile
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/nanohatoled $(1)/etc/init.d/nanohatoled
	$(INSTALL_DIR) $(1)/usr
	cp -pR ./files/usr/* $(1)/usr/
endef

define Package/$(PKG_NAME)/postinst
#!/bin/sh
if [ -z "$${IPKG_INSTROOT}" ]; then
    /etc/init.d/nanohatoled enable
fi
exit 0
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
