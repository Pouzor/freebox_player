#!/usr/bin/env bash
# Spin up Home Assistant in Docker with this integration mounted, for local
# testing of the HACS component.
#
# Usage:
#   ./scripts/dev-ha.sh           # start HA, follow logs
#   ./scripts/dev-ha.sh stop      # stop the container
#   ./scripts/dev-ha.sh restart   # restart container (picks up code edits)
#   ./scripts/dev-ha.sh logs      # tail logs
#   ./scripts/dev-ha.sh shell     # bash inside container
#
# After first start: open http://localhost:8123 -> onboard -> Settings ->
# Devices & Services -> Add Integration -> "Freebox Player".
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

COMPOSE_FILE="docker-compose.dev.yml"
SERVICE="homeassistant"

ensure_config_dir() {
  mkdir -p "$ROOT/dev-config"
  # Seed a minimal config the first time, with debug logging for this domain.
  if [[ ! -f "$ROOT/dev-config/configuration.yaml" ]]; then
    echo "→ Seeding dev-config/configuration.yaml..."
    cat >"$ROOT/dev-config/configuration.yaml" <<'YAML'
default_config:

logger:
  default: info
  logs:
    custom_components.freebox_player: debug
YAML
  fi
}

cmd_up() {
  ensure_config_dir
  echo "→ Starting Home Assistant container..."
  docker compose -f "$COMPOSE_FILE" up -d "$SERVICE"
  echo
  echo "✅ HA running at http://localhost:8123"
  echo "   Add the integration via Settings → Devices & Services → \"Freebox Player\"."
  echo "   Following logs (Ctrl+C to stop following — container keeps running)..."
  echo
  docker compose -f "$COMPOSE_FILE" logs -f "$SERVICE"
}

cmd_stop() {
  echo "→ Stopping container..."
  docker compose -f "$COMPOSE_FILE" down
}

cmd_restart() {
  echo "→ Restarting container (picks up code edits)..."
  docker compose -f "$COMPOSE_FILE" restart "$SERVICE"
  docker compose -f "$COMPOSE_FILE" logs -f "$SERVICE"
}

cmd_logs() {
  docker compose -f "$COMPOSE_FILE" logs -f "$SERVICE"
}

cmd_shell() {
  docker compose -f "$COMPOSE_FILE" exec "$SERVICE" /bin/bash
}

case "${1:-up}" in
  up|"")    cmd_up ;;
  stop)     cmd_stop ;;
  restart)  cmd_restart ;;
  logs)     cmd_logs ;;
  shell)    cmd_shell ;;
  *)
    echo "Unknown command: $1" >&2
    echo "Usage: $0 [up|stop|restart|logs|shell]" >&2
    exit 1
    ;;
esac
