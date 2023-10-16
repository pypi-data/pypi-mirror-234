from enum import Enum, IntEnum
from typing import List

import jpype
from asposepdf import Assist, Api
from jpype import JArray


class PdfFileEditor(Assist.BaseJavaClass):
    """!
    Class representing Acro form object.
    """

    javaClassName = "com.aspose.python.pdf.facades.PdfFileEditor"

    def __init__(self):
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass()

    def concatenateTwo(self, firstInputFile, secInputFile, outputFile):
        """!
        Concatenates two files.
        """

        if firstInputFile is None or secInputFile is None or outputFile is None:
            raise Exception("arguments are required")
        else:
            result = self.javaClass.concatenate(firstInputFile, secInputFile, outputFile)

    def concatenate(self, src: List[Api.Document], dest: Api.Document):
        """!
        Concatenates documents.
        """

        if src is None or dest is None:
            raise ValueError("Both 'src' and 'dest' arguments are required.")
        else:
            java_array = JArray(Api.Document.javaClassName)(len(src))
            for i, item in enumerate(src):
                java_array[i] = item.getJavaClass()
            result = self.javaClass.concatenate(java_array, dest.getJavaClass())

    def concatenate(self, src: List[str], dest: str):
        """!
        Concatenates files.
        """

        if src is None or dest is None:
            raise ValueError("Both 'src' and 'dest' arguments are required.")
        else:
            java_array = jpype.JArray(jpype.JString)(len(src))
            for i, item in enumerate(src):
                java_array[i] = item
            result = self.javaClass.concatenate(java_array, jpype.JString(dest))

    def splitFromFirst(self, inputFile, location, outputFile):
        """!
        Splits Pdf file from first page to specified location,and saves the front part as a new file.
        """

        if inputFile is None or location is None or outputFile is None:
            raise Exception("arguments are required")
        else:
            result = self.javaClass.splitFromFirst(inputFile, location, outputFile)

    def splitToEnd(self, inputFile, location, outputFile):
        """!
        Splits from location, and saves the rear part as a new file.
        """

        if inputFile is None or location is None or outputFile is None:
            raise Exception("arguments are required")
        else:
            result = self.javaClass.splitToEnd(inputFile, location, outputFile)

