#!/bin/bash

# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

source builds/common || exit

chsh --shell /bin/bash

echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections

# prevent alias expansion of apt-get as this is installing its prerequisites
command sudo apt-get --quiet --quiet --yes install moreutils >/dev/null
