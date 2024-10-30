# t2linux-fedora-kernel

Patched kernel and supporting packages for hardware enablement on t2 macs. Binary packages are available from [copr](https://copr.fedorainfracloud.org/coprs/sharpenedblade/t2linux). You can also download and install the `copr-sharpenedblade-t2linux-release` package.

The internal ssd, camera, mic, and the keyboard/trackpad work out of the box. WiFi and Bluetooth might work with some extra steps. Read [the wiki](https://wiki.t2linux.org/state/) for information about the latest hardware support.

This kernel is usually at the same version as the stable Fedora kernel. It is currently built for Fedora 41.

## Instalation

Download the live ISO from [here](https://github.com/t2linux/fedora-iso). Follow the [installation guide](https://wiki.t2linux.org/distributions/fedora/installation/).

## WiFi/Bluetooth

Follow the [firmware guide](https://wiki.t2linux.org/guides/wifi/).

## Building from source

Clone this repo locally:

```bash
git clone --recursive --depth 1 https://github.com/t2linux/fedora t2-fedora
cd t2-fedora
```

Then run the build container, which has dependencies already installed. The packages will be in `builddir`. If you want to only build a specific package, pass its name as a argument to this command:

```bash
podman run --privileged -v "$PWD":/repo ghcr.io/t2linux/fedora-ci:41 /repo/build-packages.sh
```

## Credits

This kernel was heavily inspired by [mikeeq/mbp-fedora-kernel](https://github.com/mikeeq/mbp-fedora-kernel). The patches are from the [t2linux](https://t2linux.org) project and created by [everyone that contributed to to it](https://github.com/t2linux/linux-t2-patches/graphs/contributors).

## Disclaimer

This project is not officially provided or supported by the Fedora Project. The official Fedora software is available at [https://fedoraproject.org/](https://fedoraproject.org/). This project is not related to Fedora in any way.
