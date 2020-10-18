include $(TOPDIR)/rules.mk

PKG_NAME:=micropython-drcom
PKG_RELEASE:=2
PKG_LICENSE:=AGPL-3.0
PKG_LICENSE_FILE:=LICENSE.md
PKG_MAINTAINER:=Hagb <hagb_green@qq.com>

include $(INCLUDE_DIR)/package.mk

define Package/micropython-drcom
	SECTION:=net
	CATEGORY:=Network
	TITLE:=DrCOM unofficial client for micropython
	URL:=https://github.com/Hagb/micropython-drcom
	DEPENDS:=+micropython +micropython-lib
	PKGARCH:=all
endef

define Package/micropython-drcom/description
DrCOM unofficial client modified from drcom-generic project to run in
micropython. For smaller size, you can use micropython-drcom-with-lib package
but not micropython-drcom package with tailored micropython-lib, which can be
installed without large micropython-lib package.
endef

define Package/micropython-drcom-with-lib
	SECTION:=net
	CATEGORY:=Network
	TITLE:=DrCOM unofficial client for micropython, with tailored micropython-lib
	URL:=https://github.com/Hagb/micropython-drcom
	DEPENDS:=+micropython
	PKGARCH:=all
endef

define Package/micropython-drcom-with-lib/description
DrCOM unofficial client modified from drcom-generic project to run in
micropython. This package with tailored  micropython-lib, can be installed
without large micropython-lib package.
endef

define Build/Compile
	true
endef

define Build/Configure
	true
endef

define Build/Install
	true
endef

define Package/micropython-drcom/install
	$(INSTALL_DIR) $(1)/usr/bin/ $(1)/etc/ $(1)/usr/lib/micropython-drcom/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/openwrt/drcom-wired $(1)/usr/bin/drcom-wired
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/drcom_wired.conf $(1)/etc/drcom_wired.conf
	$(INSTALL_DATA) $(PKG_BUILD_DIR)/*.py $(1)/usr/lib/micropython-drcom/
endef

define Package/micropython-drcom-with-lib/install
	$(call Package/micropython-drcom/install,$(1))
	$(INSTALL_DIR) $(1)/usr/lib/micropython-drcom/
	$(CP) -ar $(PKG_BUILD_DIR)/micropython/* $(1)/usr/lib/micropython-drcom/
endef

$(eval $(call BuildPackage,micropython-drcom))
$(eval $(call BuildPackage,micropython-drcom-with-lib))
