#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:18:08 2017

@author: sanketchobe
"""
"""
Import Laibraries for StemmerPorter and Word Tokenizer
"""
import argparse
import numpy as np
import math
import random

"""
Function Used to Corrupt the 10 or 20 % data by introducing misspelling 
"""
def corrupt_data(document, corrupt_text):
    N = len(document)
    count = 0
    max_limt =int(N/5)
    corrupt_doc = []
    corrupt_document =''
    
    for text in document:
        randm_no = np.random.random()
      #  if count == max_limt:
      #      corrupt_doc.append(text)
      #  else:
        if text in corrupt_text:
            if randm_no > 0.0 and randm_no <= 0.2 :
                 char =corrupt_text[text]
                 corrupt_doc.append(char)
                 count =count +1
            else:
                 corrupt_doc.append(text)
        else:
            corrupt_doc.append(text)
    
    corrupt_document =''.join(corrupt_doc)
    
    print 'Total text corruption %:', float(float(count)/float(len(document))) * 100

    return corrupt_document

"""
Function Used to Train the corrupt data to build HMM 
"""
def train_data(document, corrupt_document):
     
    i =0
    state_dictionary ={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    op1_dictionary ={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    op2_dictionary ={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    
    for i in range(len(document)):
        char1 =document[i]
        char2 = corrupt_document[i]
        if char1 in op1_dictionary.keys() and char2 in op2_dictionary.keys():
            state_dictionary[char1] =state_dictionary[char1] +1
            if char1 ==char2:
                if char1 in op1_dictionary.keys():
                    op1_dictionary[char1] = op1_dictionary[char1] +1
            else:
                if char2 in op2_dictionary.keys():
                    op2_dictionary[char2] = op2_dictionary[char2] +1
    
    return state_dictionary, op1_dictionary, op2_dictionary

def parse_options():
    optparser = argparse.ArgumentParser(description='Document Parser')
    optparser.add_argument(
        '-f', '--input_file',
        dest='filename',
        help='filename containing csv',
        required=True
    )
    optparser.add_argument(
        '-op', '--output_file',
        dest='outfilename',
        help='outfilename containing csv',
        required=True
    )
    return optparser.parse_args()

def main():
    options = parse_options()
    train_docs =[]
    test_docs =[]
    train_corrupt_docs =[]
    test_corrupt_docs =[]
    max_prob =[]
    delta_prob =np.zeros((1,26))
    prev_delta_prob =np.zeros((1,26))
    argmax_path =[]
    states =['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    state_trans ={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    
    special_char = [',','~','(',')','_','.',';','/','^','{','}','[',']']
    corrupt_text ={'a':'z','b':'v','c':'x','d':'f','e':'r','f':'t','g':'y','h':'j','i':'u',
                   'j':'n','k':'o','l':'p','m':'b','n':'h','o':'i','p':'w','q':'g','r':'e','s':'d',
                   't':'f','u':'c','v':'l','w':'q','x':'a','y':'h','z':'s'}
    initial_prob =np.zeros((1,26))
    symbol_prob =np.zeros((26,26))
    state_trans_matrix =np.zeros((26,26))
    
    f = open(options.filename, 'r')
    op = open(options.outfilename, 'w')
    
    documents = f.read()
    
    doc_len_limit = int(len(documents) * 0.8)
    #print 'doc_len_limit:', doc_len_limit
    
    for char in documents:  
        if char in special_char:
            documents =documents.replace(char, ' ')
        if char.isdigit():
            documents =documents.replace(char, ' ')

    documents = documents.lower()
    corrupt_document =corrupt_data(documents,corrupt_text)
    for k in range(len(documents)):
        if k <= doc_len_limit:
            train_docs.append(documents[k])
            train_corrupt_docs.append(corrupt_document[k])
        else:
            test_docs.append(documents[k])
            test_corrupt_docs.append(corrupt_document[k])
    
    train_docs =''.join(train_docs)
    train_corrupt_docs =''.join(train_corrupt_docs)
    test_docs =''.join(test_docs)
    test_corrupt_docs =''.join(test_corrupt_docs)
    print 'length of Original document:', len(documents)
    print 'length of Training docs:', len(train_corrupt_docs)
    state_dict, op1_dict, op2_dict = train_data(train_docs, train_corrupt_docs)
    
    #print 'state_dict:', state_dict
    for i in range(len(states)):
        if op1_dict[states[i]] >0 and op2_dict[states[i]]:
            total_trans =op1_dict[states[i]] + op2_dict[states[i]]
            initial_prob[0][i] =float(float(1)/float(total_trans))
        else:
            if op1_dict[states[i]] >0:
                total_trans =op1_dict[states[i]]
                initial_prob[0][i] =float(float(1)/float(total_trans))
            elif op2_dict[states[i]] > 0:
                total_trans =op2_dict[states[i]]
                initial_prob[0][i] =float(float(1)/float(total_trans))
            else:
                initial_prob[0][i] =float(0)
        total_trans = 0
    #print 'initial prob:', sum(initial_prob)

    i =0
    j =0
    k = 0
    for state, count1 in state_dict.items():
        symb1 = corrupt_text[state]
        for symb, count2 in op2_dict.items():
            if symb == symb1:
                symbol_prob[i,j] =float(float(count2 +1)/float((count1)+26))
                k = k +count2
            else:
                if symb ==state:
                   count2 =op1_dict[symb]
                   symbol_prob[i,j] =float(float(count2+1)/float((count1)+26))
                else:
                    symbol_prob[i,j] =float(float(1)/float((count1)+26))
            j = j+1
        j = 0
        i = i+1
    print 'Training corruption %:', float(float(k)/float(len(train_corrupt_docs))) * 100
   # print 'Training corrupt documents:', train_corrupt_docs
    
    i =0
    while i < len(train_corrupt_docs):
        if i > 0:
           # print 'checking prev_char:', prev_char, 'char:',char
            if ( prev_char not in states)  and (char in states):
                prev_char =train_corrupt_docs[i-1]
                char =train_corrupt_docs[i]
            else:
                if (prev_char in states) and (char not in states):
            #        print 'prev_char in states:', prev_char, 'char:',char
                    char =train_corrupt_docs[i]
                else:
                    prev_char =train_corrupt_docs[i-1]
                    char =train_corrupt_docs[i]              
        else:
            prev_char =' '
            char =train_corrupt_docs[i]
        if char in states:
           # if prev_char >'':
            if prev_char in states:
  #              print 'both chars in states'
                state_trans_matrix[states.index(prev_char)][states.index(char)]=state_trans_matrix[states.index(prev_char)][states.index(char)] +1
                state_trans[prev_char] =state_trans[prev_char] +1
             #   print 'prev_char:', prev_char, 'char:',char, 'state_trans[',prev_char,']:', state_trans[prev_char]
                i = i +1         
            else:
              #  print 'prev_char:', prev_char, 'char:',char
   #             print 'prev chars not in states'
                i = i +1
               # state_trans[char] =state_trans[char] +1
        else:
            if prev_char in states:
    #            print 'char not in states but prev char in states'
                state_trans[prev_char] =state_trans[prev_char] +1
               # print 'prev_char:', prev_char, 'char:',char,'state_trans[',prev_char,']:', state_trans[prev_char]
     #       else:
                #print 'prev_char:', prev_char, 'char:',char
            i = i+1
        
    #for i in range(len(train_corrupt_docs)):
    #    if i > 0:
    #        prev_char =train_corrupt_docs[i-1]
    #        char =train_corrupt_docs[i]
    #    else:
    #        prev_char =''
    #        char =train_corrupt_docs[i]
    #    if char in states:
    #        if prev_char >'':
    #            if prev_char in states:
    #                state_trans_matrix[states.index(char)][states.index(prev_char)]=state_trans_matrix[states.index(char)][states.index(prev_char)] +1
    ##                state_trans[char] =state_trans[char] +1
     #       else:
     #           state_trans[char] =state_trans[char] +1
    
    for key, value in state_trans.items():
        for item in states:
            state_trans_matrix[states.index(key)][states.index(item)] = float(float(state_trans_matrix[states.index(key)][states.index(item)] + 1)/float(value + 26))
    
    i =0
    j = 0
    for i in range(len(test_corrupt_docs)):
        char = test_corrupt_docs[i]
        if char in states:
            if i == 0:
                while j < 26:
                    if j >= 26:
                        break
                    else:
                        delta_prob[0,j] =float(np.log(initial_prob[0,j])) + float(np.log(symbol_prob[states.index(char),j]))
                        j = j+1
            else:
                j = 0
                prev_delta_prob = delta_prob
                while j < 26:
                    if j >= 26:
                        break
                    else:
                        for k in range(len(states)):
                            max_prob.append(prev_delta_prob[0,k] + np.log(state_trans_matrix[k,j]))
                        delta_prob[0,j] =max(max_prob) + np.log(symbol_prob[j,states.index(char)])
                        j = j+1
                        max_prob =[]
            indx1, indx2 =np.unravel_index(delta_prob.argmax(), delta_prob.shape)
            argmax_path.append(states[indx2])
        else:
            argmax_path.append(char)
            
    argmax_path =''.join(argmax_path)
    op.writelines('{}:{}\n'.format('Original Test Document',test_docs))
    op.writelines('{}\n'.format('================================================'))
    op.writelines('{}:{}\n'.format('Predicted Test Document',argmax_path))
    
    TP =0
    TN =0
    FP =0
    FN =0
    for i in range(len(test_docs)):
       # if test_docs[i] in states:
        if test_docs[i] == test_corrupt_docs[i]:
            if argmax_path[i] == test_docs[i]:
                 TN =TN +1
            else:
                 FP =FP +1
        else:
            if argmax_path[i] == test_docs[i]:
                TP =TP +1
            else:
                FN =FN +1
    if TP > 0 and FN > 0:           
        recall = (float(float(TP)/float(TP +FN))) * 100
    else:
        recall = 0
    
    if TP > 0 and FP > 0:
        precision = (float(float(TP)/float(TP +FP)))* 100
    else:
        precision =0
    
    accuracy = float(float(TP + TN)/float(TP + TN + FP + FN))
    
    print 'Observation prob:', symbol_prob
    print 'State trans no:', state_trans
    print 'State transition prob:', state_trans_matrix
    print 'TP:', TP,'TN:', TN,'FP:', FP,'FN:', FN,'\nPrecision:', precision,'\nRecall:', recall,'\n accuracy:', accuracy

    op.writelines('{}:{},{}:{},{}:{},{}:{}\n'.format('True Positive',TP,'False Negative',FN,'True Negative',TN,'False Positive',FP))
    op.writelines('{}:\n{}\n'.format('Precision %',precision))
    op.writelines('{}:\n{}\n'.format('Recall %',recall))
    
    f.close(),
    op.close()

if __name__ == '__main__':
    main()