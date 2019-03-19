import os
from os import listdir
from os.path import isfile, join
from os import walk
import re

from spam_detection import word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam, probability_ham, probability_spam

print(probability_ham)
print(probability_spam)
# print(len(word_dictionary))
# print(len(ham_word_dictionary))
# print(len(spam_word_dictionary))
# print(len(p_ham))
# print(len(p_spam))

# getting the current path
dir_path = os.path.dirname(os.path.realpath(__file__))

testing_path = os.path.join(dir_path, 'test')


testing_files = []
ham_testing_files = []
spam_testing_files = []

for (dirpath, dirnames, filenames) in walk(testing_path):
    testing_files.extend(filenames)

for i in testing_files:
    if i.find("ham") != -1:
        ham_testing_files.append(i)
    if i.find("spam") != -1:
        spam_testing_files.append(i)

def getWordAndFrequencies(file_path):
    result_words = []

    f = open(file_path, 'r', encoding="latin-1")
    for line in f:
        line = line.lower()
        # tokenizing the line. returns an array of lines ending by \n
        arr = re.split('\[\^a-zA-Z\]',line)

        for x in arr:
            # remove the \n at the end of every string
            result = x.split('\n')
            # print(result[0])

            # split the result on the empty space
            words = result[0].split(' ')

            for word in words:
                word = re.sub(r'[^a-zA-Z]', "", word)

                # ignore the word if there is no word on that line 
                # a line was only skipped
                if len(word) == 0:
                    continue
                
                # is the word is already in our result dictionay increment frequency
                # else set frequency to 1
                '''
                if word in result_words:
                    result_words[word] += 1
                else:
                    result_words[word] = 1
                '''
                result_words.append(word)
    f.close()
    return result_words
        
file_summary = {}
for file in testing_files:
    path_to_file = os.path.join(testing_path, file)
    words = getWordAndFrequencies(path_to_file)


    probability_email_spam = 0
    probability_email_ham = 0
    for word in words:
        if word not in word_dictionary:
            continue
        # need to calculate probabilities
    # lets make a file summary storing necessary info like ham score, spam score, .. etc so it can be easily outputted
    file_summary[file] = {}
    file_summary[file][]
    print(words)