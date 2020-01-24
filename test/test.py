# -*- coding: utf8 -*-

from pdf import PDF

pdf = PDF()
pdf.set_margin( right=30, left=30, top=10, bot=10 )

pdf.add_page()

# Titol
pdf.set_font("Arial", style="B", size=12)
pdf.write("MÒDUL 1 - Implantació de Sistemes Operatius / Sistemes Informàtics", align="C")

pdf.set_font("Arial", style="", size=10)
pdf.write( "text mes llarg test", x=-40, border=1 )

pdf.save( "docs/{}".format( "test.pdf" ))
