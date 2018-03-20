from pprint import pprint
from Parser import Parser
import util
import operator
import string
import re
import numpy as np
import os
import nltk
from  collections import OrderedDict
class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    tfidVectors = [] 
   #Tidies terms
    parser=None


    def __init__(self, documents=[]):
        self.documentVectors=[]
        self.parser = Parser()
        if(len(documents)>0):
            self.build(documents)

    def build(self,documents):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.documentVectors = [self.makeVector(document) for document in documents]

#        print (self.vectorKeywordIndex)
#        print (self.documentVectors)


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string    
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
#    print query
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)

        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def tf_jaccard(self,searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)

        ratings = [util.binjaccard(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings
  

    def tf_idf_search(self,searchList):

        queryVector = self.buildQueryVector(searchList)
#        print (queryVector)
        self.tfidVectors = util.tf_idf(self.documentVectors)
#    print self.tfidVectors
        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.tfidVectors]
       
    # ratings = [util.cosine(queryVector, util.tf_idf(documentVectors)) for documentVector in self.documentVectors]
#        print(ratings)
        return ratings


    def tf_idf_jaccard(self,searchList):

        queryVector = self.buildQueryVector(searchList)
#        print (queryVector)
        self.tfidVectors = util.tf_idf(self.documentVectors)
#    print self.tfidVectors
        ratings = [util.binjaccard(queryVector,documentVector) for documentVector in self.tfidVectors]
        return ratings

  
    def tf_idf_jaccard_2(self, searchList1,searchList2):
        
        queryVector1 = self.buildQueryVector(searchList1)
#        print(queryVector1)
        queryVector2 = self.buildQueryVector(searchList2)
#        print(len(queryVector2))
        qV1_float = [float(i) for i in queryVector1]
        qV2_float = [float(i)*0.5 for i in queryVector2]
        queryVector = [ x + y for x, y in zip(qV1_float, qV2_float)]
 #       print("queryVector")
 #       print(len(queryVector))
  #      print(queryVctor)
        self.tfidVectors = util.tf_idf(self.documentVectors)
#        print("tfiidfV")
#        print(len(self.tfidVectors))
#        print(self.tfidfVectors)
        ratings = [util.binjaccard(queryVector,documentVector) for documentVector in self.tfidVectors]
        return ratings

#    def build_idf(self,documentVectors)
#    idfVectors = []
#    idfVectors = [np.array(documentVectors for

if __name__ == '__main__':
    #test data
    path = './documents/'
    result = []
    doc_id = []
    query = input("input your query: ")
    for filename in  os.listdir(path):
        f = open(os.path.join(path,filename),'r')
    #documents = open('wsm_essays_test.txt','w')
    #documents.write(f.read())
    #f.close()
        punc = (",./:'?&-")
        while True:
            line = f.read()
            if not line:break
            line = line.lower()
            line = line.replace('\r'," ")
#            line = re.sub('\s{2,}',' ',line)
            line = line.replace('\r\\\n',' ')
#            line = line.replace('/',' ')
#           line = line.replace('',' ')
#            line = line.replace(',',' ')
#            line = line.replace('?','')
#            line = line.replace('!','')
#            line = line.replace('-',' ')
#            line = line.replace(':::',' ')
#            line = line.replace("(",'')
#            line = line.replace(")",'')
 #           line = line.replace(";",'')
#            line = line.replace('.','')
#            transtable = {ord(c): None for c in punc}
#            line = line.translate(transtable)
            line = line.strip(' ')
#            line = line.replace('\"','')
            line = line.replace("^M\\n",'')
#            line = ' '.join(line.split())
#            line = re.sub(r'\d+', '', line)
            result.append(line)
            doc_id.append(os.path.splitext(filename)[0])
#    if not line: break
        f.close()
#    print (result[0])
#    print VectorSpace([result[23]])
#    print result[38]
#    print  VectorSpace([result[38]])
    output_d = VectorSpace(result)
    tf_cosine = {}
    all_tf_cosine = output_d.search([query])
#    print("all_tf_cosine")
#    print(all_tf_cosine)
#    print(len(all_tf_cosine))
    for i in range(0,len(all_tf_cosine),1):
      tf_cosine[i] = all_tf_cosine[i]
#      print(tf_cosine)
#      print(i)
#    print("tf_cosine")
#    print(tf_cosine)
    #tf_cosine_list = tf_cosine.keys()
    #tf_cosine_list.sort(reverse=True)
    tf_cosine_list = OrderedDict(sorted(tf_cosine.items(), key = lambda t:t[1], reverse=True ))
#    print("tf_cosine_list")
#    print(tf_cosine_list)
    j=0
    print ("Term Freauency (TF) Weighting + Cosine Similarity:")
    print ("\n")
    print ("DocID \t Score")
    for key in tf_cosine_list:
        j=j+1
        if j==6:break
        print ("%s \t %s" % (doc_id[key],tf_cosine[key]))
    print ("\n")

    tf_jaccard = {}
    all_tf_jaccard = output_d.tf_jaccard([query])
#    print("all_tf_jaccard")
#    print(all_tf_jaccard)
#    print(len(all_tf_jaccard))
    for i in range(0,len(all_tf_jaccard),1):
      tf_jaccard[i] = all_tf_jaccard[i]
 #     print(tf_jaccard)
 #     print(i)
 #   print("tf_jaccard")
 #   print(tf_jaccard)
#    tf_jaccard_list = tf_jaccard.keys()
#    tf_jaccard_list.sort(reverse=True)
    tf_jaccard_list = OrderedDict(sorted(tf_jaccard.items(), key=lambda t:t[1], reverse = True))
#    print("tf_jaccard_list")
#    print(tf_jaccard_list)
    j=0
    print ("Term Freauency (TF) Weighting + Jaccard Similarity:")
    print ("\n")
    print ("DocID \t Score")
    for key in tf_jaccard_list:
        j=j+1
        if j==6:break
        print ("%s \t %s" % (doc_id[key],tf_jaccard[key]))
    print ("\n")

    tf_idf_cosine = {}
    all_tf_idf_cosine = output_d.tf_idf_search([query])
    for i in range(0,len(all_tf_idf_cosine),1):
      tf_idf_cosine[i] = all_tf_idf_cosine[i]
#    tf_idf_cosine_list = tf_idf_cosine.keys()
#    tf_idf_cosine_list.sort(reverse=True)
    tf_idf_cosine_list = OrderedDict(sorted(tf_idf_cosine.items(), key=lambda t:t[1], reverse = True))
    j=0
    
    print ("TF-IDF Weighting + Cosine Similarity:")
    print ("\n")
    print ("DocID \t Score")
    for key in tf_idf_cosine_list:
        j=j+1
        if j==6:break
        print ("%s \t %s" % (doc_id[key],tf_idf_cosine[key]))
    print ("\n")


    tf_idf_jaccard = {}
    all_tf_idf_jaccard = output_d.tf_idf_jaccard([query])
    for i in range(0,len(all_tf_idf_jaccard),1):
      tf_idf_jaccard[i] = all_tf_idf_jaccard[i]
#    tf_idf_jaccard_list = tf_idf_jaccard.keys()
#    tf_idf_jaccard_list.sort(reverse=True)
    tf_idf_jaccard_list =  OrderedDict(sorted(tf_idf_jaccard.items(), key=lambda t:t[1], reverse = True))
    j=0

    print ("TF-IDF Weighting + Jaccard Similarity:")
    print ("\n")
    print ("DocID \t Score")
    for key in tf_idf_jaccard_list:
        j=j+1
        if j==6:break
        print ("%s \t %s" % (doc_id[key],tf_idf_jaccard[key]))

   #tf_cosine_top5 = dict(sorted(tf_cosine.iteritems(), key=operator.itemgetter(0),reverse=True)[:1])

#    print(list(tf_idf_jaccard_list)[0])
    index_doc=(list(tf_idf_jaccard_list)[0])    
#    print(type(doc_id[index_doc]))
    open_doc_str = doc_id[index_doc] + '.product'
#    print(open_doc_str)
    result2 = []
    query2 = ''
    query2_list = []
    g = open(os.path.join(path,open_doc_str), 'r')
    while True:
        line = g.read()
        if not line: break
#        line = line.lower()
#        line = line.replace('\r',' ')
#        line = line.replace('\r\\\n',' ')
#        line = line.replace('','')
        result2.append(line)
    g.close()
    sentence = result2[0]
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    for item in tagged:
        if item[1][0] == 'N' or item[1][0] == 'V':
            query2_list.append(item[0])
#    print(query2_list)
    for item in query2_list:
        query2 = item +' '+ query2
#    query2 = query2.replace('',)
#    print(query2)

    tf_idf_jaccard_2 = {}
#    print(output_d)
    all_tf_idf_jaccard_2 = output_d.tf_idf_jaccard_2([query], [query2])
    for i in range(0,len(all_tf_idf_jaccard_2),1):
      tf_idf_jaccard_2[i] = all_tf_idf_jaccard_2[i]
#    tf_idf_jaccard_list = tf_idf_jaccard.keys()
#    tf_idf_jaccard_list.sort(reverse=True)
    tf_idf_jaccard_list_2 =  OrderedDict(sorted(tf_idf_jaccard_2.items(), key=lambda t:t[1], reverse = True))
    j=0
    print ("\n")
    print ("Feedback Queries + TF-IDF Weighting + Jaccard Similarity:")
    print ("\n")
    print ("DocID \t Score")
    for key in tf_idf_jaccard_list_2:
        j=j+1
        if j==6:break
        print ("%s \t %s" % (doc_id[key],tf_idf_jaccard_2[key]))

   # pprint(output_d.search(["sport"]))
###################################################
