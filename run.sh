#!/bin/bash

if [  $# -ne 2 ]
then
    exename=$(basename $0)
    echo "Usage: $exename <path> <sleepiness>"
    echo "  Mounts an NFS server mirroring the given path with the given sleepiness level"
    echo "  The sleepiness is milliseconds to wait for each filesystem operation"
    echo "  Example:"
    echo "    $exename ~/test_directory 150"
    exit 1
fi

MIRRORED_PATH="$1"
SLEEPINESS="$2"
MOUNT_PATH=/tmp/mnt/sleepyfs

set -e
#set -x

sudo umount -f /private/tmp/mnt/sleepyfs 2>/dev/null > /dev/null || true
mkdir -p "${MOUNT_PATH}"
sudo launchctl start com.apple.rpcbind
#./server/srv.py -f path &
./server/srv.py -f tar -s "${SLEEPINESS}" &
SERVER_PID=$!

# Kill server if we die
function cleanup() {
    echo
    echo "Hang on, cleaning up"
    set -x
    sudo umount -f "${MOUNT_PATH}" || true
    kill -TERM "${SERVER_PID}"
}
trap cleanup TERM INT

echo "Launched NFS server with sleepiness ${SLEEPINESS} ms, now mounting..."
echo  "Server pid: ${SERVER_PID}"
sleep 2
sudo mount -t nfs -o noac -o port=12049 -o nfsvers=2 127.0.0.1:${MIRRORED_PATH} ${MOUNT_PATH}
echo "Mounted ${MIRRORED_PATH} at ${MOUNT_PATH}"
echo "Control-C to exit"
wait $pid
cleanup
