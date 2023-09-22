# netatalk-webmin
Webmin module for managing Netatalk.

It functions by parsing and modifying the afp.conf configuration file on the fly.

The netatalk service needs to be restarted or reloaded after modifying afp.conf for the new settings to take effect.

# Installation
- Install webmin by following the instructions at https://webmin.com/
- Generate a module tarball with `make dist`
- Multiple methods to install the module:
  - `make install` (only tested on Debian)
  - From the dir where webmin is installed, run `./install-module.pl /path/to/netatalk3-wbm.tgz`
  - From within the Webmin UI: Configuration -> Modules -> From local file

# Configuration
You may need to adjust the paths to the netatalk binary and afp.conf, as well as init commands, by editing the `config` file.

The same thing can be accomplished within the Webmin UI, in the Netatalk module's Module config.
