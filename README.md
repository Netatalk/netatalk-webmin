# netatalk-webmin
Webmin module for managing Netatalk

# Installation
- Install webmin by following the instructions at https://webmin.com/
- Generate a module tarball with `make dist`
- From the dir where webmin is installed, run `sudo ./install-module.pl /path/to/netatalk3-wbm.tgz`

# Configuration
- You may need to adjust the paths to the netatalk binary and afp.conf, as well as init commands, by editing the `config` file
