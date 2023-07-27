# t2linux-fedora-kernel

This is a patched kernel for Fedora on T2 macs. A `dnf` repo is avaliable by installing the `t2linux-repo` package from the latest [release](https://github.com/t2linux-fedora/t2linux-fedora-kernel/releases/latest).

The internal ssd, camera, mic, and the keyboard/trackpad work out of the box. WiFi and Bluetooth work with some extra steps. Read [this](https://wiki.t2linux.org/state/) for information about the latest hardware support.

This kernel is usually at the same version as the stable Fedora kernel. It is currently built for Fedora 38.

## Instalation

Download the live ISO from [here](https://github.com/t2linux/t2linux-fedora-iso). Follow the [installation guide](https://wiki.t2linux.org/distributions/fedora/installation/).

## WiFi/Bluetooth

Follow the [firmware guide](https://wiki.t2linux.org/guides/wifi/). When you get to the [On Linux](https://wiki.t2linux.org/guides/wifi-bluetooth/#on-linux) section, you can just run `firmware.sh`.

## Troubleshooting

- Problem: The touchbar is not working and is blank  
   Solution: Reboot into MacOS Recovery by holding `command`+`r` while booting up, then reboot into Fedora again.

- Problem: Suspend is not working  
   Solution: Put this in `/usr/lib/systemd/system-sleep/rmmod_wifi.sh`:
  ```bash
  #!/usr/bin/env bash
  if [ "${1}" = "pre" ]; then
          modprobe -r brcmfmac_wcc
          modprobe -r brcmfmac
  elif [ "${1}" = "post" ]; then
          modprobe brcmfmac
  fi
  ```

## Building from source

Clone this repo locally:

```
git clone --depth 1 https://github.com/t2linux/t2linux-fedora-kernel
cd t2linux-fedora-kernel
```

Pick the package you want to build (`t2linux-config`, `t2linux-repo`, `t2linux-config`, or `kernel`):

```
export PACKAGE="packagenamehere"
```

Then run the build container, which has dependencies already installed. The packages will be in the `_output` directory:

```
podman run -it -v "$PWD":/repo -e PACKAGE ghcr.io/t2linux/fedora-dev:latest /repo/build-packages.sh
```

## Credits

This kernel was heavily inspired by [mikeeq/mbp-fedora-kernel](https://github.com/mikeeq/mbp-fedora-kernel). The patches are from the [t2linux](https://t2linux.org) project and created by [everyone that contributed to to it](https://github.com/t2linux/linux-t2-patches/graphs/contributors).

## Disclaimer

This project is not officially provided or supported by the Fedora Project. The official Fedora software is available at [https://fedoraproject.org/](https://fedoraproject.org/). This project is not related to Fedora in any way.
