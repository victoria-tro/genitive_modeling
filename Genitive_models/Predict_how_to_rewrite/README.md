# Running the script and installing dependencies

This script allows you to predict the class for how to translate a -s genitive in Bokmål to the appropriate genitive form in Nynorsk. 

Note that the dataset is still small. It is based on the [Målfrid dataset](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-78/) at Språkbanken.

## How to run test_model.py

This scripts will let you test simple phrases to check how the classifier performs.

Go to the folder containing this script and run the command below in your terminal:

`python3 test_model.py`


## How to install dependencies and run classifier_kfold.py script

First, go to the folder containing the script in your terminal:

`cd path/to/script`

Then run these commands in the terminal to create your own classifier model:

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`python classifier_kfold.py`