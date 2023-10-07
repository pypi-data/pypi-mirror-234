# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from no_vtf.main import main_command
from no_vtf.task_runner import TaskRunner


def _main() -> None:
    TaskRunner.initialize()

    main_command()


if __name__ == "__main__":
    _main()
