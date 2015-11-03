PART I

Commands example:

python perceplearn.py spam_training.txt spam_model.nb

python percepclassify.py spam_model.nb < spam_test.txt



PART II: part-of-speech tagging

Commands example:

python postrain.py pos.train pos_model.nb

python postag.py pos_model.nb < pos.dev > pos.test.out

No option is used.



PART III: named entity recognition

Commands example:

python nelearn.py ner.esp.train ner_model.nb

python netag.py ner_model.nb <ner.esp.dev > ner.esp.test.out

No option is used.


In part II and part III, the files: postrain.py and nelearn.py will not call the perceplearn.py; at the same time, postag.py and netag.py will not call the percepclassify.py. But the algorithms are almost the same. And the files:perceplearn.py and percepclassify.py could train and classify data which format is same as homework 1.



Part IV:

1.What is the accuracy of your part-of-speech tagging?

For development data:  

correct:36908

total:40117

accuracy: 0.920008973751776


2.What are the precision, recall and F-score for each of the named entity types for your named entity recognizer, and what is the overall F-score?

There are 5 named entity types: ORG, PER, MISC, LOC and O. We do not consider type O here.



For ORG:

precision:0.648989898989899
recall:0.6047058823529412
f_score:0.6260657734470159



For PER:

precision:0.9516806722689075
recall:0.3707037643207856
f_score:0.5335689045936396



For MISC:

precision:0.38443935926773454
recall:0.3775280898876405
f_score:0.380952380952381



For LOC:

precision:0.6158139534883721
recall:0.6727642276422764
f_score:0.6430305973773677



Overall F-score:

precision:0.646976483762598
recall:0.5311422661457136
f_score:0.5833648870377383



3.What happens if you use your Naive Bayes classifier instead of your perceptron classifier (report performance metrics)? Why do you think that is?

Use POS development data to make statements as following:

If we use Naive Bayes classifier, then the accuracy is :

correct:36188

total:40117

accuracy: 0.902061470199666

As for perceptron classifier, the accuracy on pos.dev data file is:

correct:36908

total:40117

accuracy: 0.920008973751776

After comparison, I should say that Perceptron classifier is often more accurate than   Naive Bayes classifier. Because Naive Bayes classifier builds a training model through counting data once and then giving predictions with the assumption that features are independent. However, perceptron classifier is aimed at mitaken-driven learning, not only looping throung data many times, but also take feature dependency into consideration.



