import os
from os import listdir
from os.path import isfile, join
from os import walk
import re
from collections import defaultdict
# getting the current path
dir_path = os.path.dirname(os.path.realpath(__file__))


training_path = os.path.join(dir_path, 'train')


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


                # print(word_counter, end=". ")
                # print(word, end=" |")
                # print(len(word))
                word_counter += 1

        # print(arr)

#    if counter == 0:
#        break

    counter += 1

p_spam = {}
p_ham = {}
p_word = {}

total_num_words = 0
for i in word_dictionary:
    # print(i, ' ' , word_dictionary[i])
    total_num_words += word_dictionary[i]

print("total number of words:", total_num_words)


total_num_ham_words = 0
for i in ham_word_dictionary:
    # print(i, ' ' , ham_word_dictionary[i])
    total_num_ham_words += ham_word_dictionary[i]
print("total number of ham words:", total_num_ham_words)


total_num_spam_words = 0
for i in spam_word_dictionary:
    # print(i, ' ' , ham_word_dictionary[i])
    total_num_spam_words += spam_word_dictionary[i]
print("total number of spam words:", total_num_spam_words)

print("------------------------------------------------")
print("p(ham)", total_num_ham_words/total_num_words)
print("p(spam)", total_num_spam_words/total_num_words)
print("------------------------------------------------")


for i in ham_word_dictionary:
    p_ham[i] = ham_word_dictionary[i]/total_num_ham_words
    # print(i, '|', p_ham[i])

for j in spam_word_dictionary:
    p_spam[j] = spam_word_dictionary[j]/total_num_spam_words
    # print(i, '|', p_ham[i])

for k in word_dictionary:
    p_word[k] = word_dictionary[k]/total_num_words
