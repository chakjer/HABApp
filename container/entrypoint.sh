#!/bin/bash -x

set -euo pipefail

NEW_USER_ID=${USER_ID}
NEW_GROUP_ID=${GROUP_ID:-$NEW_USER_ID}

echo "Starting with habapp user id: $NEW_USER_ID and group id: $NEW_GROUP_ID"
if ! id -u habapp >/dev/null 2>&1; then
  if [ -z "$(getent group $NEW_GROUP_ID)" ]; then
    echo "Create group habapp with id ${NEW_GROUP_ID}"
    addgroup -g $NEW_GROUP_ID habapp
  fi
  echo "Create user habapp with id ${NEW_USER_ID}"
  adduser -u $NEW_USER_ID -D -g '' -h "${HABAPP_HOME}" -G habapp habapp
fi

chown -R habapp:habapp "${HABAPP_HOME}/config"
sync

exec "$@"
