import ast

import astunparse


class FileFunction:
    def __init__(self, pyfile: str):
        """
        Convert a python file into an executable function,
        and the passed parameters will modify the same name variables during execution. \n
        1, Only keyword parameter passing is supported.  \n
        2, To define the RETURN variable in the original python file to return a value. \n
        3, The passed parameters is const and can not be modified. \n
        :param pyfile: original python file.
        """
        self.pyfile = pyfile
        with open(self.pyfile) as f:
            self.code_tree = ast.parse(f.read())

    def __call__(self, **kwargs):
        """
        1, Only keyword parameter passing is supported.  \n
        2, To define the RETURN variable in the original python file to return a value. \n
        3, The passed parameters is const and can not be modified. \n
        """
        for code in self.code_tree.body:
            locals().update(kwargs)
            exec(astunparse.unparse(code), locals())

        return locals().get("RETURN", None)
