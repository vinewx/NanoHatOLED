include $(TOPDIR)/rules.mk

PKG_NAME:=nanohatoled
PKG_VERSION:=1.0
PKG_RELEASE:=beta
PKG_DATE:=20200422

include $(INCLUDE_DIR)/package.mk

define Package/$(PKG_NAME)
  CATEGORY:=LuCI
  SUBMENU:=3. Applications
  TITLE:=Support for NanoHatOLED
  PKGARCH:=all
  DEPENDS:=+ifstat +kmod-i2c-core +kmod-i2c-gpio +kmod-i2c-gpio-custom +kmod-i2c-smbus +luci-app-openclash +python-pillow +python-smbus
endef

define Build/Prepare
endef
 
define Build/Configure
endef
 
define Build/Compile
endef

define Package/$(PKG_NAME)/install	
	$(INSTALL_DIR) $(1)/etc/init.d
	cp ./etc/init.d/oled $(1)/etc/init.d/oled
	
	$(INSTALL_DIR) $(1)/usr
	cp -pR ./usr/* $(1)/usr/
endef

define Package/$(PKG_NAME)/postinst
#!/bin/sh
chmod 0755 $${IPKG_INSTROOT}/etc/init.d/oled >/dev/null 2>&1
if [ -z "$${IPKG_INSTROOT}" ]; then
    /etc/init.d/oled enable
fi
exit 0
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
