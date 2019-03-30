import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-ex2','--remove_stop_words', help='', action='store_true')
parser.add_argument('-ex3','--word_length_restriction', help='restricts the word to atleast 2 and at most 9', action='store_true')
parser.add_argument('-v','--verbose', help='print data outputted to file on screen', action='store_true')

args = parser.parse_args()

apply_stop_word = args.remove_stop_words
apply_word_length_restriction = args.word_length_restriction

model_output_file = ""
result_output_file = ""
if apply_stop_word is True and apply_word_length_restriction is False:
    print("--------------EXPERIMENT2: STOP WORD FILTERING--------------")
    model_output_file = "stopword-model.txt"
    result_output_file = "stopword-result.txt"
elif apply_word_length_restriction is True and apply_stop_word is False:
    print("--------------EXPERIMENT3 WORD LENGTH FILTERING--------------")
    model_output_file = "wordlength-model.txt"
    result_output_file = "wordlength-result.txt"
else:
    print("--------------CUSTOM EXPERIMENT--------------")
    model_output_file = input("enter a model output file: ")
    result_output_file = input("enter a result output file: ")

print(model_output_file)
print(result_output_file)
print("-----------------------------------------------------------")




import os
from os import listdir
from os.path import isfile, join
from os import walk
import re
from collections import defaultdict
# getting the current path
dir_path = os.path.dirname(os.path.realpath(__file__))

print("part3.py > Building Naive Bayes Classifier model")
stop_word_path = os.path.join(dir_path, 'English-Stop-Words.txt')


stop_words = []

f = open(stop_word_path, 'r')

for line in f:
    line = line.split('\n')[0]

    line = re.sub(r'[^a-zA-Z]', "", line)

    if len(line) == 0:
        continue

    stop_words.append(line)



training_path = os.path.join(dir_path, 'train')


'''
takes in a dictionary of key and vlues (words and frequencies)
and return dictionary with words in alphabetical order
'''
def alphabetical_sort(dictionary):
    result = {}
    dictionary.keys()
    sorted(dictionary.keys())
    for key in sorted(dictionary.keys()) :
        result[key] = dictionary[key]

    return result


def print_model(word_dict, ham_dict, spam_dict, p_ham, p_spam):
    f = open(model_output_file, "w+")
    counter = 0
    for word in word_dict:
        counter += 1
        if args.verbose is True:
            print(counter, end="  ")
            print(word, end="  ")
            print(ham_dict[word], end="  ")
            print(p_ham[word], end="  ")
            print(spam_dict[word], end="  ")
            print(p_spam[word])

        f.write(str(counter))
        f.write("  ")
        f.write(str(word))
        f.write("  ")
        f.write(str(ham_dict[word]))
        f.write("  ")
        f.write(str(p_ham[word]))
        f.write("  ")
        f.write(str(spam_dict[word]))
        f.write("  ")
        f.write(str(p_spam[word]))
        f.write("\n")
    f.close()


training_files = []
ham_training_files = []
spam_training_files = []

for (dirpath, dirnames, filenames) in walk(training_path):
    training_files.extend(filenames)


for i in training_files:
    if i.find("ham") != -1:
        ham_training_files.append(i)
    if i.find("spam") != -1:
        spam_training_files.append(i)


word_dictionary = {}
ham_word_dictionary = {}
spam_word_dictionary = {}
counter = 0


for file in ham_training_files:
    path_to_file = os.path.join(training_path, file)
    f = open(path_to_file)
    for line in f:
        line = line.lower()
        arr = re.split('\[\^a-zA-Z\]',line)
        #  arr = line.split()
        for x in arr:
            result = x.split('\n')
            # print(result[0])

            words = result[0].split(' ')

            word_counter = 1
            for word in words:


                word = re.sub(r'[^a-zA-Z]', "", word)

                if len(word) == 0:
                    continue

                if apply_word_length_restriction is True:
                    if len(word) <= 2 or len(word) >= 9:
                        continue

                if apply_stop_word is True:
                    if word in stop_words:
                        # print("word: ", word , " was stopped")
                        continue

                if word in word_dictionary:
                    x = word_dictionary[word]
                    x += 1
                    word_dictionary[word] = x
                else:
                    word_dictionary[word] = 1

                if word in ham_word_dictionary:
                    x = ham_word_dictionary[word]
                    x += 1
                    ham_word_dictionary[word] = x
                else:
                    ham_word_dictionary[word] = 1


                # make word is also added to spam if it does exist
                # and with 0 probability
                if word not in spam_word_dictionary:
                    spam_word_dictionary[word] = 0


                # print(word_counter, end=". ")
                # print(word, end=" |")
                # print(len(word))
                word_counter += 1

        # print(arr)

#    if counter == 0:
#        break

    counter += 1

for file in spam_training_files:
    path_to_file = os.path.join(training_path, file)
    f = open(path_to_file)
    for line in f:
        line = line.lower()
        arr = re.split('\[\^a-zA-Z\]',line)
        #  arr = line.split()
        for x in arr:
            result = x.split('\n')
            # print(result[0])

            words = result[0].split(' ')

            word_counter = 1
            for word in words:
                word = re.sub(r'[^a-zA-Z]', "", word)

                if len(word) == 0:
                    continue

                if apply_word_length_restriction is True:
                    if len(word) <= 2 or len(word) >= 9:
                        continue

                if apply_stop_word is True:
                    if word in stop_words:
                        # print("word: ", word , " was stopped")
                        continue


                if word in word_dictionary:
                    x = word_dictionary[word]
                    x += 1
                    word_dictionary[word] = x
                else:
                    word_dictionary[word] = 1

                if word in spam_word_dictionary:
                    x = spam_word_dictionary[word]
                    x += 1
                    spam_word_dictionary[word] = x
                else:
                    spam_word_dictionary[word] = 1

                # make word is also added to ham if it does exist
                # and with 0 probability
                if word not in ham_word_dictionary:
                    ham_word_dictionary[word] = 0

                # print(word_counter, end=". ")
                # print(word, end=" |")
                # print(len(word))
                word_counter += 1

        # print(arr)

#    if counter == 0:
#        break

    counter += 1


#print("len all = ", len(word_dictionary))
#print("len spam = ", len(spam_word_dictionary))
#print("len ham = ", len(ham_word_dictionary))



total_num_words = 0
for i in word_dictionary:
    # print(i, ' ' , word_dictionary[i])
    total_num_words += word_dictionary[i]

# print("total number of words:", total_num_words)


total_num_ham_words = 0
for i in ham_word_dictionary:
    # print(i, ' ' , ham_word_dictionary[i])
    total_num_ham_words += ham_word_dictionary[i]
# print("total number of ham words:", total_num_ham_words)


total_num_spam_words = 0
for i in spam_word_dictionary:
    # print(i, ' ' , ham_word_dictionary[i])
    total_num_spam_words += spam_word_dictionary[i]
# print("total number of spam words:", total_num_spam_words)

probability_ham = total_num_ham_words/total_num_words
probability_spam = total_num_spam_words/total_num_words

# print("------------------------------------------------")
# print("p(ham)", total_num_ham_words/total_num_words)
# print("p(spam)", total_num_spam_words/total_num_words)
# print("------------------------------------------------")

# the probabilities of each word in its set
p_spam = {}
p_ham = {}
p_word = {}

number_of_words = len(word_dictionary)
# and len(word_dictionary) = len(ham_word_dictionary) =  len(spam_word_dictionary)
# because we inserted every word into the other data category and assigned 0 if it did not exist

for i in ham_word_dictionary:
    p_ham[i] = (ham_word_dictionary[i]+0.5)/(total_num_ham_words+0.5*number_of_words)

for j in spam_word_dictionary:
    p_spam[j] = (spam_word_dictionary[j]+0.5)/(total_num_spam_words+0.5*number_of_words)

for k in word_dictionary:
    p_word[k] = (word_dictionary[k]+0.5)/(total_num_words+0.5*number_of_words)


word_dictionary = alphabetical_sort(word_dictionary)


print_model(word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam)


print("part3.py > Running Naive Bayes Classifier model")
print("-----------------------------------------------------------")

from math import log10


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
    f = open(result_output_file, "w+")

    # calculate accuracy of the classification
    wrongCounter = 0
    rightCounter = 0

    counter = 0
    for file_name in file_summary:
        counter += 1

        if args.verbose is True:
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

    accuracy = rightCounter/(rightCounter + wrongCounter)
    #print("--------------------------accurracy--------------------------")
    #print(accuracy*100, ' % ')
    #print("--------------------------accurracy--------------------------")

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

# is confusion matrix

confusion = [[0,0],[0,0]]

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

    # true positive
    if actual_classification=="spam" and classification=="spam":
        confusion[0][0] += 1

    # true negative
    if actual_classification=="ham" and classification=="ham":
        confusion[1][1] += 1

    # false positive
    if classification=="spam" and actual_classification=="ham":
        confusion[0][1] +=1

    # false negative
    if classification=="ham" and actual_classification=="spam":
        confusion[1][0] +=1

    # lets make a file summary storing necessary info like ham score, spam score, .. etc so it can be easily outputted
    file_summary[file] = {}
    file_summary[file]['spam_score'] = probability_email_spam
    file_summary[file]['ham_score'] = probability_email_ham
    file_summary[file]['classification'] = classification
    file_summary[file]['actual_classification'] = actual_classification
    file_summary[file]['result'] = result


print_result(file_summary)

print("confusion matrix")
print()
print('      SPAM |  HAM  ')
print('     --------------')
print('SPAM| %4d | %4d |'%(confusion[0][0], confusion[0][1]))
print('HAM | %4d | %4d |' %(confusion[1][0], confusion[1][1]))
print('     --------------')

true_positive = confusion[0][0]
false_positive = confusion[0][1]
false_negative = confusion[1][0]
true_negative = confusion[1][1]


total_emails = confusion[0][0] + confusion[0][1] + confusion[1][0] + confusion[1][1]
correctly_id_emails = confusion[0][0] + confusion[1][1]

accuracy = correctly_id_emails/total_emails
print("accuracy >> ", correctly_id_emails/total_emails)

percision = true_positive/(true_positive+false_positive)
print("percision >> ", percision )

recall = true_positive/(true_positive+false_negative)
print("recall >> ", recall)

f1 = 2*(percision*recall)/(percision+recall)
print("f1 >> ", f1)
print()
