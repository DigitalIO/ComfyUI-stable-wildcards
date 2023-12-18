/**
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
#*/

import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

/**
  Call the server to process the prompt and set it as the textarea title
*/
async function updateTitle(node, e) {
  const promptValue = node.widgets[0].element.value;
  const seedValue = node.widgets[1].value;

  // Get the resulting string from the server
  const response = await api.fetchApi(`/stable-wildcards/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({prompt: promptValue, seed: seedValue})
  });
  const data = await  response.json();

  // Update the title
  node.widgets[0].element.title = data['prompt'];
}

/**
  Change the title for the text area to include the loaded result
*/
function loadStableWildcardNode(node, app) {
  let wildcardData = app.graph.extra['stable-wildcards'];

  // Fallback to use the server on changes
  if (!wildcardData || !wildcardData[node.id]) {
    updateTitle(node, null);
    return;
  }
    
  // Change the title
  node.widgets[0].element.title = wildcardData[node.id];
}

/**
  Listen for prompt changes and update title
*/
function stableWildcardNodeCreated(node, app) {
  node.widgets[0].element.addEventListener(
    'change',
    updateTitle.bind(null, node),
    false
  );
}

// Create the Stable Wildcard extension
const StableWildcardsExtension = {
  name: 'StableWildcards',
  loadedGraphNode(node, app) {
    if (node.type !== "Stable Wildcards") {
      return;
    }
    loadStableWildcardNode(node, app);
  },
  nodeCreated(node, app) {
    if (node.comfyClass !== "Stable Wildcards") {
      return;
    }
    stableWildcardNodeCreated(node, app);
  }
}

// Register app
app.registerExtension(StableWildcardsExtension);