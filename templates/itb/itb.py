#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pdf import PDF
import os
import datetime

def load_resource( path ):
    return os.path.dirname(os.path.abspath(__file__))+"/"+path

class ITBPDF(PDF):
    def __init__( self, title, author, *args, **kwargs ):
        super( ).__init__( *args, **kwargs )

        self.title = title
        self.author = author

        self.set_header_size( 20 )
        self.set_footer_size( 12 )

        # TODO Avoid this: Absolute path file
        self.root = os.path.dirname(os.path.abspath(__file__))+"/"

    def header( self ) :
        super( ).pre_header()

        #TODO path od resources realitive to file location without self.root
        self.image( load_resource( "itb.png" ), h=10)
        self.set_position( y=0 )
        x_offset = 14 

        #h = 3
        #self.set_font( "Arial", size=7 )
        #self.write( "Generalitat de Catalunya", x=x_offset, h=h, align="L" )
        #self.write( "Departament d'Educació", x=x_offset, h=h, align="L" )

        #h = 4
        #self.set_font( "Arial", style="B", size=8 )
        #self.write( "Institut La Ferreria", x=x_offset, h=h, align="L" )
        #self.write( "Departament d'Informàtica", x=x_offset, h=h, align="L" )

        self.set_position( x=-30, y=0)
        self.image( load_resource( "consorci.png" ), h=14)

        super( ).post_header()

    def footer( self ) :
        super( ).pre_footer()

        h = 4
        self.set_font( "Arial", style="", size=8 )
        self.write( "Nom fitxer: ", w=20, h=h )
        self.set_font( "Arial", style="B", size=8 )
        self.write( self.title, x=20, y=0, h=h )
        
        self.set_font( "Arial", style="", size=8 )
        self.write( "Autor :", w=20, h=h )
        self.set_font( "Arial", style="B", size=8 )
        self.write( self.author, x=20, y=h, h=h )

        now = datetime.datetime.now()
        date = now.strftime( "%B %Y" )
        self.set_font( "Arial", style="B", size=8 )
        self.write( date, x=-30, y=0, h=h, align="R" )
        self.set_font( "Arial", style="", size=8 )
        self.write( "Data:", x=-45, w=20, y=0, h=h, align="R" )

        self.set_font( "Arial", style="I", size=9 )
        self.write( "Aquest document pot quedar obsolet una vegada imprès.", x=-90, y=h, h=h, align="R" )

        self.set_font( "Arial", style="B", size=8 )
        self.write( "Page "+str(self.page_no()), h=h, align="C" )

        super().post_footer()
