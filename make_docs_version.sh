#!/bin/bash

# Updates the Read the Docs configuration (docs/source/conf.py) with the
# current version from VERSION.txt and rebuilds the HTML documentation.
#
# Usage:
#   ./make_docs_version.sh          # update conf.py + rebuild docs
#   ./make_docs_version.sh --no-build   # update conf.py only

SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
VERSION_FILEPATH=${SCRIPT_PATH}/VERSION.txt
CONF_FILEPATH=${SCRIPT_PATH}/docs/source/conf.py
DOCS_DIR=${SCRIPT_PATH}/docs

# Read the current version
FULL_VERSION=$(cat ${VERSION_FILEPATH} | tr -d '[:space:]')
IFS=. read -r MAJOR_VERSION MINOR_VERSION PATCH_VERSION <<< "${FULL_VERSION}"

if [ -z "${MAJOR_VERSION}" ] || [ -z "${MINOR_VERSION}" ] || [ -z "${PATCH_VERSION}" ]; then
    echo "Error: Could not parse version from ${VERSION_FILEPATH}"
    exit 1
fi

echo "Current version: ${FULL_VERSION}"

# Update release in conf.py
if [ ! -f "${CONF_FILEPATH}" ]; then
    echo "Error: conf.py not found at ${CONF_FILEPATH}"
    exit 1
fi

echo "Updating ${CONF_FILEPATH}..."
sed -i "s/^release = .*/release = '${FULL_VERSION}'/" "${CONF_FILEPATH}"
echo "Set release = '${FULL_VERSION}' in conf.py"

# Rebuild docs unless --no-build is passed
if [ "$1" != "--no-build" ]; then
    echo ""
    echo "Rebuilding documentation..."
    cd "${DOCS_DIR}"
    make clean && make html
    echo ""
    echo "Documentation built successfully at ${DOCS_DIR}/build/html/"
fi

# Stage and commit
git add -A
git commit -m "updated docs version to ${FULL_VERSION}"
echo "Docs version updated to ${FULL_VERSION}"
