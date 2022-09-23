# t2linux-fedora-kernel
Patched kernel for fedora linux on T2 macs. It mostly works, but dont expect a MacOS like experience. If you have problems with wifi, follow the guide on the wiki. A dnf/yum repo is avaliable at [`https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo`](https://t2linux-fedora-repo.netlify.app/repo/t2linux-fedora.repo).

## Compatability


- What works (See [https://wiki.t2linux.org/state/](https://wiki.t2linux.org/state/) for the latest info).
    - Wifi (follow [https://wiki.t2linux.org/guides/wifi/](https://wiki.t2linux.org/guides/wifi/))
    - Internal Drive
    - Audio
    - USB
    - Internal keyboard/trackpad
    - Internal display
    - Touchbar (only function keys)
    - Camera/Microphone
    - Bluetooth
    - Audio
    - Everything else that works on normal x86_64 laptops
 
- What doesnt work
    - Using the T2 chip as TPM
    - Reading APFS
