import os
import time
import itertools
import re
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
import entityEtra


dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

relationToUse = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
mainSim, hashOut = 0, 0
subToUse, objToUse = '', ''


def specificImageURLs(word, hashed_output, writer, relationToUse, context):
    print("Inside the secooond functionnnns", word)
    try:
        syns = wordnet.synsets('{}'.format(word))[0]
        syn_offset = syns.offset()
        print(syn_offset)
        page = requests.get('http://www.image-net.org/search?q={}'.format(word))
        soup = BeautifulSoup(page.content, 'html.parser')
        if len(str(syn_offset)) == 7:
            try:
                print("Reachhhhhhhhhhhed first try")
                for link in soup.find_all('a', {'href': 'synset?wnid=n0{}'.format(syn_offset)}):
                    print("Insidde the fooooooooooooor")
                    writer.write(
                        '_:{} <{}{}_Images> "http://www.image-net.org/{}" <{}> .'.format(hashed_output, relationToUse,
                                                                                         word, link.img['src'],
                                                                                         context))
                    print('_:{} <{}{}_Images> "http://www.image-net.org/{}" <{}> .'.format(hashed_output, relationToUse,
                                                                                         word, link.img['src'],
                                                                                         context))
                    writer.write('\n')
            except Exception as e:
                print (e)
        else:
            try:
                print("Reachhhhhhhhhhhed second try")
                for link in soup.find_all('a', {'href': 'synset?wnid=n{}'.format(syn_offset)}):
                    writer.write(
                        '_:{} <{}{}_Images> "http://www.image-net.org/{}" <{}> .'.format(hashed_output, relationToUse,
                                                                                         word, link.img['src'],
                                                                                         context))
                    print('_:{} <{}{}_Images> "http://www.image-net.org/{}" <{}> .'.format(hashed_output, relationToUse,
                                                                                         word, link.img['src'],
                                                                                         context))
                    writer.write('\n')
            except Exception as e:
                pass
    except Exception as e:
        print(e)



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
                    print("sub ext", extractedSub)
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
                    print("obj ext", extractedObj)
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

                from semanticSimi import make_Hash
                hashOut = make_Hash(first, second)

                try:
                    from relations import write_Relation
                    write_Relation(first, second, writer, sub1, sub2, context)
                except Exception:
                    pass
                try:
                    from semanticSimi import write_Semantic
                    write_Semantic(first, second, writer, sub1, sub2, context)
                except Exception:
                    pass
                try:
                    from relatedImages import imageURLS
                    imageURLS(first, hashOut, writer, relationToUse, context)
                    imageURLS(second, hashOut, writer, relationToUse, context)
                except Exception:
                    pass

                specificImageURLs(first, hashOut, writer, relationToUse, context)
                specificImageURLs(second, hashOut, writer, relationToUse, context)

        writer.flush()
        writer.close()

        readIn = open('output.nq')
        data = readIn.read().replace('<', '&lt;').replace('>', '&gt;').replace('\n', '</br>')
        readIn.close()
        return data