# genitive_modeling
A bunch of scripts to predict genitive constructions in translations between bokmål and nynorsk.

# Genitive models

## Predicts_if_genitives

This script will predict if a sentence contains an s-genitive in Bokmål.

Current mean score using k-fold cross validation: 0.9559866962305986

The training data is based on the [Målfrid corpus](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-69/#corpus-info) and was manually tagged.

## Predicts_if_rewrites

This script will predict if a sentence that contains an s-genitive in Bokmål should have that construction rewritten in Nynorsk.

Current mean score using k-fold cross validation: 0.852496537279146

The training data is based on the [Målfrid corpus](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-69/#corpus-info) and was manually tagged.

## Predict_how_to_rewrite

This script will predict how a phrase in Bokmål that contains an -s genitive should be rewritten in Nynorsk.

Current mean score using k-fold cross validation: 0.51098901098901

The training data is based on the [Målfrid corpus](https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-69/#corpus-info) and was manually tagged.