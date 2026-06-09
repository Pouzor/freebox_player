# Freebox Player — Custom Component for Home Assistant

Control your Freebox Player from Home Assistant, emulating the network remote
via the player's `remote_control` HTTP API.

## Compatibility

Works with the **classic players** (Révolution, Delta player, One, Crystal).

The **Freebox Pop** and **Mini 4K** run Android TV and do **not** expose this
API — use Home Assistant's built-in **Android TV Remote** integration for them.

## Configuration

Set up from the UI: **Settings → Devices & Services → Add Integration →
Freebox Player**, then enter the player's **host** (IP) and **remote control
code** (Player: *Réglages → Système → Informations → « Code télécommande
réseau »*).

## Usage

```yaml
service: freebox_player.remote
data:
  code: "power"      # or several: "1,2,3"
```

See the [README](https://github.com/Pouzor/freebox_player) for the full button
list and details.
