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
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
from random import Random
import re


class StableWildcard:
    """
    ComfyUI Custom Node
    Implements wildcards using a stable seed to make workflows reproducible after creation
    """

    def __init__(self):
        pass

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Prompt String",)
    OUTPUT_NODE = False
    FUNCTION = "execute"

    # A reusable wildcard pattern matches any string with brackets {}
    # but will not select over other wildcards.
    WILDCARD_PATTERN = re.compile('{[^{}]+}')

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Without dynamicPrompts set to false ComfyUI will randomize our prompt before we get to it!
                "prompt":  ('STRING', {'default': '', 'multiline': True, 'dynamicPrompts': False}),
                "seed"  :  ('INT', {'default': 0, 'min': 0, 'max': sys.maxsize}),

                # Currently unused, but if a breaking change must be introduced
                # it can be used to provide backwards compatibility.
                "version": ([1], {'default': 1})
            },
            "hidden": {
                "id": "UNIQUE_ID",
                "png_info": "EXTRA_PNGINFO",
            },
            "optional": {}
        }

    def execute(self, prompt, seed, **kwargs):
        """
        Process wildcards using a seed to produce stable output.
        To achieve stable results a new random object is created
        using the given seed.
        """

        # Setup RNG
        rng = Random(int(seed))

        # Search & replace matches
        match = self.WILDCARD_PATTERN.search(prompt)
        while match:

            # Get the options - Remove the {}, split by | character
            # Because the search pattern requires at least one character,
            # ops is guaranteed to have at least one option
            ops = match.group()[1:-1].split('|')

            # Pick a random option.
            pick = ops[rng.randint(0, len(ops)-1)]

            # Replace the match and update the string
            # Limit one match incase there are repeated wildcards
            prompt = prompt.replace(match.group(), pick, 1)

            # Search for more wildcards
            match = self.WILDCARD_PATTERN.search(prompt)

        # Output result console
        print('\033[96m Stable Wildcard: ({}) "{}"\033[0m'.format(seed, prompt))

        # Save output into metadata if everything exists
        if 'id' in kwargs and 'png_info' in kwargs:
            id = kwargs['id']
            png_info = kwargs['png_info']

            # Check for workflow and extra
            if 'workflow' in png_info:
                workflow = png_info['workflow']

                # Create extra if missing
                if 'extra' not in workflow:
                    workflow['extra'] = {}

                # Create a namespace if necessary
                if 'stable-wildcards' not in workflow['extra']:
                    workflow['extra']['stable-wildcards'] = {}

                # Save the result in metadata by id
                workflow['extra']['stable-wildcards'][id] = prompt

            else:
                print('\033[96m Stable Wildcard: Workflow missing, output not saved in metadata\033[0m')

        else:
            print('\033[96m Stable Wildcard: Hidden input missing, output not saved in metadata\033[0m')

        return prompt,
