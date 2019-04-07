import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
stop_word_path = os.path.join(dir_path, 'English-Stop-Words.txt')

stop_words = []

f = open(stop_word_path, 'r')

for line in f:

    line = re.sub(r'[^a-zA-Z]', "", line)

    if len(line) == 0:
        continue
    stop_words.append(line)

f.close()

stop_word_dictionary = {}

f = open("model.txt", 'r')
print('writing to stop_word_stats.txt')
print('------------------------------------------------------------')
for line in f:
    line = line.split('\n')[0]
    if len(line) == 0:
        continue
    line = line.split('  ')

    word = line[1]
    if word not in stop_words:
        continue

    stop_word_dictionary[word] = {}
    stop_word_dictionary[word]['word'] = line[1]
    stop_word_dictionary[word]['freq'] = line[2] + line[4]
    stop_word_dictionary[word]['p_ham'] = line[3]
    stop_word_dictionary[word]['p_spam'] = line[5]


    print('%-20s' %(stop_word_dictionary[word]['word']), end="  ")
    print('%-10s' %(stop_word_dictionary[word]['freq']), end="  ")
    print('%-30s'%(stop_word_dictionary[word]['p_ham']), end="  ")
    print('%-25s'%stop_word_dictionary[word]['p_spam'])


f.close()
print('------------------------------------------------------------')


f = open("stop_word_stats.txt", 'w+')

total_spam_word_freq = 0
total_ham_word_freq = 0

f.write('%-20s  %-10s  %-30s  %-25s  %s'%("word", "freq", "P(word|ham)", "P(word|spam)", "classification"))
f.write('\n\n')
counter = 1
for word in stop_word_dictionary:
    f.write('%-4d  '%counter)
    f.write('%-20s  ' %(stop_word_dictionary[word]['word']))
    f.write('%-10s  ' %(stop_word_dictionary[word]['freq']))
    f.write('%-30s  '%(stop_word_dictionary[word]['p_ham']))
    f.write('%-25s  '%stop_word_dictionary[word]['p_spam'])

    p_ham = float(stop_word_dictionary[word]['p_ham'])
    p_spam = float(stop_word_dictionary[word]['p_spam'])

    classification = ""
    if(p_spam >= p_ham):
        classification = "SPAM"
        total_spam_word_freq += int(stop_word_dictionary[word]['freq'])
    else:
        classification = "HAM"
        total_ham_word_freq += int(stop_word_dictionary[word]['freq'])
    f.write(classification)


    f.write("\n")
    counter += 1

f.close()

print('total spam words occurance', total_spam_word_freq)
print('total ham words occurance', total_ham_word_freq)
