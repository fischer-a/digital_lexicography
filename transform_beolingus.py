# zu korrigieren: superEntry nur wenn mehrere Einträge
# ids ergänzen für superEntry/Entry
# (dran denken, patterns außerhalb der Loops zu kompilieren)
# (einträge strippen, um white spaces wegzubekommen)
# definition statt note in sense
# ASSIGNEMENT:
# I) IDs für superEntry and entry, zum Beispiel: (1) (1_1)
# II) usage und descr/spec. in SENSE ergänzen
# III) usage vereinheitlichen? [austr.] und [Austr.] vereinheitlichen zu 'austr'?
# IV) usage für alle entries
# assignment: TEI an Entwurf angleichen, zusätzliche Sachen noch ergänzen

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
        #print(k1)
        print(k1)
        if len(v1)>1:
            superentry = etree.Element('superentry')
            superentry_id=str(k1)
            superentry.set('xml_id', superentry_id)
        else:
            superentry_id=str(k1)
        counter=1
        for k2, v2 in v1.items():
            entry = etree.SubElement(superentry, 'entry')
            entry_id=superentry_id+"_"+str(counter)
            entry.set('xml_id', entry_id)
            split_forms = k2.split(';')
            split_senses = v2.split(';')

            '''
            print("k:")
            pprint.pprint(split_forms)
            print(len(split_forms))
            print("v:")
            pprint.pprint(split_senses)
            print(len(split_senses)) ############
            '''

            orth_pattern = re.compile(r'^(.+?)(?={|\[|\(|$)')
            gram_pattern = re.compile(r'{.+?}')
            usg_pattern = re.compile(r'\[.+?\]')
            note_pattern = re.compile(r'\(.+?\)')

            orth_pattern_sense = re.compile(r'^(.+?)(?=\(|$)') #### nur ohne "note"

            forms_counter=1
            for f in split_forms:
                f = f.lstrip()
                form = etree.SubElement(entry, 'form')
                form_id=entry_id+"_form"+str(forms_counter)
                form.set('xml_id', form_id)

                orth_match = orth_pattern.findall(f)
                # notes, gram etc. kann auch später mit .replace ("...", "") entfernt werden
                for o in orth_match:
                    orth = etree.SubElement(form, 'orth')
                    orth.text = o.strip()
                    gram_match = gram_pattern.findall(f)
                    if gram_match:
                        gramGrp = etree.SubElement(form, 'gramGrp')
                        for g in gram_match:
                            gram = etree.SubElement(gramGrp, 'gram')
                            gram.text = g

                note_match = note_pattern.findall(f)
                if note_match:
                    for n in note_match:
                        note = etree.SubElement(form, 'note')
                        note.text=n

                if f!=split_forms[-1] and len(v1)>1:
                    usg_match = usg_pattern.findall(f)
                    if usg_match:
                        for u in usg_match:
                            usg = etree.SubElement(entry, 'usg')
                            # usg.text=u
                            usg.text = u.strip(".").lower()

                else:
                    usg_match = usg_pattern.findall(f)
                    if usg_match:
                        for u in usg_match:
                            usg = etree.SubElement(form, 'usg')
                            # usg.text=u
                            usg.text = u.strip(".").lower()
                forms_counter+=1
            sense_counter=1
            for s in split_senses:
                sense = etree.SubElement(entry, 'sense')
                sense_id=entry_id+"_sense"+str(sense_counter)
                sense.set('xml_id', sense_id)

                sense_note_match=orth_pattern_sense.findall(s)
                for se in sense_note_match:
                    sense.text = se.strip()
                    '''gram_match = gram_pattern.findall(s)
                    if gram_match:
                        gramGrp = etree.SubElement(sense, 'gramGrp')
                        for g in gram_match:
                            gram = etree.SubElement(gramGrp, 'gram')
                            gram.text = g
    
                    usg_match = usg_pattern.findall(s)
                    if usg_match:
                        for u in usg_match:
                            usg = etree.SubElement(sense, 'usg')
                            usg.text=u'''

                    note_match = note_pattern.findall(s)
                    if note_match:
                        for n in note_match:
                            note = etree.SubElement(sense, 'note')
                            note.text=n
                sense_counter+=1
            counter += 1
        if k1>5000:########################
            break##########################
        if len(v1)>1:
            body.append(superentry)
        else:
            body.append(entry)
    et = etree.ElementTree(root)
    return et


et = transform_in_tei(input_output.deserialize('data/splitted_beolingus.pickle'))
et.write('data/beolingus_tei_2.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')