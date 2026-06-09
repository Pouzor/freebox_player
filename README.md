# Freebox Player — Custom Component for Home Assistant

[![](https://img.shields.io/github/release/Pouzor/freebox_player/all.svg?style=for-the-badge)](https://github.com/Pouzor/freebox_player)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![](https://img.shields.io/github/license/Pouzor/freebox_player?style=for-the-badge)](LICENSE)

Control your **Freebox Player** from Home Assistant. This component emulates the
infrared remote over the network, using the player's `remote_control` HTTP API.

## Compatibility

This component targets the **classic Freebox Players** that expose the legacy
remote-control API. The newer Android-TV players (Pop, Mini 4K) do **not** expose
that API — use Home Assistant's built-in **[Android TV Remote][androidtv]**
integration for those instead (see [below](#freebox-pop--mini-4k)).

| Player | Supported here | How to control |
|--------|:--------------:|----------------|
| Freebox Révolution | ✅ | This component (remote code) |
| Freebox Delta (player) | ✅ | This component (remote code) |
| Freebox One / Crystal | ✅ | This component (remote code) |
| Freebox **Pop** | ❌ | [Android TV Remote][androidtv] (core integration) |
| Freebox **Mini 4K** | ❌ | [Android TV Remote][androidtv] (core integration) |

> The remote code lives on the **Player** (the TV box), not on the server. In a
> Delta-server + Pop-player setup, the player is a Pop → use Android TV Remote.

## Installation

### HACS

1. In HACS, go to **Integrations** and search for **Freebox Player**.
2. Install, then **restart Home Assistant**.
3. Configure it (see below).

## Configuration

Configuration is done through the UI.

1. **Settings → Devices & Services → Add Integration**.
2. Search for **Freebox Player**.
3. Enter the **Host** (IP address of the player) and the **remote control code**.

> YAML is deprecated. An existing `freebox_player:` block in `configuration.yaml`
> is imported automatically on the next restart; you can then remove it.

### How to find the remote control code

On the Player: **Main menu → Réglages → Système → Informations** → line
**« Code télécommande réseau »** (8 digits).

## Usage

Call the `freebox_player.remote` service with a `code`:

```yaml
service: freebox_player.remote
data:
  code: "power"
```

### Sending several codes

Separate codes with a comma to send a sequence (e.g. channel `123`):

```yaml
service: freebox_player.remote
data:
  code: "1,2,3"
```

## Freebox Pop / Mini 4K

These run **Android TV** and ignore the legacy remote API. Control them with the
official **[Android TV Remote][androidtv]** integration — it gives directional
keys, power, volume, media and app launching (more than this component does):

1. **Settings → Devices & Services → Add Integration → Android TV Remote**.
2. Enter the player's **IP address**.
3. Type the **pairing code shown on the TV**.

```yaml
service: remote.send_command
target:
  entity_id: remote.freebox_player_pop
data:
  command: "DPAD_UP"   # DPAD_CENTER, BACK, HOME, POWER, ...
```

[androidtv]: https://www.home-assistant.io/integrations/androidtv_remote/

## Button list

* "red" — Bouton rouge
* "green" — Bouton vert
* "blue" — Bouton bleu
* "yellow" — Bouton jaune
* "power" — Power
* "list" — Liste des chaînes
* "tv" — TV
* "1" … "9", "0" — Pavé numérique
* "back" — Retour
* "swap" — Swap
* "info" — Info
* "epg" — EPG (fct+)
* "mail" — Mail
* "media" — Media (fct+)
* "help" — Help
* "options" — Options (fct+)
* "pip" — PiP
* "vol_inc" / "vol_dec" — Volume +/-
* "ok" — OK
* "up" / "down" / "left" / "right" — Navigation
* "prgm_inc" / "prgm_dec" — Programme +/-
* "mute" — Sourdine
* "home" — Free
* "rec" — Enregistrement
* "bwd" — Retour arrière (<<)
* "prev" — Précédent (|<<)
* "play" — Lecture / Pause
* "fwd" — Avance rapide (>>)
* "next" — Suivant (>>|)
* "replay", "vod", "whatson", "records", "youtube", "radios", "canalvod", "netflix"

## Development

Local Home Assistant in Docker with this integration mounted:

```bash
./scripts/dev-ha.sh          # start HA at http://localhost:8123, follow logs
./scripts/dev-ha.sh restart  # pick up code edits
./scripts/dev-ha.sh stop
```

Run the tests:

```bash
pip install -r requirements_test.txt
pytest
```

Diagnose whether a player exposes the Freebox Player API (useful for Pop owners):

```bash
python3 scripts/freebox-check.py
```
