## Solution description

This repo contains the implementation of a basic spell checker.

Spell checker is implemented in python and java. Both implementations provide a command-line interface to check the spelling of input texts. The implementations use existing libraries/dictionaries to process the input data and form a list of possible corrections for all unknown words. Here unknown words are words not identified in the source dictionary. It is worth mentioning that this approach is not very accurate (since it allows both false positives and true negatives).

Spell checker ranks candidates using different measures of closeness (applied to a misspelled word and a candidate) as features. The ranking is performed based on the mean value of normalized features.

## Discussion

TODO
