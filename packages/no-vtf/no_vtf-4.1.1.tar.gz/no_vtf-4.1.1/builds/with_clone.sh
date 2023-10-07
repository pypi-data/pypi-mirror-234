#!/bin/bash

# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common || exit

[ -n "$1" ]

cd "$(mktemp --directory)"
git clone --quiet --no-checkout "$OLDPWD" .
git checkout --quiet HEAD

exec "$@"
