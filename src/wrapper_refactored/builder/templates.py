'''
Created on Apr 12, 2010

@author: henrik
'''
import re
import string


from pygccxml import declarations
#from occ_declarations import class_t
from pygccxml.declarations.cpptypes import free_function_type_t, type_t

from pypp_mods import class_t
from builder.pypp_mods import include_matcher, module_matcher



class Template(string.Template):
    idpattern = "[_a-z][_a-z0-9]*[a-z0-9]"
    
      
class BaseTemplate:
    """
        Testing 
            ${one} 
                ${two} 
                    ${three}
    """

    def __init__(self, indent=0):
        self._template = self.__doc__
        self.dict = self.__dict__
        self.compact = False
        
    def indent(self, line, indent):
        diff = indent - self.original_indent()
        if diff < 0:
            return re.sub("^(\ \ \ \ ){0,%s}"% abs(diff), "", line)
        elif diff > 0:
            indents = "".join(["    " for i in xrange(diff)])
            return "%s%s" % (indents, line)
        else: return line
            
    def original_indent(self):
        return self._template.splitlines()[1].count("    ")
    
    def process(self, *args):
        return {}
            
    def render(self, declaration, indent=0):
        self.process(declaration)
        
        if self._template == None:
            print "Template is none for ", self.__class__.__name__

        template = self._template.rstrip('\t \n')
        template = template.strip('\n')
        template = "\n".join([self.indent(line, indent) for line in template.splitlines()])
        template = re.sub("[ \t\r\f\v]*\*\$", "$", template)
        
        t = Template(template)
        ret =  t.safe_substitute(self.__dict__)
        if self.compact:
            ret = re.sub("\n\n+", "\n", ret)
        return ret

class WrapperTemplate(BaseTemplate):
    """
    // HXX wrapper generated by pythonOCC generate_code.py script.
    #ifndef __${module_name}_wrapper__
    #define __${module_name}_wrapper__
    ${includes}
    #endif __${module_name}_wrapper__
    """
    def process(self, name_and_includes):
        self.module_name, includes = name_and_includes
        self.includes = "\n".join(['#include "%s"' % inc for inc in includes])