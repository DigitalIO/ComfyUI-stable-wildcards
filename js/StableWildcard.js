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
  Change the title for the text area to include the loaded result
*/
function loadStableWildcardNode(node, app) {
  let wildcardData = app.graph.extra['stable-wildcards'];

  // Only act if there is data to act on
  if (!wildcardData || !wildcardData[node.id]) {
    console.log('No stable-wildcard data found');
    return;
  }
    
  // Change the title
  node.widgets[0].element.title = wildcardData[node.id];
}

/**
  Attach to the textarea and seed and update the title after every change
*/
function stableWildcardNodeCreated(node, app) {
  async function updateTitle(e) {
    
    const promptValue = node.widgets[0].element.value;
    const seedValue = node.widgets[1].value;
    
    // Get the resulting string from the server
    const response = await api.fetchApi(`/stable-wildcards/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({prompt: promptValue, seed: seedValue})
      });
    
    const data = await  response.json();
    
    node.widgets[0].element.title = data['prompt'];
  }
  
  // Add event listeners
  node.widgets[0].element.addEventListener(
    'change',
    updateTitle,
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