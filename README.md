# Freebox Player Custom Component for Home Assistant

Based on pure-python library, this custom component enables remote control on your Freebox Player devices.

This component is tested on Freebox Delta, but should work too on FreeBox Revolution, mini and crystal (feedsback will be appreciated)

## Features
* Supports On / Off 
* Supports changing channels
* Supports volume changes
* Supports navigation controls
* Even more incoming

## Still under developpment
This conponent use the old remote API, but since short time, Free is developping new API unrelated to remote (control player to open URL ect...)

## Configuration
Once installed, the Freebox Player component needs to be configured in order to work.

Edit `configuration.yaml` file and add the following:

```yaml
# Example configuration.yaml entry
freebox_player:
  remote_code: 00000000
  host: 192.168.0.xx
```

Where `remote_code` is the free authorization code for remote and `host` the ip of the player device.

### How to get the remote control code

Go to 
* `Freebox main menu` >> `Parameters` >> `General Information` For old box
* `Freebox main menu` >> `Réglage` >> `Systeme Information` For Delta 

## How to use the remote
Incomming... (only power on for now)