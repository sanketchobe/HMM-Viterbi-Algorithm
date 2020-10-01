# HMM-Viterbi-Algorithm
Implementation of HMM/Viterbi algorithm for spelling error corrections

*HMM Implementation:

•	Hidden Markov Models are known for their application in Machine learning and Pattern recognition such as speech recognition, spelling corrector, bioinformatics etc.
•	Our HMM implementation is dealing with correcting the spelling errors introduced in a text and predict the accurate data from the observations in terms of corrupted text.
•	We can implement our project in 4 steps as follows:
1.	Corrupt the whole text with 10% or 20% of spelling errors introduced in the text.
2.	Divide Data into 80% of text as ‘Training Data’ and 20% of text as ‘Testing Data’.
3.	Calculating the probability of observing a character at each state of the HMM model.
4.	Calculating the initial probability of starting at each state and probability of transmission from one state to another.
5.	Implementing Viterbi algorithm to calculate the maximal path for the test data from the HMM build on training data.
6.	Calculate the accuracy of the predicted data based on the Precision and Recall measure.

*Text Corruption:

•	All the numbers or digits in the whole text are replaced with spaces and whole text is converted to lowercase characters.
•	To introduce the spelling errors in the text, one random character can be replaced with the original character based on the random number generated between 0.0 to 0.1.
•	For 26 alphabets (a to z), one character was assigned as a corruption-character which will be replaced with original character in text when a random number is generated between 0.0 to 0.1.
•	For ex: ‘a’ can be replaced with ‘z’, ‘b’ can be replaced with ‘v’ etc.
•	For first Training model, 10% of data can be corrupted by introducing misspelling when random number is generated between 0.0 to 0.1.
•	For second model, 20% of data can be corrupted by introducing misspelling when random number is generated between 0.0 to 0.2.

*Training HMM:

•	80% of the text is used as training data.
•	For training HMM, probability of output observation and probability of state transition needs to be estimated.
•	Probability of output observation can be estimated by counting the no of times of output character appears in the corrupted text dividing by the count on number of times character appears in original text.


•	Probability of state transition can be estimated by counting the no of times one state travels to another dividing the count on number of times character appears in original text.

*Testing HMM:

•	Remaining 20% of the text is used as Testing data.
•	We can use Viterbi algorithm to test the HMM designed to predict the correct data around the corrupted data.
•	For every character in the test data, we derive the maximal possible path or character that can be predicted using Viterbi algorithm.
•	All such maximal path characters lead to the predicted output or predicted data for corresponding test data observation.

*Precision and Recall:

•	Precision is ratio of actual correctly predicted instances to the sum of incorrectly predicted instances and correctly predicted instances.
•	Recall is ratio of actual correctly predicted instances to the total number of accurate instances.
•	For calculating Precision and Recall, we need to calculate number of True Positives (TP), True Negatives (TN), False Positives (FP) and False Negatives (FN).
•	True Positive is calculated when the original text is not same as corrupted text, but original text is same as predicted text i.e. Wrong -> Correct.
•	True Negative is calculated when original text is same as corrupted text and original text is same as predicted text i.e. Correct -> Correct.
•	False Positive is calculated when original text is same as corrupted text but original text is not same as predicted text i.e. Correct -> Wrong.
•	False Negative is calculated when original text is not same as corrupted text and original text is not same as predicted text i.e. Wrong -> Wrong.
•	Precision = TP / (TP + FP)
•	Recall =TP / (TP + FN)
•	Precision value of implementation is varying between 3% to 8% (for both model with 10% of corruption and 20% corruption).

*Model with Corruption %	Precision	Recall
9.385572843	3.4924330617	8.02377414562
18.7717114569	8.18144997975	8.94200973882
•	Recall value of implementation is varying between 7% to 9% (for both model with 10% of corruption and 20% corruption).
