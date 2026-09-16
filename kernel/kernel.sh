#!/usr/bin/bash
set -e

KERNEL_VERSION=$(cat ./version)

cd "$sourcedir"
koji download-build --quiet --arch=src "kernel-$KERNEL_VERSION"
rpmdev-extract -q "kernel-$KERNEL_VERSION.src.rpm"
mv -n "kernel-$KERNEL_VERSION.src"/* .
rm -r "kernel-$KERNEL_VERSION.src.rpm" "kernel-$KERNEL_VERSION.src"

# Set buildid to .t2
sed -i 's/# define buildid .local/%define buildid .t2/g' "kernel.spec"

# Bump release
# sed -i 's/%define specrelease 200/%define specrelease 210/g' "kernel.spec"

# Disable debug kernels
sed -i "/%define with_debug /c %define with_debug 0" "kernel.spec"

# Add our patches
sed -i "/Patch1:/a Patch2: t2linux-combined.patch" "kernel.spec"
sed -i "/ApplyOptionalPatch patch-%{patchversion}-redhat.patch/a ApplyOptionalPatch t2linux-combined.patch" "kernel.spec"

# cp "linux-t2-patches/extra_config" "kernel-local"
cat << 'EOF' > "kernel-local"
CONFIG_SPI_HID_APPLE_OF=y
CONFIG_HID_DOCKCHANNEL=y
CONFIG_APPLE_DOCKCHANNEL=y
CONFIG_APPLE_RTKIT_HELPER=m
CONFIG_APFS_FS=m
EOF

function write_kconfig_to_file {
  config_opt=$(echo "$1" | cut -d'=' -f1)
  if [[ "$config_opt" =~ '# '(.+)' is not set' ]]; then
    config_opt="${BASH_REMATCH[1]}"
  fi
  sed -i "/# $config_opt is not set/d" "$2"
  sed -i "/$config_opt=/d" "$2"
  echo "$1" >> "$2"
}

function set_kconfig_x86_64 {
  for file in \
    "kernel-x86_64-fedora.config" \
    "kernel-x86_64-rt-debug-fedora.config" \
    "kernel-x86_64-rt-fedora.config" \
    "kernel-x86_64-debug-fedora.config"
  do
    write_kconfig_to_file "$1" "$file"
  done
}

set_kconfig_x86_64 'CONFIG_APPLE_BCE=m'

readarray -t extra_config < linux-t2-patches/extra_config
for config in "${extra_config[@]}"; do
  set_kconfig_x86_64 "$config"
done

set_kconfig_x86_64 'CONFIG_INPUT_SPARSEKMAP=y'
set_kconfig_x86_64 'CONFIG_MODULE_FORCE_UNLOAD=y'
set_kconfig_x86_64 'CONFIG_CMDLINE="intel_iommu=on iommu=pt pm_async=off"'
set_kconfig_x86_64 'CONFIG_CMDLINE_BOOL=y'
set_kconfig_x86_64 '# CONFIG_CMDLINE_OVERRIDE is not set'

set_kconfig_x86_64 'CONFIG_I2C_MUX=y'
set_kconfig_x86_64 'CONFIG_VIDEO_DEV=y'
set_kconfig_x86_64 'CONFIG_MEDIA_CONTROLLER=y'
set_kconfig_x86_64 'CONFIG_DVB_CORE=y'
set_kconfig_x86_64 '# CONFIG_USB_AIRSPY is not set'
set_kconfig_x86_64 '# CONFIG_USB_HACKRF is not set'
set_kconfig_x86_64 '# CONFIG_USB_MSI2500 is not set'
set_kconfig_x86_64 '# CONFIG_SDR_PLATFORM_DRIVERS is not set'
set_kconfig_x86_64 'CONFIG_VIDEO_CS3308=m'
set_kconfig_x86_64 'CONFIG_VIDEO_SAA6752HS=m'
set_kconfig_x86_64 '# CONFIG_SDR_MAX2175 is not set'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_E4000=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_FC0011=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_FC0012=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_FC0013=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_FC2580=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_IT913X=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_M88RS6000T=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MAX2165=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MT2060=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MT2063=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MT2131=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MT2266=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MXL5005S=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_MXL5007T=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_QM1D1B0004=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_QM1D1C0042=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_QT1010=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_R820T=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_SI2157=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_TDA18212=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_TDA18218=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_TDA18250=m'
set_kconfig_x86_64 'CONFIG_MEDIA_TUNER_TUA9001=m'
set_kconfig_x86_64 'CONFIG_DVB_M88DS3103=m'
set_kconfig_x86_64 'CONFIG_DVB_MXL5XX=m'
set_kconfig_x86_64 'CONFIG_DVB_STB0899=m'
set_kconfig_x86_64 'CONFIG_DVB_STB6100=m'
set_kconfig_x86_64 'CONFIG_DVB_STV090x=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0910=m'
set_kconfig_x86_64 'CONFIG_DVB_STV6110x=m'
set_kconfig_x86_64 'CONFIG_DVB_STV6111=m'
set_kconfig_x86_64 'CONFIG_DVB_DRXK=m'
set_kconfig_x86_64 'CONFIG_DVB_SI2165=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA18271C2DD=m'
set_kconfig_x86_64 'CONFIG_DVB_CX24110=m'
set_kconfig_x86_64 'CONFIG_DVB_CX24116=m'
set_kconfig_x86_64 'CONFIG_DVB_CX24117=m'
set_kconfig_x86_64 'CONFIG_DVB_CX24120=m'
set_kconfig_x86_64 'CONFIG_DVB_CX24123=m'
set_kconfig_x86_64 'CONFIG_DVB_DS3000=m'
set_kconfig_x86_64 'CONFIG_DVB_MB86A16=m'
set_kconfig_x86_64 'CONFIG_DVB_MT312=m'
set_kconfig_x86_64 'CONFIG_DVB_S5H1420=m'
set_kconfig_x86_64 'CONFIG_DVB_SI21XX=m'
set_kconfig_x86_64 'CONFIG_DVB_STB6000=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0288=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0299=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0900=m'
set_kconfig_x86_64 'CONFIG_DVB_STV6110=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA10071=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA10086=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA8083=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA8261=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA826X=m'
set_kconfig_x86_64 'CONFIG_DVB_TS2020=m'
set_kconfig_x86_64 'CONFIG_DVB_TUA6100=m'
set_kconfig_x86_64 'CONFIG_DVB_TUNER_CX24113=m'
set_kconfig_x86_64 'CONFIG_DVB_TUNER_ITD1000=m'
set_kconfig_x86_64 'CONFIG_DVB_VES1X93=m'
set_kconfig_x86_64 'CONFIG_DVB_ZL10036=m'
set_kconfig_x86_64 'CONFIG_DVB_ZL10039=m'
set_kconfig_x86_64 'CONFIG_DVB_AF9013=m'
set_kconfig_x86_64 'CONFIG_DVB_CX22700=m'
set_kconfig_x86_64 'CONFIG_DVB_CX22702=m'
set_kconfig_x86_64 'CONFIG_DVB_CXD2820R=m'
set_kconfig_x86_64 'CONFIG_DVB_CXD2841ER=m'
set_kconfig_x86_64 'CONFIG_DVB_DIB3000MB=m'
set_kconfig_x86_64 'CONFIG_DVB_DIB3000MC=m'
set_kconfig_x86_64 'CONFIG_DVB_DIB7000M=m'
set_kconfig_x86_64 'CONFIG_DVB_DIB7000P=m'
set_kconfig_x86_64 'CONFIG_DVB_DRXD=m'
set_kconfig_x86_64 'CONFIG_DVB_EC100=m'
set_kconfig_x86_64 'CONFIG_DVB_L64781=m'
set_kconfig_x86_64 'CONFIG_DVB_MT352=m'
set_kconfig_x86_64 'CONFIG_DVB_NXT6000=m'
set_kconfig_x86_64 'CONFIG_DVB_RTL2830=m'
set_kconfig_x86_64 'CONFIG_DVB_RTL2832=m'
set_kconfig_x86_64 'CONFIG_DVB_RTL2832_SDR=m'
set_kconfig_x86_64 'CONFIG_DVB_SI2168=m'
set_kconfig_x86_64 'CONFIG_DVB_SP887X=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0367=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA10048=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA1004X=m'
set_kconfig_x86_64 'CONFIG_DVB_ZD1301_DEMOD=m'
set_kconfig_x86_64 'CONFIG_DVB_ZL10353=m'
set_kconfig_x86_64 'CONFIG_DVB_STV0297=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA10021=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA10023=m'
set_kconfig_x86_64 'CONFIG_DVB_VES1820=m'
set_kconfig_x86_64 'CONFIG_DVB_AU8522_DTV=m'
set_kconfig_x86_64 'CONFIG_DVB_AU8522_V4L=m'
set_kconfig_x86_64 'CONFIG_DVB_BCM3510=m'
set_kconfig_x86_64 'CONFIG_DVB_LG2160=m'
set_kconfig_x86_64 'CONFIG_DVB_LGDT3305=m'
set_kconfig_x86_64 'CONFIG_DVB_LGDT3306A=m'
set_kconfig_x86_64 'CONFIG_DVB_LGDT330X=m'
set_kconfig_x86_64 'CONFIG_DVB_MXL692=m'
set_kconfig_x86_64 'CONFIG_DVB_NXT200X=m'
set_kconfig_x86_64 'CONFIG_DVB_OR51132=m'
set_kconfig_x86_64 'CONFIG_DVB_OR51211=m'
set_kconfig_x86_64 'CONFIG_DVB_S5H1409=m'
set_kconfig_x86_64 'CONFIG_DVB_S5H1411=m'
set_kconfig_x86_64 'CONFIG_DVB_DIB8000=m'
set_kconfig_x86_64 'CONFIG_DVB_MB86A20S=m'
set_kconfig_x86_64 'CONFIG_DVB_S921=m'
set_kconfig_x86_64 'CONFIG_DVB_TC90522=m'
set_kconfig_x86_64 'CONFIG_DVB_PLL=m'
set_kconfig_x86_64 'CONFIG_DVB_TUNER_DIB0070=m'
set_kconfig_x86_64 'CONFIG_DVB_TUNER_DIB0090=m'
set_kconfig_x86_64 'CONFIG_DVB_A8293=m'
set_kconfig_x86_64 'CONFIG_DVB_AF9033=m'
set_kconfig_x86_64 'CONFIG_DVB_ASCOT2E=m'
set_kconfig_x86_64 'CONFIG_DVB_ATBM8830=m'
set_kconfig_x86_64 'CONFIG_DVB_HELENE=m'
set_kconfig_x86_64 'CONFIG_DVB_HORUS3A=m'
set_kconfig_x86_64 'CONFIG_DVB_ISL6405=m'
set_kconfig_x86_64 'CONFIG_DVB_ISL6421=m'
set_kconfig_x86_64 'CONFIG_DVB_ISL6423=m'
set_kconfig_x86_64 'CONFIG_DVB_IX2505V=m'
set_kconfig_x86_64 'CONFIG_DVB_LGS8GXX=m'
set_kconfig_x86_64 'CONFIG_DVB_LNBH25=m'
set_kconfig_x86_64 'CONFIG_DVB_LNBP21=m'
set_kconfig_x86_64 'CONFIG_DVB_LNBP22=m'
set_kconfig_x86_64 'CONFIG_DVB_M88RS2000=m'
set_kconfig_x86_64 'CONFIG_DVB_TDA665x=m'
set_kconfig_x86_64 'CONFIG_DVB_DRX39XYJ=m'
set_kconfig_x86_64 'CONFIG_DVB_SP2=m'

cat "linux-t2-patches"/*.patch > "t2linux-combined.patch"
