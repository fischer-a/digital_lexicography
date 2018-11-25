from lxml import etree
import input_output
import pprint
import re


def transform_in_tei(beo_as_dict):
    root = etree.Element('TEI', attrib={"xmlns": 'http://www.tei-c.org/ns/1.0'})

    ##HEADER
    header = etree.SubElement(root, 'teiHeader')

    fileDesc = etree.SubElement(header, 'fileDesc')
    titleStmt = etree.SubElement(fileDesc, 'titleStmt')
    title = etree.SubElement(titleStmt, 'title')
    title.text = 'TEI Version of Beolingus DE-EN'

    publicationStmt = etree.SubElement(fileDesc, 'publicationStmt')
    p_publicationStmt = etree.SubElement(publicationStmt, 'p')
    p_publicationStmt.text = 'Original Data: Copyright (c) :: Frank Richter <frank.richter.tu-chemnitz.de>'

    sourceDesc = etree.SubElement(fileDesc, 'sourceDesc')
    p_sourceDesc = etree.SubElement(sourceDesc, 'p')
    p_sourceDesc.text = 'Digi_Lex - TEI Version'

    ##TEXT
    text = etree.SubElement(root, 'text')
    body = etree.SubElement(text, 'body')

    for k1, v1 in beo_as_dict.items():  ##k1 ist die Zeilenzahl, v1 der Eintrag pro Zeile im dict
        superentry = etree.Element('superentry')
        #print(k1)
        for k2, v2 in v1.items():
            split_forms = k2.split(';')
            split_senses = v2.split(';')
            '''
            print("k:")
            pprint.pprint(split_forms)
            print(len(split_forms))
            print("v:")
            pprint.pprint(split_senses)
            print(len(split_senses))
            '''
            entry = etree.SubElement(superentry, 'entry')

            for f in split_forms:
                f = f.lstrip()
                form = etree.SubElement(entry, 'form')
                orth_pattern = re.compile(r'^(.+?)(?={|\[|\(|$)')
                orth_match = orth_pattern.findall(f)
                for o in orth_match:
                    orth = etree.SubElement(form, 'orth')
                    orth.text = o.strip()
                    gram_pattern = re.compile(r'{.+?}')
                    gram_match = gram_pattern.findall(f)
                    if gram_match:
                        gramGrp = etree.SubElement(form, 'gramGrp')
                        for g in gram_match:
                            gram = etree.SubElement(gramGrp, 'gram')
                            gram.text = g

                usg_pattern = re.compile(r'\[.+?\]')
                usg_match = usg_pattern.findall(f)
                if usg_match:
                    for u in usg_match:
                        usg = etree.SubElement(form, 'usg')
                        usg.text=u

                note_pattern = re.compile(r'\(.+?\)')
                note_match = note_pattern.findall(f)
                if note_match:
                    for n in note_match:
                        note = etree.SubElement(form, 'note')
                        note.text=n


            for s in split_senses:
                sense = etree.SubElement(entry, 'sense')
                sense.text = s.strip()
                '''
                gram_pattern = re.compile(r'{.+?}')
                gram_match = gram_pattern.findall(s)
                if gram_match:
                    gramGrp = etree.SubElement(sense, 'gramGrp')
                    for g in gram_match:
                        gram = etree.SubElement(gramGrp, 'gram')
                        gram.text = g

                usg_pattern = re.compile(r'\[.+?\]')
                usg_match = usg_pattern.findall(s)
                if usg_match:
                    for u in usg_match:
                        usg = etree.SubElement(sense, 'usg')
                        usg.text=u

                note_pattern = re.compile(r'\(.+?\)')
                note_match = note_pattern.findall(s)
                if note_match:
                    for n in note_match:
                        note = etree.SubElement(sense, 'note')
                        note.text=n
                '''

        body.append(superentry)

    et = etree.ElementTree(root)
    return et


et = transform_in_tei(input_output.deserialize('data/splitted_beolingus.pickle'))
et.write('data/beolingus_tei_2.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')