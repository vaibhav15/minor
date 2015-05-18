# -*- coding: utf-8 -*

#import regex
import re
import csv
import pprint
import nltk.classify

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
#end

#start process_line
def processLine(line):
    # process the lines
    
    #Convert to lower case
    line = line.lower()
    #Convert www.* or https?://* to URL
    line = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',line)
    #Convert @username to AT_USER
    line = re.sub('@[^\s]+','AT_USER',line)    
    #Remove additional white spaces
    line = re.sub('[\s]+', ' ', line)
    #Replace #word with word
    line = re.sub(r'#([^\s]+)', r'\1', line)
    #trim
    line = line.strip('\'"')
    return line
#end 

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(line, stopWords):
    featureVector = []  
    words = line.split()
    for w in words:
        #replace two or more with two occurrences 
        w = replaceTwoOrMore(w) 
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #ignore if it is a stopWord
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector    
#end

#start extract_features
def extract_features(line):
    line_words = set(line)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in line_words)
    return features
#end


#Read the lines one by one and process it



fpos = open('data/positive_keywords.txt', 'r')
fneg = open('data/negative_keywords.txt', 'r')
line1 = fpos.readline()
line2 = fneg.readline()

#train_words = csv.reader(open('data/training_dataset.csv', 'rb'), delimiter=',', quotechar='|')

stopWords = getStopWordList('data/stopwords.txt')
count = 0;
featureList = []
words = []

#print train_words

#for row in train_words:
#    sentiment = row[0]
#    line = row[1]
#    processedLine = processLine(line)
#    featureVector = getFeatureVector(processedLine, stopWords)
#    featureList.extend(featureVector)
#    words.append((featureVector, sentiment));
#end loop




while line1:
    sentiment = "positive"
    processedLine = processLine(line1)
    featureVector = getFeatureVector(processedLine, stopWords)
    featureList.extend(featureVector)
    words.append((featureVector, sentiment));
    line1 = fpos.readline()

while line2:
    sentiment = "negative"
    processedLine = processLine(line2)
    featureVector = getFeatureVector(processedLine, stopWords)
    featureList.extend(featureVector)
    words.append((featureVector, sentiment));
    line2 = fneg.readline()



#print featureList
# Remove featureList duplicates
featureList = list(set(featureList))



# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, words)


# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

# Test the classifier
test_word = """

"""

processedTestWord = processLine(test_word)
sentiment1 = NBClassifier.classify(extract_features(getFeatureVector(processedTestWord, stopWords)))
print "testWord = %s, sentiment = %s\n" % (test_word, sentiment1)
