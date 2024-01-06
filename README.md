# netatalk-webmin
The official Webmin module for managing Netatalk.

It functions by parsing and modifying the afpd.conf and AppleVolumes.default configuration files on the fly.

The afpd service needs to be restarted or reloaded for the new settings to take effect.

# Installation
- Install webmin by following the instructions at https://webmin.com/
- Generate a module tarball with `make dist`
- Multiple methods to install the module:
  - `make install` (only tested on Debian)
  - From the dir where webmin is installed, run `./install-module.pl /path/to/netatalk2-wbm.tgz`
  - From within the Webmin UI: Configuration -> Modules -> From local file

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
- Editing afpd.conf through the form will remove unsupported options
- When multiple shared volumes use the same path, there is confusion

# Authors
- Matthew Keller
- Frank Lahm and the Netatalk Team, January 2010
- Steffan Cline, January 2011
- Daniel Markstedt, September 2023
