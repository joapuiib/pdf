#import os
#import importlib
#
#for template in os.listdir( os.path.dirname(os.path.abspath(__file__)) ) :
#    if template not in [ os.path.basename(__file__), '__pycache__' ] :
#        module_obj = importlib.import_module( "{}.{}".format( template, template ) )
#        globals()[template] = module_obj
