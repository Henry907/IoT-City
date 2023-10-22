docker run --rm -it --network=host --privileged --tmpfs /dev/shm:exec -v /run/udev:/run/udev:ro -e MTX_PATHS_CAM_SOURCE=rpiCamera bluenviron/mediamtx:latest-ffmpeg-rpi
