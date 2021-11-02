## Solution description

This repo contains the implementation of a basic spell checker.

Spell checker is implemented in python and java. Both implementations provide a command-line interface to check the spelling of input texts. The implementations use existing libraries/dictionaries to process the input data and form a list of possible corrections for all unknown words. Here unknown words are words not identified in the source dictionary. It is worth mentioning that this approach is not very accurate (since it allows both false positives and true negatives).

Spell checker ranks candidates using different measures of closeness (applied to a misspelled word and a candidate) as features. The ranking is performed based on the mean value of normalized features.

## Discussion

### What I didn't do

* First of all, I apologize in advance for the quality of java code: I haven't used it for 3+ years :)
* Secondly, for both implementations, I didn't perform any analysis on the achieved scores. It would be great to evaluate the implemented models (to tune the features set/perform feature engineering/adjust the solution method).
* Additionally, I think that it makes sense to try trainable / more sophisticated approaches. The implemented ranking is **really** simple.

### Java vs Python

Python has a very comprehensive set of libraries. The complexity of the solution is not limited by it in any way. It allows simple integration of all the desirable state-of-the-art models and techniques. Powerful libraries (such as, for instance, `numpy`) provide extremely usable interfaces for data processing. In other words, the complexity of the solution is limited only by your knowledge/resources. Even though there may be other potential benefits of using different programming languages (for instance, in terms of the execution speed), the coding process in python is smooth and satisfactory.

Implementation in Java was harder for me. However, I didn't finish it (a set of features implemented in Java is a subset of the set in Python). I also may be biased since I used Python much more frequently lately.

I noticed the following inconveniences:
* Lack of some libraries (on the contrary, for Python, there often are multiple libraries available);
* Work with arrays is much more comfortable in Python;
* Most of the Python libraries used by me are regularly updated. In the case of Java, I encountered some issues related to the outdated/deprecated parts of libraries.

It is worth mentioning that, perhaps, in principle, Java usage for ML purposes isn't such a bad thing. Nevertheless, due to the simplicity, compatibility, and some other reasons, Python is the general programming language for ML. And it is one of the reasons why the new libraries for ML primarily appear for Python.
