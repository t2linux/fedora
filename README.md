# t2linux-fedora-kernel

This is a patched kernel for Fedora on T2 macs. A `dnf` repo is avaliable by installing the `t2linux-repo` package from the latest [release](https://github.com/t2linux-fedora/t2linux-fedora-kernel/releases/latest).

The internal ssd, camera, mic, and the keyboard/trackpad work out of the box. WiFi and Bluetooth work with some extra steps. Read [this](https://wiki.t2linux.org/state/) for information about the latest hardware support.

This kernel is usually at the same version as the stable Fedora kernel. It is currently built for Fedora 38.

## Instalation

Download the live ISO from [here](https://github.com/t2linux/t2linux-fedora-iso). Follow the [installation guide](https://wiki.t2linux.org/distributions/fedora/installation/).

## WiFi/Bluetooth

Follow the [firmware guide](https://wiki.t2linux.org/guides/wifi/). When you get to the [On Linux](https://wiki.t2linux.org/guides/wifi-bluetooth/#on-linux) section, you can just run `firmware.sh`. 

## Upgrading to a new Fedora Version

This should work normally, either with `dnf system-upgrade` or Gnome Software (PackageKit). If you get an error about `t2linux-config`, run `sudo dnf remove t2linux-config && sudo dnf install t2linux-config`.

## Troubleshooting

- Q: Suspend is not working.  
    A: Install the WiFi firmware. Follow the [wifi section](#wifi).
- Q: The keyboard backlight is not working.  
    A: It doesnt work for *some* users on Fedora. If you *really* need it, contact `@sharpenedblade` on the t2linux discord.
- Q: The touchbar is blank, and I already installed the firmware.  
    A: Reboot into MacOS Recovery by holding CMD+R while booting up, then reboot into Fedora again.

## Credits

This kernel was heavily inspired by [mikeeq/mbp-fedora-kernel](https://github.com/mikeeq/mbp-fedora-kernel). The patches are from the [t2linux](https://t2linux.org) project and [everyone that contributed to to it](https://github.com/t2linux/linux-t2-patches/graphs/contributors).

## Disclaimer
This project is not officially provided or supported by the Fedora Project. The official Fedora software is available at [https://fedoraproject.org/](https://fedoraproject.org/). This project is not related to Fedora in any way.
