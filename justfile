build-package arg:
    podman run --rm -it --privileged -v "$PWD":/repo:z ghcr.io/t2linux/fedora-ci:43 /repo/build-packages.sh {{arg}}
