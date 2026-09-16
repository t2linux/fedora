build-package arg:
    podman run --rm -it --privileged -v "$PWD":/repo:z ghcr.io/t2linux/fedora-ci:45 /repo/build-packages.sh {{arg}}
