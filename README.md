# netatalk-webmin

Webmin module for managing Netatalk.

<img src="https://netatalk.io/gfx/webmin3_1.png" alt="Webmin Module screenshot" width="75%" height="auto">

It functions by parsing and modifying the afp.conf configuration file on the fly.

The netatalk service needs to be restarted or reloaded after modifying afp.conf for the new settings to take effect.

# Installation

If you don't have it installed already, install webmin itself by following the instructions at https://webmin.com/

## From release tarball

1. Download a [stable release tarball](https://github.com/Netatalk/netatalk-webmin/releases)
1. Multiple methods to install the module:
   * From the dir where webmin is installed, run `./install-module.pl /path/to/netatalk-wbm.tgz`
   * From within the Webmin UI: Configuration -> Modules -> From local file

## From source

1. Generate a module tarball with `make dist`
1. Run `sudo make install` (tested on Debian and Fedora)

# Configuration

You may need to adjust the paths to the netatalk binary and afp.conf, as well as init commands, by editing the `config` file.

The same thing can be accomplished within the Webmin UI, in the Netatalk module's Module config.

# See Also
- https://netatalk.io/docs/Webmin-Module
