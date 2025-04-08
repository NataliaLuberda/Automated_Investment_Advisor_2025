#!/bin/bash

# Usage: ./docker-commands.sh <action> <container>
# Example: ./docker-commands.sh restart app
# Example: ./docker-commands.sh logs mysql

ACTION="$1"
CONTAINER="$2"

if [ -z "$ACTION" ] || [ -z "$CONTAINER" ]; then
  echo "❌ Usage: $0 <action> <container>"
  echo "   Actions: build | restart | logs"
  echo "   Containers: app | mysql | all"
  exit 1
fi

if [ "$CONTAINER" == "all" ]; then
    CONTAINER=""
fi

case "$ACTION" in
  build)
    echo "🔨 Building $CONTAINER container(s)..."
    docker-compose up -d --no-deps --build ${CONTAINER:-}
    ;;

  restart)
    echo "🔄 Restarting $CONTAINER container(s)..."
    docker-compose restart ${CONTAINER:-}
    ;;

  logs)
    echo "📜 Showing logs for $CONTAINER..."
    docker-compose logs -f ${CONTAINER:-}
    ;;

  *)
    echo "❌ Invalid action. Use: build | restart | logs"
    exit 1
    ;;
esac
