#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
from types import SimpleNamespace

DEBUG=False

class PDF(FPDF):
    def __init__( self, title="no title", *args, **kwargs ):
        super().__init__( *args, **kwargs )

        self.title = title

        # Relative cursor position in the canvas
        self.x_cursor = 0
        self.y_cursor = 0

        self.header_size = 0
        self.footer_size = 0

        # Default margins
        self.set_margin( left=20, right=20, top=7.5,  bot=7.5 )

        # Absolute position where our canvas start and size
        self.x_canvas = 0
        self.y_canvas = 0

        # Default line height
        self.line_height = 4.5

        # Columns
        # Number of current columns
        self.n_columns = 1
        # Index of current column
        self.current_column = 0
        # Width of columns (default all page)
        self.column_width = self.canvas_width
        # Width between columns
        self.column_margin = 10

        self.drawing_footer = False
        self.drawing_header = False


    def set_margin( self, left=None, top=None, right=None, bot=None) :

        # Margin values
        if left is not None :
            self.left = left
            super().set_left_margin( left )
        if right is not None :
            self.right = right
            super().set_right_margin( right )
        if top is not None :
            self.top = top
            super().set_top_margin( top )
        if bot is not None :
            self.bot = bot 
            super().set_auto_page_break( 1, bot + self.footer_size )

        self.reset_canvas()

        super().set_margins( left=self.left, top=self.top, right=self.right )

    def draw_margins( self ) :
        self.line( self.left, 0, self.left, self.h ) # Left
        self.line( self.w - self.right, 0, self.w - self.right, self.h ) # Right

        self.line( 0, self.top, self.w, self.top ) # Top
        self.line( 0, self.h - self.bot, self.w, self.h - self.bot) # Top

    def get_effective_width(self) :
        return self.w - self.left - self.right

    def reset_canvas( self ) :
        #self.set_columns( 1 )
        self.set_canvas_position( x = self.right, y = self.top + self.header_size )
        self.set_canvas_size( 
                              width  = self.get_effective_width(),
                              height = self.h - self.top  - self.bot - self.header_size - self.footer_size
                            )

    def set_canvas( self, x, y, width, height ) :
        self.set_canvas_position( x, y )
        self.set_canvas_size( width, height )

    def set_canvas_size( self, width=None, height=None ) :
        #print( "set_canvas_size( w={}, h={} )".format( width, height ) )
        if width is not None :
            self.canvas_width = width
        if height is not None :
            self.canvas_height = height
        self.reset_position()

    def set_canvas_position( self, x=None, y=None ) :
        #print( "set_canvas_position( x={}, y={} )".format( x, y ) )
        if x is not None :
            if x < 0:
                x = self.w - x
            self.x_canvas = x
        if y is not None :
            if y < 0:
                y = self.h - y
            self.y_canvas = y

    def reset_position( self ) :
        self.set_position( x=0, y=0 )

    def update_position( self ) :
        self.set_position( x=self.x_cursor, y=self.y_cursor )

    def set_position( self, x=None, y=None ) :

        if y is not None :

            if y < 0 :
                y = self.canvas_height + y
            
            #print( "Y: {}\tCanvas: {}\t Canvas_H: {}".format( y, self.y_canvas, self.canvas_height) )

            # set_y sets x = left margin by default
            if x is None :
                old_x = self.x
            self.set_y( self.y_canvas + y )
            if x is None :
                self.set_x( old_x )
            self.y_cursor = y

        if x is not None :

            if x < 0 :
                x = self.canvas_width + x

            #print( "X: {}\tCanvas: {}\t Canvas_W: {}".format( x, self.x_canvas, self.canvas_width ) )
            self.set_x( self.x_canvas + x )
            self.x_cursor = x

        #print( "set_position( x={}, y={} )\tCursor: ({}, {})\tAbsolute: ({}, {})".format( x, y, self.x_cursor, self.y_cursor, self.x, self.y ) )

    def move_pos( self, x=None, y=None ) :
        actual_pos = self.get_pos()
        if x is not None :
            x += actual_pos.x
        if y is not None :
            y += actual_pos.y
        self.set_position( x=x, y=y )

    def line_up( self, h=None ):
        up = self.line_height
        if h is not None :
            up = h
        self.move_pos( y=-up )

    # This method returns the current position in the current effective page (no margins nor header/footer/banners)
    def get_pos( self ) :
        return SimpleNamespace( x=self.x_cursor, y=self.y_cursor )

    def set_header_size ( self, size ) :
        self.header_size = size  

    def set_footer_size ( self, size ) :
        self.footer_size = size  
        super(PDF, self).set_auto_page_break( 1, self.bot + size )

    def set_draw_header( self, flag ) :
        self.drawing_header = flag
    def draw_header( self ) :
        left = self.left
        right = self.w - self.right
        top = self.top
        bot = self.top + self.header_size

        self.line( left,  top, left,  bot ) # Left
        self.line( right, top, right, bot ) # Right

        self.line( left, top, right, top ) # Top
        self.line( left, bot, right, bot ) # Bot

    def set_draw_footer( self, flag ) :
        self.drawing_footer = flag
    def draw_footer( self ) :
        left = self.left
        right = self.w - self.right
        top = self.h - self.bot - self.footer_size
        bot = self.h - self.bot

        self.line( left,  top, left,  bot ) # Left
        self.line( right, top, right, bot ) # Right

        self.line( left, top, right, top ) # Top
        self.line( left, bot, right, bot ) # Bot

    def pre_header( self ) :
        #print( "pre header" )
        self.set_canvas( self.right, self.top, self.get_effective_width(), self.header_size )

        # Save color state
        self.last_text_color = self.text_color
        self.set_text_color(0,0,0)
        
        # Save columns state
        self.last_columns = self.n_columns
        self.set_columns( 1 )

        if self.drawing_header:
            self.draw_header()

        #self.print_variables()

    def header( self ):
        self.pre_header()
        self.post_header()

    def post_header( self ) :
        #print( "post header" )
        self.reset_canvas()

        # Restore columns
        self.set_columns( self.last_columns )
        del self.last_columns

        # Restore color
        self.text_color = self.last_text_color
        del self.last_text_color

    def pre_footer( self ) :
        #print( "pre footer" )
        self.set_canvas( self.right, self.h - self.bot - self.footer_size, self.get_effective_width(), self.footer_size )

        if self.drawing_footer :
            self.draw_footer()

        # Save color state
        self.last_text_color = self.text_color
        self.set_text_color(0,0,0)

        #self.print_variables()

    def footer( self ):
        self.pre_footer()
        self.post_footer()

    def post_footer( self ) :
        #print( "post footer" )
        self.reset_canvas()

        # Restore color
        self.text_color = self.last_text_color
        del self.last_text_color

    def set_columns( self, n_columns, height=None ):
        self.current_column = 0
        self.n_columns = n_columns
        self.y_start_columns = self.y

        self.column_height = self.y_space_left()
        if height is not None :
            self.column_height = height

        self.column_width = (self.get_effective_width() - (n_columns - 1)*self.column_margin) / self.n_columns
        self.set_canvas( self.left , self.y_start_columns, self.column_width, self.column_height )
        if DEBUG: print( "set_columns( {}, height={} )".format( n_columns, height ) )
        if DEBUG: print( "Start: {}\tHeight: {}\tWidth: {}".format( self.y_start_columns, self.column_height, self.column_width ) )

    @property
    def accept_page_break( self ):
        self.current_column += 1
        if self.current_column >= self.n_columns :
            self.current_column = 0

        x_start = self.left + ( self.column_width + self.column_margin ) * self.current_column
        self.set_canvas( x_start, self.y_start_columns, self.column_width, self.column_height )

        if self.current_column > 0 :
            return False
        else :
            return True

    # This method moves the current position in the current effective page (no margins nor header/footer/banners)
    def save( self, path=None ) :
        if not path :
            path = self.title
        self.output( path )

    def y_space_left( self ) :
        space_left = self.canvas_height - self.y_cursor
        return space_left

    def print_variables( self ):
        print( "size:({:3.1f},{:3.1f}),\tmargins:(l{:3.1f},r{:3.1f},t{:3.1f},b{:3.1f})".format(
            self.w, self.h,
            self.left, self.right, self.top, self.bot ), end="" )
        print( "\tcanvas: ({:3.1f},{:3.1f}),\tcanvas_size: ({:3.1f},{:3.1f})\t".format( 
            self.x_canvas, self.y_canvas,
            self.canvas_width, self.canvas_height) , end="")
        print( "fpdf:({:3.1f},{:3.1f}),\tcursor:({:3.1f},{:3.1f}),\tleft: {:3.1f}".format( 
            self.x, self.y, 
            self.x_cursor, self.y_cursor,
            self.y_space_left() ))


    def write( self, text, x=None, y=None, w=None, h=None, align="J", border=0 ) :
        if DEBUG: print( "write( self.x={}, self.y={}, x={}, y={}, w={}, h={}, text={}".format(self.x, self.y, x, y, w, h, text ) )

        if x is not None :
            self.set_position( x=x )
        x = self.x_cursor

        if y is not None :
            self.set_position( y=y )
        y = self.y_cursor

        if h is None :
           h = self.line_height
        if h < 0 :
           h = self.y_space_left()

        if w is None :
            w = self.canvas_width - x

        if not isinstance( text, list ) :
            text = [text]

        if DEBUG: print( "write( self.x={}, self.y={}, x={}, y={}, w={}, h={}, text={}".format(self.x, self.y, x, y, w, h, text ) )
        space_used = 0
        for line in text:
            _, split_text = self.multi_cell( w, h, txt=line, border=( 1 if DEBUG else border ), align=align )
            space_used += len(split_text) * h
            #print( space_used )
            self.set_position( x=0 )
            self.y_cursor += h * len(split_text);
            self.set_position( y=self.y_cursor )

        #self.print_variables();
        return space_used

    def write_space_needed(self, text, x=None, w=None, h=None, align='J', border=0):
        if x is None :
            x = self.get_pos().x

        if h is None :
            h = self.line_height

        if w is None :
            w = self.column_width - x
        
        space = 0
        if not isinstance( text, list ) :
            text = [text]
        #print( text )
        for line in text:
            _, split_text = self.multi_cell( w, h, txt=line, border=border, align=align, split_only=True )
            #print( split_text )
            space += h*len(split_text)
        #self.print_variables();

        return space

    def write_white( self, h=0, border=0 ) :
        consumed = self.write( text="", h=h, border=border )
        #print( "white h:{} actual:{}".format(h, consumed ))

    def column_break( self, border=0 ) :
        self.write_white( h=self.y_space_left(), border=border )

    def set_color( self, r, g, b ) :
        super(PDF, self).set_text_color(r, g, b)
        #print( self.text_color )

    def load( self, path ) :
        self.add_page()
        self.set_source_file( path )
        templ = self.importPage( 1 )
        self.useTemplate( templ, 0, 0, 0, 0, True )
