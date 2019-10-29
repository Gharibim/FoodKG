'''
This is the mail file where we get the semantic similarity for the concepts from our embedding vector (AGROVEC)

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

# Generate a hash for a triple and returns 8 unique numbers to be used a blank nodes.
def make_Hash(subject, object):
    return abs(hash('{} {}'.format(subject, object))) % (10 ** 8)


# Writes the semantic similarity after calculating the semantic similarity
# Do not call directly, there is a wrapper for this function in relations.py
def write_Semantic(subject, object, writer, sub1, sub2, context):
    from relations import Universal_rel
    from prepare_Models import get_Similarity
    Similarity = get_Similarity(subject, object)
    to_hash = make_Hash(subject, object)
    hashed_output = to_hash
    writer.write('<{}> <{}{}> _:{} <{}> .'.format(sub1, relationToUse, Universal_rel, hashed_output, context))
    writer.write('\n')
    writer.write('<{}> <{}{}> _:{} <{}> .'.format(sub2, relationToUse, Universal_rel, hashed_output, context))
    writer.write('\n')
    writer.write(
        '_:{} <{}Semantic_Similarity> "{}" <{}> .'.format(hashed_output, relationToUse, str(Similarity), context))
    writer.write('\n')


def calSimilarity(subject, object, writer, sub1, sub2, context):
    global mainSim
    global hashOut
    try:
        from relations import write_Relation
        write_Relation(subject, object, writer, sub1, sub2, context)
    except Exception as e:
        pass

    try:
        write_Semantic(subject, object, writer, sub1, sub2, context)
    except Exception:
        pass

def readFile(fileName, context):
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

                from relations import check_Words
                words_to_use = check_Words(extractedSub, extractedObj)
                first, second = words_to_use[0], words_to_use[1]
                calSimilarity(first, second, writer, sub1, sub2, context)


        writer.flush()
        writer.close()

        readIn = open('output.nq')
        data = readIn.read().replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')
        readIn.close()
        return data
