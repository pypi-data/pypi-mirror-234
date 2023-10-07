#!/bin/bash

# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common || exit

wine git config core.fileMode false

wine pip-install nox

exec wine python3.10 -m nox "$@"
