# SPDX-FileCopyrightText: 2023 Mewbot Developers <mewbot@quicksilver.london>
#
# SPDX-License-Identifier: BSD-2-Clause

"""
Front end for the annotation script.
"""

import os
from functools import partial

from ..annotate import main as annotate_main

main = partial(annotate_main, search_root=os.getcwd())
