# netatalk-webmin
The official Webmin module for managing Netatalk 2.x.

<img src="https://netatalk.io/gfx/webmin2_1.png" alt="Webmin Module screenshot" width="75%" height="auto">

It functions by parsing and modifying the afpd.conf and AppleVolumes.default configuration files on the fly.

The afpd service needs to be restarted or reloaded for the new settings to take effect.

# Installation

If you don't have it installed already, install webmin itself by following the instructions at https://webmin.com/

## From release tarball

1. Download a [stable release tarball](https://github.com/Netatalk/netatalk-webmin/releases)
1. Multiple methods to install the module:
   * From the dir where webmin is installed, run `./install-module.pl /path/to/netatalk2-wbm.tgz`
   * From within the Webmin UI: Configuration -> Modules -> From local file

## From source

1. Generate a module tarball with `make dist`
1. Run `sudo make install` (tested on Debian and Fedora)

# Configuration
You may need to adjust the paths to the netatalk binaries and config files, as well as init commands, by editing the `config` file.

The same thing can be accomplished within the Webmin UI, in the Netatalk module's Module config.

# The current level of Netatalk 2 feature support
- Starting and stopping afpd and all AppleTalk services
- Interactive editor of all config files
- UI for all of the AppleVolumes.default options
- UI for a subset of afpd.conf options
- Connected user management

# Known limitations
- Editing afpd.conf through the form will remove options that are not supported by this module.
- When multiple shared volumes use the same path, there is confusion. Don't do this.

# Authors
- Matthew Keller
- Frank Lahm and the Netatalk Team, January 2010
- Steffan Cline, January 2011
- Daniel Markstedt, September 2023
