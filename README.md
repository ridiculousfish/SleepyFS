### SleepyFS

SleepyFS is a tool used to create an unresponsive filesystem for testing purposes.

SleepyFS uses a user-space NFS server (based on [PineFS](http://www.panix.com/~asl2/software/Pinefs/)) to "mirror" a directory into another mount point. Operations on this filesystem are slowed down via an adjustable timeout.

SleepyFS currently runs on macOS only, but is designed to be compatible with Unix systems.

#### Usage

    run.sh <directory> <sleepiness_ms>

This re-mounts <directory> at the fixed path `/tmp/mnt/sleepyfs`, where filesystem operations are slowed down by the given sleepiness (expressed in milliseconds).

Note that the implementation creates a tarfile under the hood, so do NOT use this with large directories (`$HOME`, etc).
