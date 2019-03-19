import os
from os import listdir
from os.path import isfile, join
from os import walk
import re
from math import log10

from spam_detection import word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam, probability_ham, probability_spam

# print(probability_ham)
# print(probability_spam)
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

def print_result(file_summary):
    f = open("baseline-result.txt", "w+")

    # calculate accuracy of the classification
    wrongCounter = 0
    rightCounter = 0

    counter = 0
    for file_name in file_summary:
        counter += 1
        print(counter, end="  ")
        print(file_name, end="  ")
        print(file_summary[file_name]["classification"], end="  ")
        print(file_summary[file_name]["ham_score"], end="  ")
        print(file_summary[file_name]["spam_score"], end="  ")
        print(file_summary[file_name]["result"])
        
        f.write(str(counter))
        f.write("  ")
        f.write(str(file_name))
        f.write("  ")
        f.write(str(file_summary[file_name]["classification"]))
        f.write("  ")
        f.write(str(file_summary[file_name]["ham_score"]))
        f.write("  ")
        f.write(str(file_summary[file_name]["spam_score"]))
        f.write("  ")
        f.write(str(file_summary[file_name]["result"]))
        f.write("\n")

        if file_summary[file_name]["result"] == "wrong":
            wrongCounter += 1
        elif file_summary[file_name]["result"] == "right":
            rightCounter += 1
        else:
            print("ERROR")
            break
    accuracy = rightCounter/(rightCounter + wrongCounter)
    print("--------------------------accurracy--------------------------")
    print(accuracy*100, ' % ')
    print("--------------------------accurracy--------------------------")

    f.close()


def getWords(file_path):
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
                ''' # I do not know if we allow for multiple words to show
                if word in result_words:
                    continue
                else:
                    result_words.append(word)
                '''
                result_words.append(word)
    f.close()
    return result_words
        
file_summary = {}
for file in testing_files:
    path_to_file = os.path.join(testing_path, file)
    words = getWords(path_to_file)

    classification = ""
    actual_classification = ""
    probability_email_spam = log10(probability_ham)
    probability_email_ham = log10(probability_spam)
    for word in words:
        if word not in word_dictionary:
            continue
        # need to calculate probabilities
        probability_email_spam += log10(p_spam[word])
        probability_email_ham += log10(p_ham[word])

    if probability_email_spam >= probability_email_ham:
        classification = "spam"
    else:
        classification = "ham"
    
    if file.find("ham") != -1:
        actual_classification = "ham"
    if file.find("spam") != -1:
        actual_classification = "spam"

    result = "wrong"
    if actual_classification == classification:
        result = "right"

    # lets make a file summary storing necessary info like ham score, spam score, .. etc so it can be easily outputted
    file_summary[file] = {}
    file_summary[file]['spam_score'] = probability_email_spam
    file_summary[file]['ham_score'] = probability_email_ham
    file_summary[file]['classification'] = classification
    file_summary[file]['actual_classification'] = actual_classification
    file_summary[file]['result'] = result


print_result(file_summary)