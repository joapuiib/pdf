# -*- coding: utf8 -*-

from templates.ferreria.ferreria import FerreriaPDF
from templates.itb.itb import ITBPDF
#from pdf import PDF

for template in [ ITBPDF, FerreriaPDF ] :
    title = "test%s.pdf" % template.__name__
    pdf = template( title,
                    "Joan Puigcerver", 
                    format=(200,200) )
    #pdf = PDF()
    pdf.set_margin( right=30, left=30, top=10, bot=10 )

    # TEST MARGINS OK
    #pdf.set_margin( left=150 )
    #pdf.set_margin( right=150 )
    #pdf.set_margin( top=150 )
    #pdf.set_margin( bot=150 )

    # TEST HEADER & FOOTER OK
    #pdf.draw_margins()
    #pdf.set_draw_header( True )
    #pdf.set_draw_footer( True )
    pdf.add_page()

    # Titol
    pdf.set_font("Arial", style="B", size=12)
    pdf.write("MÒDUL 1 - Implantació de Sistemes Operatius / Sistemes Informàtics", align="C")

    # OK!
    pdf.set_columns( 4 )

    pdf.set_font("Arial", style="", size=10)
    for i in range(250) :
        pdf.write( "text mes llarg test{}".format(i), border=0 )

    pdf.save( "docs/{}".format( title ))
