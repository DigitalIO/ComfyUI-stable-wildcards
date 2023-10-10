# ComfyUI Stable Wildcards
## Overview
ComfyUI has an amazing feature that saves the workflow to reproduce an image in the image itself. In theory, you can
import the workflow and reproduce the exact image. Unfortunately, this does not work with wildcards. The goal of this
node is to implement wildcard support using a seed to stabilize the output to allow greater reproducibility. 

## Use
### Wildcards
Wildcards are supported via brackets and pipes. 

Example:

`A painting of a {boat|fish} in the {sea|lake}`

The first pair of words will randomly select `boat` or `fish`, and the second will either be `sea` or `lake`. 
The following is a list of possible random output using the above prompt:

* A painting of a boat in the sea
* A painting of a boat in the lake
* A painting of a fish in the sea
* A painting of a fish in the lake

_Note:_ Everything including the brackets are replaced with the final word. 
Include spaces around your ` {} ` to prevent words from running together, or use it 
to modify words.
Ex: `{cat|dog}fish` outputs `catfish` or `dogfish`. 

### Node
The node requires three inputs
1) a string - Your prompt
2) a seed - This is what makes your prompt reproducible
3) a version - Allows for future changes to not break backwards compatibility

The node has one output
1) a string - Your final prompt with wildcards processed

### Bonus Node
An additional node is included that disabled the default dynamicPrompt behavior of multiline inputs.

## Opinions
Below are *my opinions* and as such will probably not be changed.

### CLIP
Many other implementations combine this feature with the CLIP node. I chose not to do this to keep the wildcard code and 
CLIP implementation separate and more re-usable.

### Wildcard Files
Probably won't be implemented. Files are external to the workflow, so there is no guarantee that (1) the file exists on
another system and (2) the file content has not been modified. File wildcards are not an appropriate approach if you are 
looking to create repeatable output.