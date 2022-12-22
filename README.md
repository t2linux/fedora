# t2linux-fedora-kernel

Patched kernel for Fedora on T2 macs. A dnf/yum repo is avaliable by installing the `t2linux-repos` package from the latest [release](https://github.com/sharpenedblade/t2linux-fedora-kernel/releases/latest).

Make sure to follow the [WiFi/Bluetooth guide](https://wiki.t2linux.org/guides/wifi-bluetooth/).The internal ssd, camera, mic, and keyboard/trackpad *are* working out of the box. Wifi and bluetooth work with some extra steps, follow the instructions bellow. The fingerprint reader is not working. Look at [https://wiki.t2linux.org/state/](https://wiki.t2linux.org/state/) for the latest state of hardware enablement.

Secure boot is disabled when using this kernel. **This is not a bad thing**. Mac firmware does not enforce secure boot; even when the kernel is signed. It is imposible to have secure boot on macs. To protect yourself from evil maid attacks, you should never give other people access to your computer.

This kernel will follow the latest stable kernel version in the updates repo of the latest Fedora release. The latest release is currently built for Fedora 37, but it should work with newer/older releases.

### Wifi

Follow the [wifi guide](https://wiki.t2linux.org/guides/wifi/). Installing the wifi firmware will also enable bluetooth. First download the wifi script from the wiki. Then run the script from MacOS, after that reboot into Fedora. From Fedora run `sudo mount /dev/nvmen1p1 /mnt && sudo /mnt/wifi.sh`. Reboot, Wifi, Bluetooth, and suspend will work now.

## Instalation

1. Partition disks using Bootcamp Assistant, but dont install Windows.
2. Write [t2linux-fedora-iso](https://github.com/sharpenedblade/t2linux-fedora-iso) to a bootable drive.
3. Boot the drive, then follow the WiFi section.
4. Install Fedora normally, do not close the installer. Make sure to not delete the MacOS partition.
5. Reboot while holding *option*.

## Troubleshooting

- Q: Suspend is not working.
    A: Install the WiFi firmware. Follow the [wifi section](#wifi).
- Q: The keyboard backlight is not working.
    A: It is not working on Fedora yet. If you *really* need it, contact `@sharpenedblade` on the t2linux discord.
- Q: The touchbar is blank, and I already installed the firmware.
    A: Reboot into MacOS twice. Log in to MacOS, then shut down from MacOS. Reboot into Fedora.

## Roadmap

- Modules in kernel.
- Secure boot signed kernel.
- Keyboard backlight.
- General bug fixes.
