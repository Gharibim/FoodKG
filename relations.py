'''
Here we use our retrained model STM to predict the relation between each two concepts. 
If there is a relation between two subjects the we check the similarity between them 
'''

import os
import time
import itertools
import re
import entityEtra

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

relationToUse = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
mainSim, hashOut = 0, 0
subToUse, objToUse = '', ''
words_to_use = ''
Universal_rel = ''

# Write a triple after predicting the relation between the subject and object
def write_Relation(subject, object, writer, sub1, sub2, context):
    global mainSim
    global hashOut
    global Universal_rel
    from prepare_Models import predict_Relationship
    to_write = predict_Relationship(subject, object)
    relation = to_write
    Universal_rel = relation
    s = "/".join(sub1.split('/')[:-1])
    o = "/".join(sub2.split('/')[:-1])
    writer.write('<{}> <{}{}> <{}> <{}> .'.format(s + '/' + subject.capitalize(), relationToUse, relation,
                                                  o + '/' + object.capitalize(), context))
    writer.write("\n")


# Return the semantic similarity between the subject and the object
def calSimilarity(subject, object, writer, sub1, sub2, context):
    global mainSim
    global hashOut
    global Universal_rel
    try:
        write_Relation(subject, object, writer, sub1, sub2, context)
    except Exception as e:
        pass


# A wrapper function for the semantic similarity
def checkSim(f, s):
    from prepare_Models import get_Similarity
    return get_Similarity(f, s)

# Check the similarity When there is a list of words instead of 2
def check_Words(extractedSub, extractedObj):
    min_similarity = 0
    sub_toWrite = obj_toWrite = ''
    for ind, first in enumerate(extractedSub):
        for index, second in enumerate(extractedObj):
            temp_sim = checkSim(first, second)
            if temp_sim > min_similarity:
                min_similarity = temp_sim
                sub_toWrite = first
                obj_toWrite = second
    words_to_use = [sub_toWrite, obj_toWrite]
    return words_to_use


def readFile(fileName, context):
    global words_to_use
    start_time = time.time()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    try:
        reader = open(fileName, "r")
        writer = open('output.nq', 'w+')
    except Exception as e:
        print(e)
    else:
        parity = itertools.cycle([True, False])
        for line in reader:
            line = line.replace('%20', ',').replace('%2C', ',')
            if line.startswith("_:"):
                writer.write('{} <{}> .'.format(line.strip().rstrip(' .'), context))
                writer.write('\n')
                continue
            if line.isspace():
                continue
            if next(parity):
                line1 = line
                writer.write('{} <{}> .'.format(line1.strip().rstrip(' .'), context))
                writer.write('\n')

                line1 = re.findall('<([^>]*)>', line)
                if len(line1) == 3:
                    sub_line1, rel_line1, obj_line1 = line1[0], line1[1], line1[2]

                elif len(line1) == 2:
                    sub_line1, rel_line1 = line1[0], line1[1]
                    obj_line1 = re.findall('"([^"]*)"', line)[0]

                else:
                    pass

                finalSub = ''
                sub1 = sub_line1
                sub_line1 = sub_line1.split('/')[-1].upper()
                try:
                    extractedSub = entityEtra.get_continuous_chunks(sub_line1.upper())
                    extractedSubLength = len(extractedSub)
                except Exception as e:
                    print(e)
                else:
                    # print("NLTK works perfectly")
                    if extractedSubLength == 0:
                        pass
                    elif extractedSubLength == 1:
                        finalSub = extractedSub[0]
                    else:
                        writer.write(
                            '<{}> <{}isA> <{}> <{}> .'.format(sub1, relationToUse,
                                                              '/'.join(sub1.split('/')[:-1]) + '/' + ','.join(
                                                                  extractedSub),
                                                              context))
                        writer.write('\n')


            else:
                line2 = line
                writer.write('{} <{}> .'.format(line2.strip().rstrip(' .'), context))
                writer.write('\n')

                line2 = re.findall('<([^>]*)>', line)
                if len(line2) == 3:
                    sub_line2, rel_line2, obj_line2 = line2[0], line2[1], line2[2]

                elif len(line2) == 2:
                    sub_line2, rel_line2 = line2[0], line2[1]
                    obj_line2 = re.findall('"([^"]*)"', line)[0]

                else:
                    pass

                # writer.write("Both line: {}{}".format(line1, line2))

                finalObj = ''
                sub2 = sub_line2
                sub_line2 = sub_line2.split('/')[-1].upper()
                try:
                    extractedObj = entityEtra.get_continuous_chunks(sub_line2.upper())
                    extractedObjLength = len(extractedObj)
                except Exception as e:
                    print(e)
                else:
                    # print("NLTK works perfectly")
                    if extractedObjLength == 0:
                        pass
                    elif extractedObjLength == 1:
                        finalObj = extractedObj[0]
                    else:
                        writer.write('<{}> <{}isA> <{}> <{}> .'.format(sub2, relationToUse,
                                                                       '/'.join(sub2.split('/')[:-1]) + '/' + ','.join(
                                                                           extractedObj), context))
                        writer.write('\n')

                sub_line1, sub_line2 = sub_line1.lower(), sub_line2.lower()

                words_to_use = check_Words(extractedSub, extractedObj)
                sub_toWrite, obj_toWrite = words_to_use[0], words_to_use[1]
                calSimilarity(sub_toWrite, obj_toWrite, writer, sub1, sub2, context)


        writer.flush()
        writer.close()
        readIn = open('output.nq')
        data = readIn.read().replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')
        readIn.close()
        return data
