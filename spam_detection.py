import os
from os import listdir
from os.path import isfile, join
from os import walk
import re
from collections import defaultdict

# getting the current path
dir_path = os.path.dirname(os.path.realpath(__file__))

# getting path of the training files
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

'''
prints the output to the file model.txt and optionally to the terminal

p_ham is probability of document being ham document
p_spam is probability of document being spam document
word_dictionary contains a list of all words
p_ham is a dictionay with the conditional probablities of all ham words
p_spam is a dictionay with the conditional probabilites of all spam words
'''
def print_result(word_dict, ham_dict, spam_dict, p_ham, p_spam):
    print_to_console = input("would you like to print file output to the console (0 for no 1 for yes) >")
    f = open("model.txt", "w+")
    counter = 0
    for word in word_dict:
        counter += 1
        if print_to_console == '1':
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

for (dirpath, dirnames, filenames) in walk(training_path):
    training_files.extend(filenames)

word_dictionary = {}
ham_word_dictionary = {}
spam_word_dictionary = {}

number_of_spam_documents = 0
number_of_ham_documents = 0

for file in training_files:
    if file.find("ham") != -1:
        number_of_ham_documents += 1
    if file.find("spam") != -1:
        number_of_spam_documents += 1

# the probabilty of document being ham or spam
probability_ham = number_of_ham_documents/(number_of_spam_documents+number_of_ham_documents)
probability_spam = number_of_spam_documents/(number_of_spam_documents+number_of_ham_documents)


for file in training_files:
    path_to_file = os.path.join(training_path, file)
    f = open(path_to_file, 'r', encoding="latin-1")
    for line in f:
        line = line.lower()
        # print(line, end=" -> ")
        words = re.split('[^a-zA-Z]',line)
        # print(words)
        for word in words:
            # print(word , end=" - >")
            # print(word)

            if len(word) == 0:
                continue


            if word in word_dictionary:
                x = word_dictionary[word]
                x += 1
                word_dictionary[word] = x
            else:
                word_dictionary[word] = 1

            # if the file is a ham file
            if file.find("ham") != -1:
                # if the word is already in the ham dictionary increment the frequency
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

            # if the file is a spam file
            if file.find("spam") != -1:
                # if the word is already in spam dictionary increment the frequency
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


# count the total frequency of words in both ham and spam files
total_num_words = 0
for i in word_dictionary:
    total_num_words += word_dictionary[i]

# print("total number of words:", total_num_words)

# count the total frequency of ham words only ham files
total_num_ham_words = 0
for i in ham_word_dictionary:
    total_num_ham_words += ham_word_dictionary[i]

# count the total frequency of spam words only in spam files
total_num_spam_words = 0
for i in spam_word_dictionary:
    total_num_spam_words += spam_word_dictionary[i]


# the probabilities of each word in its set
p_spam = {}
p_ham = {}

# total number of unique words
number_of_words = len(word_dictionary)
# and len(word_dictionary) = len(ham_word_dictionary) =  len(spam_word_dictionary)
# because we inserted every word into the other data category and assigned 0 if it did not exist

# dictionary of ham word probabilites
for i in ham_word_dictionary:
    p_ham[i] = (ham_word_dictionary[i]+0.5)/(total_num_ham_words+0.5*total_num_words)

# dictionary of spam word probabilites
for j in spam_word_dictionary:
    p_spam[j] = (spam_word_dictionary[j]+0.5)/(total_num_spam_words+0.5*total_num_words)

# sorts the word dictionary alphabetically
word_dictionary = alphabetical_sort(word_dictionary)

if __name__ == "__main__":
    print_result(word_dictionary, ham_word_dictionary, spam_word_dictionary, p_ham, p_spam)

    print("-----------------")
    print("number_of_spam_documents:", number_of_spam_documents)
    print("number_of_ham_documents:", number_of_ham_documents)
    print("P(spam):", probability_spam)
    print("P(ham):", probability_ham)
    print("total_num_ham_words:", total_num_ham_words)
    print('total_num_spam_words:',total_num_spam_words)
    print("-----------------")
