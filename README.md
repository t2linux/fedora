# t2linux-fedora-kernel

Patched kernel for fedora linux on T2 macs. It mostly works, but dont expect a MacOS like experience. If you have problems with wifi, follow the guide on the wiki. A dnf/yum repo is avaliable at [`https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo`](https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo).

Follow the [wifi guide](https://wiki.t2linux.org/guides/wifi/). Installing the wifi firmware will also enable bluetooth. The internal drive, camera, mic, and keyboard/trackpad **are** working. Wifi and bluetooth woork with some extra steps, see below. The fingerprint reader is not working. Make sure to leave some space for MacOS, it is the only way to get firmware updates. Look at [https://wiki.t2linux.org/state/](https://wiki.t2linux.org/state/) for the latest state of hardware enablement.

Secure boot is disabled when using this kernel. **This is not a bad thing**. Mac firmware does not enforce secure boot; even when the shim loads a signed kernel, the shim itself can be modified. It is imposible to have secure boot on macs, a signed kernel does not help, it is a false sense of security. To protect yourself from evil maid attacks, you should never give other people access to your computer.

This kernel will follow the latest stable kernel version in the updates repo of the latest fedora release. The latest release is currently for Fedora 37, but it should work with newer/older releases.

### Wifi

Follow the [wifi guide](https://wiki.t2linux.org/guides/wifi/). Installing the wifi firmware will also enable bluetooth. First download the wifi script from the wiki. Then run the script from MacOS, after that reboot into Fedora. From Fedora run `sudo mount /dev/nvmen1p1 /mnt && sudo /mnt/wifi.sh`. Reboot, Wifi, Bluetooth, and suspend will work now.

## Instalation

1. Partition disks using Bootcamp Assistant, but dont install Windows.
2. Write [t2linux-fedora-iso](https://github.com/sharpenedblade/t2linux-fedora-iso) to a bootable drive.
3. Install Fedora like normal until you get to partitioning disks
4. Chose manual partitioning, then click auto-create mount points.
5. Click on the `/boot/efi` partition, then change the filesystem type to `EFI System Partition` from `Linux  HFS+ EFI`.
6. Install Fedora, do not close the installer.
5. Reboot while holding *option*.

## Troubleshooting

- Q: Suspend is not working.
    A: Install the mac firmware. Follow the [wifi section](#wifi).
- Q: The keyboard backlight is not working.
    A: It is not working properly yet. Run `echo 60 > /sys/class/leds/apple::kbd_backlight/brightness` to turn it on.
- Q: Touchbar is blank.
    A: Reboot into MacOS. Restart into MacOS again. Shut down from MacOS. Reboot into Fedora.

### TODO

- Signed kernel modules
- Automaticaly setting up Wifi firmware
- No extra modules in initramfs
- Keyboard backlight
