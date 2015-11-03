In part I, I use the Naïve Bayes method to do text classification and use the “add-one-smoothing” to ensure the availability of result.

In part II, for the SVM-light, I create a feature vector for the vocabulary. And for each training file, I use the words occurring as the value corresponding to the existed feature. For the MEGAM,  I use the "bernoulli implicit" as the format for input file.

PART III
1.(1) spam analysis
SPAM:
precision:0.961
recall:0.956
f_score:0.959
HAM:
precision:0.984
recall:0.986
f_score:0.985

(2) sentiment analysis
POS:
precision:0.818
recall:0.691
f_score:0.749
NEG:
precision:0.732
recall:0.846
f_score:0.786

2.(1) SVM
a.Spam analysis
SPAM:
Accuracy on test set: 94.79% (1292 correct, 71 incorrect, 1363 total)
Precision/recall on test set: 96.50%/83.47%
HAM:
Accuracy on test set: 94.79% (1292 correct, 71 incorrect, 1363 total)
Precision/recall on test set: 94.28%/98.90%

b.sentiment analysis
POS： 
Accuracy on test set: 86.33% (6475 correct, 1025 incorrect, 7500 total)
Precision/recall on test set: 85.20%/87.95%
NEG:
Accuracy on test set: 86.33% (6475 correct, 1025 incorrect, 7500 total)
Precision/recall on test set: 87.54%/84.72%

(2) MEGAM
a. spam analysis 
HAM:
precision:0.838
recall:0.985
fscore:0.904
SPAM:
precision:0.918
recall:0.463
fscore:0.615

b.sentiment analysis
POS:
precision:0.752
recall:0.799
fscore:0.775
NEG:
precision:0.786
recall:0.736
fscore:0.759

3.I have tested the part I using 10% of the original training data and got the following results. After comparing, I found that the precision, recall and f-score are almost the same. Using more training data, it will get better performance,  but sometimes it won’t.  Therefore, in my opinion, there may be a threshold for the number of training data. The model we get will run better when the training data is growing under the threshold. After exceeding the threshold, there will be a more complex and bigger model so as to undermining the performance of the model we build.

(Using  10% training data:
SPAM:
precision:0.9476744186046512
recall:0.8980716253443526
f_score:0.9222065063649223
HAM:
precision:0.9636898920510304
recall:0.982
f_score:0.972758791480931
POS:
precision:0.8260729267505647
recall:0.6826666666666666
f_score:0.7475543875018251
NEG:
precision:0.729606907521018
recall:0.8562666666666666
f_score:0.787878787878787)




























