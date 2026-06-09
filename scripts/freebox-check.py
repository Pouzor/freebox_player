#!/usr/bin/env python3
"""Diagnostic autonome de l'API Player Freebox (nouvelle API via le serveur).

But : confirmer que ton Player (ex. Freebox Pop) est bien exposé par le
serveur (Delta) avant d'implémenter quoi que ce soit dans l'intégration.

Ce script ne dépend que de la bibliothèque standard. Il :
  1. demande l'autorisation à la Freebox (à valider sur l'écran LCD),
  2. ouvre une session (challenge + HMAC-SHA1),
  3. liste les players (GET /api/v6/player),
  4. sauvegarde l'app_token dans .freebox-token.json (réutilisable).

Usage :
    python3 scripts/freebox-check.py            # host = mafreebox.freebox.fr
    python3 scripts/freebox-check.py 192.168.1.254
"""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

APP_ID = "fr.freebox.player.ha"
APP_NAME = "Home Assistant Freebox Player"
APP_VERSION = "2.0.0"
DEVICE_NAME = "Home Assistant"

TOKEN_FILE = Path(__file__).resolve().parent.parent / ".freebox-token.json"


def _call(host: str, method: str, path: str, body: dict | None = None,
          token: str | None = None) -> dict:
    url = f"http://{host}/api/v6{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("X-Fbx-App-Auth", token)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return json.loads(err.read())
    except urllib.error.URLError as err:
        sys.exit(f"❌ Connexion impossible à http://{host} : {err.reason}")


def get_app_token(host: str) -> str:
    if TOKEN_FILE.exists():
        saved = json.loads(TOKEN_FILE.read_text())
        if saved.get("host") == host and saved.get("app_token"):
            print(f"→ app_token réutilisé depuis {TOKEN_FILE.name}")
            return saved["app_token"]

    print("→ Demande d'autorisation à la Freebox...")
    res = _call(host, "POST", "/login/authorize/", {
        "app_id": APP_ID,
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "device_name": DEVICE_NAME,
    })
    if not res.get("success"):
        sys.exit(f"❌ authorize a échoué : {res}")

    app_token = res["result"]["app_token"]
    track_id = res["result"]["track_id"]

    print("\n⚠️  VA SUR L'ÉCRAN LCD DE LA FREEBOX ET APPUIE SUR ✓ (flèche droite)\n")
    while True:
        status = _call(host, "GET", f"/login/authorize/{track_id}")["result"]["status"]
        if status == "granted":
            print("✓ Autorisation accordée.")
            break
        if status in ("denied", "timeout", "unknown"):
            sys.exit(f"❌ Autorisation {status}.")
        print(f"   en attente... ({status})")
        time.sleep(2)

    TOKEN_FILE.write_text(json.dumps({"host": host, "app_token": app_token}, indent=2))
    print(f"→ app_token sauvegardé dans {TOKEN_FILE.name}")
    return app_token


def open_session(host: str, app_token: str) -> tuple[str, dict]:
    challenge = _call(host, "GET", "/login/")["result"]["challenge"]
    password = hmac.new(app_token.encode(), challenge.encode(), hashlib.sha1).hexdigest()
    res = _call(host, "POST", "/login/session/", {"app_id": APP_ID, "password": password})
    if not res.get("success"):
        sys.exit(f"❌ session a échoué : {res}")
    return res["result"]["session_token"], res["result"].get("permissions", {})


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "mafreebox.freebox.fr"
    print(f"Freebox host : {host}\n")

    app_token = get_app_token(host)
    session_token, permissions = open_session(host, app_token)

    print(f"\n→ Permissions accordées : {permissions}")
    if not permissions.get("player"):
        print("⚠️  La permission 'player' n'est PAS accordée.")
        print("   Freebox OS → Paramètres → Gestion des accès → Applications →")
        print(f"   '{APP_NAME}' → coche 'Modification des réglages du Player'.\n")

    print("\n→ GET /api/v6/player ...")
    res = _call(host, "GET", "/player/", token=session_token)
    if not res.get("success"):
        sys.exit(f"❌ Impossible de lister les players : {res}")

    players = res.get("result", [])
    if not players:
        print("❌ AUCUN player listé. Ta Pop n'est pas exposée par le serveur.")
        print("   (cf. FS#31235 — la nouvelle API ne pourra pas la piloter.)")
        return

    print(f"\n✅ {len(players)} player(s) trouvé(s) :\n")
    for p in players:
        flag = "✅" if (p.get("reachable") and p.get("api_available")) else "⚠️ "
        print(f"  {flag} id={p.get('id')}  {p.get('device_name')}  "
              f"stb={p.get('stb_type')}  api_version={p.get('api_version')}  "
              f"reachable={p.get('reachable')}  api_available={p.get('api_available')}")

    print("\nVerdict :")
    ok = [p for p in players if p.get("reachable") and p.get("api_available")]
    if ok:
        print("  → Pilotable par la nouvelle API. On peut coder l'intégration. 🎉")
    else:
        print("  → Player listé mais non joignable / API indispo. À creuser avant de coder.")


if __name__ == "__main__":
    main()
