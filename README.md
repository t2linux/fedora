# t2linux-fedora-kernel
Patched kernel for fedora linux on T2 macs. It mostly works, but dont expect a MacOS like experience. If you have problems with wifi, follow the guide on the wiki. A dnf/yum repo is avaliable at [`https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo`](https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo).

Follow the [wifi guide](https://wiki.t2linux.org/guides/wifi/). Installing the wifi firmware will also enable bluetooth. The internal drive, camera, mic, and keyboard/trackpad **are** working. Wifi and bluetooth woork with some extra steps, see below. The fingerprint reader is not working. Make sure to leave some space for MacOS, it is the only way to get firmware updates. Look at [https://wiki.t2linux.org/state/](https://wiki.t2linux.org/state/) for the latest state of hardware enablement.

Secure boot is disabled when using this kernel. **This is not a bad thing**. Mac firmware does not enforce secure boot; even when the shim loads a signed kernel, the shim itself can be modified. It is imposible to have secure boot on macs, a signed kernel does not help, it is a false scence of security. To protect yourself from evil maid atacks, you should never give other people access to your computer.

### Wifi

Follow the [wifi guide](https://wiki.t2linux.org/guides/wifi/). Installing the wifi firmware will also enable bluetooth.

### TODO
    - Signing the package
    - Using upstream shim.
    - Signed kernel modules
    - Automaticaly seting up Wifi firmware
