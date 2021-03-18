# Freebox Player Custom Component for Home Assistant

[![](https://img.shields.io/github/release/Pouzor/freebox_player/all.svg?style=for-the-badge)](https://github.com/Pouzor/freebox_player)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![](https://img.shields.io/github/license/Pouzor/freebox_player?style=for-the-badge)](LICENSE)

Based on pure-python library, this custom component enables remote control on your Freebox Player devices.

This component is tested on Freebox Delta, but should work too on Freebox Revolution and Crystal (feedsback will be appreciated).

It's doesn't works on Freebox mini 4K. This one doesn't have a remote code.


## Installation

### HACS Install

1. Search for `Freebox Player` under `Integrations` in the HACS Store tab.
2. **You will need to restart after installation for the component to start working.**
3. Configure the integation (see Configuration section)


## Features
* Supports On / Off 
* Supports changing channels
* Supports volume changes
* Supports navigation controls
* Even more incoming

## Still under developpment
This conponent use the old remote API, but since short time, Free is developping new API unrelated to remote (control player to open URL ect…)

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
* `Freebox main menu` >> `Réglages` >> `Systeme Information` For Delta 

## How to use the remote

To send remote code to the player, just call the service `freebox_player.remote` with the code in parameter: 
```yaml
code: "power"
```

### Mutiple code

If you want to send multiple code like `123` for example, you need to split each code with a comma :
```yaml
code: "1,2,3"
```

Or you call multiple times the service for each number (`1` && `2` && `3`)


## Button List

* "red" // Bouton rouge
* "green" // Bouton vert
* "blue" // Bouton bleu
* "yellow" // Bouton jaune

* "power" // Bouton Power
* "list" // Affichage de la liste des chaines
* "tv" // Bouton tv

* "1" // Bouton 1
* "2" // Bouton 2
* "3" // Bouton 3
* "4" // Bouton 4
* "5" // Bouton 5
* "6" // Bouton 6
* "7" // Bouton 7
* "8" // Bouton 8
* "9" // Bouton 9

* "back" // Bouton jaune (retour)
* "0" // Bouton 0
* "swap" // Bouton swap

* "info" // Bouton info
* "epg" // Bouton epg (fct+)
* "mail" // Bouton mail
* "media" // Bouton media (fct+)
* "help" // Bouton help
* "options" // Bouton options (fct+)
* "pip" // Bouton pip

* "vol_inc" // Bouton volume +
* "vol_dec" // Bouton volume -

* "ok" // Bouton ok
* "up" // Bouton haut
* "right" // Bouton droite
* "down" // Bouton bas
* "left" // Bouton gauche

* "prgm_inc" //Bouton programme +
* "prgm_dec" // Bouton programme -

* "mute" // Bouton sourdine
* "home" // Bouton Free
* "rec" // Bouton Rec

* "bwd" // Bouton << retour arrière
* "prev" // Bouton |<< précédent
* "play" // Bouton Lecture / Pause
* "fwd" // Bouton >> avance rapide
* "next" // Bouton >>| suivant
