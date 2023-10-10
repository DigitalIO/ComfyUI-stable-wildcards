# The MIT License (MIT)
#
# Copyright © 2023 Michael Wolfe (DigitalIO)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from .swnodes.StableWildcard import StableWildcard
from .swnodes.NonDynamicString import NondynamicString

# Nodes passed to ComfyUI.
# Node names must be unique
NODE_MAP = [
    {
        "name" : "Stable Wildcards",
        "class": StableWildcard,
        "disp" : "Stable Wildcard Output"
    },
    {
        "name" : "NonDynamic String",
        "class": NondynamicString,
        "disp" : "NonDynamic String"
    }
]

# Create the expected node maps for ComfyUI
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for x in NODE_MAP:
    x['class'].CATEGORY = 'StableWildcards'
    NODE_CLASS_MAPPINGS[x['name']] = x['class']
    NODE_DISPLAY_NAME_MAPPINGS[x['name']] = x['disp']
