# -*- coding: utf8 -*-

from ferreria.ferreria import FerreriaPDF
from types import SimpleNamespace
import re
import random
import sys
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument( "preguntes", help="Fitxer de preguntes.")
parser.add_argument( "-d", "--dir", default="", help="Directori on es generaran els documents.")
parser.add_argument( "-v", "--verbosity", action="count", default=0, help="Incrementa la verbositat.")
args = parser.parse_args()


fitxer_preguntes = args.preguntes
output = args.dir
if len(output) > 0 and output[-1] != '/' :
    output += '/'
verbositat = args.verbosity

def vprint( text="", verbosity_level=0, end="\n" ):
    if verbosity_level <= verbositat :
        print( text, end=end )

def load_questions( path ): 
    
    questions = []

    f = open( path )

    # REGEX per identificar els elements de la pregunta
    pattern_enunciat = re.compile("\s*(\d+)\. (.*)")
    pattern_resposta = re.compile("\s*([a-d])\) (.*)")
    pattern_solucio = re.compile("\s*\* ?([a-d])?.*")
    pattern_explicacio = re.compile("\s*# (.*)")

    current_question = None
    for line in f.readlines():
        #print( line )

        # Elimine caracters especials de citació
        line = line.rstrip().replace(u"\u2018", "'").replace(u"\u2019", "'")
        line = line.replace(u"\u2013", "-")
        line = line.replace(u"\u201c", "\"").replace(u"\u201d", "\"")

        match_enunciat = re.match( pattern_enunciat, line )
        match_resposta = re.match( pattern_resposta, line )
        match_solucio = re.match( pattern_solucio, line )
        match_explicacio = re.match( pattern_explicacio , line )

        if match_enunciat is not None :
            # Afegisc a la llista la pregunta anterior i cree el nou objecte
            if current_question is not None :
                questions += [current_question]
            current_question = SimpleNamespace( enunciat="", respostes=[], solucio=-1, explicacions=[] )

            # Guarde sols el enunciat (No el número de la pregunta)
            current_question.enunciat = match_enunciat.groups()[1].replace("\\n","\n").replace("\\t","")
            #print( current_question.enunciat )

        elif match_resposta is not None :
            # Guarde sols el text de la respota (No el caràcter d'abans)
            current_question.respostes += [match_resposta.groups()[1]]

        elif match_solucio is not None :
            tupla = match_solucio.groups()
            solucio = None
            # Comprove si hi ha solució especificada (pot ser no hi haja, pregunta de respota oberta)
            if tupla[0] is not None :
                solucio = ord(tupla[0]) - ord('a')
            current_question.solucio = solucio

        elif match_explicacio is not None :
            # Guarde sols el text de la respota (No el caràcter d'abans)
            current_question.explicacions += [match_explicacio.groups()[0]]

    questions += [current_question]
    f.close()

    return questions

def shuffle( questions, threshold=0 ):
    new_questions = questions.copy()
    if threshold > 0 :
        questions_left = new_questions[:threshold]
        new_questions = new_questions[threshold:]
    elif threshold < 0 :
        questions_left = new_questions[threshold:]
        new_questions = new_questions[:threshold]

    random.shuffle( new_questions )

    for question in new_questions :
        new_order = (list(enumerate(question.respostes)))
        random.shuffle( new_order )
        new_respostes = [ x[1] for x in new_order ]
        new_solucio = 0

        for i in range(len(new_order)) :
            if new_order[i][0] == question.solucio :
                question.solucio = i
                break

        question.respostes = new_respostes

    if threshold > 0 :
        new_questions = questions_left + new_questions 
    elif threshold < 0 :
        new_questions = new_questions + questions_left

    return new_questions

def write_solutions( path, questions ):
    f = open( path, "w" )

    for i in range(len(questions)) :
        if questions[i].solucio is not None :
            f.write( str(i) + "\t" + str(chr(questions[i].solucio + ord('a'))) + "\n" )
    f.close()
    vprint("Solucions:" + path, 1)

def print_questions( questions, verbosity_level=0 ):
    i = 1
    for question in questions:
        vprint( str(i)+". ", verbosity_level, end="" )
        print_question( question, verbosity_level )
        vprint("",verbosity_level)
        i += 1

def print_question( question, verbosity_level=0 ):
    vprint( question.enunciat, verbosity_level )
    for resposta in question.respostes :
        vprint( "\t" + resposta, verbosity_level )
    for explicacio in question.explicacions :
        vprint( "\t# " + explicacio, verbosity_level )

def generate_pdf( path, questions, explicacions=False, marcar_solucio=False ):
    file_name = path.split("/")[-1]
    pdf = FerreriaPDF( file_name, "Joan Puigcerver (joapuiib)")
    pdf.add_page()

    pdf.set_draw_footer(True)

    # Titol
    pdf.set_font("Arial", style="B", size=12)
    pdf.write("MÒDUL 1 - Implantació de Sistemes Operatius / Sistemes Informàtics", h=7,align="C")

    pdf.move_pos(y=2.5)
    pdf.set_font("Arial", style="B", size=10)
    pdf.write("TEST LPIC - UNITAT FORMATIVA 2", align="L")
    pdf.move_pos(y=2)
    pdf.set_font("Arial", style="", size=10)
    pdf.write("Recopilació de preguntes per al test LPIC corresponent a la UF2", align="J")

    pdf.move_pos(y=2.5)

    pdf.set_columns(2)

    i = 1
    sangria = 5
    size = 9
    size_explicacio = 8
    max_espai = 0
    espai_pregunta = 56
    same_space = False

    #print( "Left_space: {}".format( pdf.y_space_left() ) )
    for question in questions :

        espai = 0
        # Enunciat en negre i en negreta
        pdf.set_color(0,0,0)
        pdf.set_font("Arial", style="B", size=size)
        espai += pdf.write_space_needed( str(i) + ". " + question.enunciat )

        # Preguntes sense negreta
        j = 0
        pdf.set_font("Arial", style="", size=size)
        for resposta in question.respostes :
            lletra_index = str( chr( ord('a') + j ))
            espai += pdf.write_space_needed( lletra_index + ") " + resposta, x=sangria )
            j += 1

        if explicacions :
            pdf.set_font("Times", style="", size=size_explicacio)
            for explicacio in question.explicacions:
                espai += pdf.write_space_needed( explicacio );

        if espai > max_espai :
            max_espai = espai
        #print( "Space: {: 2d} Needed: {:6.1f} Left: {:6.1f}".format( i, espai, pdf.y_space_left() ))
        if espai > pdf.y_space_left() :
            pdf.column_break(border=0)
            #print( "Not enough space: {: 6.1f} Needed: {:6.1f} Left: {:6.1f}".format( i, espai, pdf.y_space_left() ))

        #pdf.print_variables()

        espai = 0
        # Enunciat en negre i en negreta
        pdf.set_color(0,0,0)
        pdf.set_font("Arial", style="B", size=size)
        espai += pdf.write( str(i) + ". " + question.enunciat )

        j = 0
        solucio = question.solucio
        # Preguntes sense negreta
        pdf.set_font("Arial", style="", size=size)

        for resposta in question.respostes :
            # Marque la solucio si cal
            if marcar_solucio and j == solucio :
                pdf.set_color(255,0,0)
            else :
                pdf.set_color(0,0,0)
            
            lletra_index = str( chr( ord('a') + j ))
            espai += pdf.write( lletra_index + ") " + resposta, x=sangria )
            j += 1

        if explicacions :
            pdf.set_color(51,51,0)
            pdf.set_font("Times", style="", size=size_explicacio)
            for explicacio in question.explicacions:
                espai += pdf.write( explicacio );

        if same_space :
            pdf.write_white( h=(espai_pregunta - espai), border=0 )
        else :
            pdf.write_white( h=2.5 )

        i += 1

    pdf.save( path )
    vprint("Generat: " + path, 1)

    #print( max_espai )


questions = load_questions( fitxer_preguntes )
print_questions( questions, 2 )

generate_pdf( output + "RecopilacióPreguntesLPIC_UF2-1819.pdf", questions,  explicacions=True, marcar_solucio=True)
