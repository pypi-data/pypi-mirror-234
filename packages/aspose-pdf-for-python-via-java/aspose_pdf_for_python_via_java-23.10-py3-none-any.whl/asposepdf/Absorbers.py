from enum import Enum
from typing import List

import jpype

from asposepdf import Assist, Api
from asposepdf.Api import Page, Document, Rectangle


class TextFormattingMode(Enum):
    """!
    Defines different modes which can be used while converting pdf document into text.
    """

    Pure = 0
    """!
     Represent pdf content with a bit of formatting routines.
    """

    Raw = 1
    """!
     Represent pdf content as is, i.e. without formatting.
    """

    Flatten = 2
    """!
    Represent pdf content with positioning text fragments by their coordinates.
    It is basically similar to "Raw" mode. But while "Raw" focuses on preserving the structure
    of text fragments (operators) in a document, "Flatten" focuses on keeping text in the order it is read.
    """

    MemorySaving = 3
    """!
    Extraction with memory saving. It is almost same to 'Raw' mode but works slightly faster and uses less memory.
    """


class TextSearchOptions(Assist.BaseJavaClass):
    """!
   Represents text search options
   """

    javaClassName = "com.aspose.python.pdf.TextSearchOptions"

    formattingMode = TextFormattingMode.Pure

    def __init__(self, rectangle: Rectangle = None, is_regular_expression_used: bool = None, java_class=None):
        if java_class is None:
            self._rectangle = rectangle
            self._is_regular_expression_used = is_regular_expression_used
            java_class_link = jpype.JClass(self.javaClassName)
            if rectangle is None and is_regular_expression_used is None:
                self.javaClass = java_class_link(False)
            elif rectangle is None:
                self.javaClass = java_class_link(is_regular_expression_used)
            elif is_regular_expression_used is None:
                self.javaClass = java_class_link(rectangle.getJavaClass())
            else:
                self.javaClass = java_class_link(rectangle.getJavaClass(), is_regular_expression_used)

        else:
            super().__init__(java_class)

    @property
    def rectangle(self):
        return self._rectangle

    @rectangle.setter
    def rectangle(self, value: Rectangle):
        self._rectangle = value

    @property
    def is_regular_expression_used(self):
        return self._is_regular_expression_used

    @is_regular_expression_used.setter
    def is_regular_expression_used(self, value: bool):
        self._is_regular_expression_used = value


class TextExtractionOptions(Assist.BaseJavaClass):
    """!
   Represents text extraction options
   """

    javaClassName = "com.aspose.python.pdf.TextExtractionOptions"

    def __init__(self, mode: TextFormattingMode, java_class=None):
        if java_class is None:
            self._formatting_mode = mode
            java_class_link = jpype.JClass(self.javaClassName)
            self.javaClass = java_class_link(self._formatting_mode.value)
        else:
            super().__init__(java_class)

    @property
    def formatting_mode(self):
        """!
        Gets factor that will be applied to scale font size during extraction in pure mode. Setting
        of less value leads to more spaces in the extracted text. Default value is 1 - no scaling;
        Setting value to zero allows algorithm choose scaling automatically.
        :return:

        """
        return self._formatting_mode

    @formatting_mode.setter
    def formatting_mode(self, formatting_mode: TextFormattingMode):
        """!
        Sets factor that will be applied to scale font size during extraction in pure mode. Setting
        of less value leads to more spaces in the extracted text (from 1 to 10). Default value is 1 - no scaling;
        Setting value to zero allows algorithm choose scaling automatically.
        :param formatting_mode:
        :return:

        """
        self._formatting_mode = formatting_mode

    @property
    def scale_factor(self):
        """!
        Gets factor that will be applied to scale font size during extraction in pure mode. Setting
        of less value leads to more spaces in the extracted text. Default value is 1 - no scaling;
        Setting value to zero allows algorithm choose scaling automatically.
        :return:

        """
        return self.getJavaClass().getScaleFactor()

    @scale_factor.setter
    def scale_factor(self, scale_factor: float):
        """!
        Sets factor that will be applied to scale font size during extraction in pure mode. Setting
        of less value leads to more spaces in the extracted text (from 1 to 10). Default value is 1 - no scaling;
        Setting value to zero allows algorithm choose scaling automatically.
        :param scale_factor:
        :return:

        """
        self.getJavaClass().setScaleFactor(scale_factor)


class TextAbsorber(Assist.BaseJavaClass):
    """!
    Extracts text on the specified document
    """

    javaClassName = "com.aspose.python.pdf.TextAbsorber"
    extraction_options = TextExtractionOptions(mode=TextFormattingMode.Pure)
    search_options = TextSearchOptions()

    def __init__(self, extraction_options=None, search_options=None, java_class=None):
        if java_class is None:
            self.extraction_options = extraction_options
            self.search_options = search_options
            java_class_link = jpype.JClass(self.javaClassName)
            if extraction_options is None and search_options is None:
                self.javaClass = java_class_link()
            elif extraction_options is None:
                self.javaClass = java_class_link(self.search_options.setJavaClass())
            elif search_options is None:
                self.javaClass = java_class_link(self.extraction_options.setJavaClass())
            else:
                self.javaClass = java_class_link(self.extraction_options.setJavaClass(),
                                                 self.search_options.setJavaClass())
        else:
            super().__init__(java_class)

    def visit(self, page: Page = None, document: Document = None):
        """!
        Extracts text on the specified page or whole PDF document
        """

        if page is None:
            self.getJavaClass().visit(document.getJavaClass())
        elif document is None:
            self.getJavaClass().visit(page.getJavaClass())

    @property
    def getText(self):
        """!
        Gets extracted text that the TextAbsorber extracts on the PDF document or page.
        """
        return str(self.getJavaClass().getText())


class AbsorbedCell(Assist.BaseJavaClass):
    """!
    Represents cell of table that exist on the page
    """

    javaClassName = "com.aspose.python.pdf.AbsorbedCell"

    def __init__(self, java_class):
        super().__init__(java_class)

    @property
    def getTextFragments(self) -> Api.TextFragmentCollection:
        """!
        Gets collection of TextFragment objects that describes text containing in the cell
        """
        return Api.TextFragmentCollection(self.getJavaClass().getTextFragments())

    @property
    def getRectangle(self):
        """!
        Gets rectangle that describes position of the cell on page
        """
        return Api.Rectangle(self.getJavaClass().get_rectangle())


class AbsorbedRow(Assist.BaseJavaClass):
    """!
    Represents row of table that exist on the page
    """

    javaClassName = "com.aspose.python.pdf.AbsorbedRow"

    def __init__(self, java_class):
        super().__init__(java_class)

    @property
    def getCellList(self) -> List[AbsorbedCell]:
        """!
        Gets readonly IList containing cells of the row
        """

        """!
        Gets readonly IList containing rows of the table
        """
        cell_list = []
        for java_row in self.getJavaClass().getCellList():
            cell_list.append(AbsorbedCell(java_row))

        return cell_list

    @property
    def getRectangle(self) -> Api.Rectangle:
        """!
        Gets rectangle that describes position of the Row on page
        """
        return Api.Rectangle(self.getJavaClass().get_rectangle())


class AbsorbedTable(Assist.BaseJavaClass):
    """!
    Represents an absorber object of table elements. Performs search and provides access to search results via
    TableAbsorber collection.
    """

    javaClassName = "com.aspose.python.pdf.AbsorbedTable"

    def __init__(self, java_class):
        super().__init__(java_class)

    @property
    def getRowList(self) -> List[AbsorbedRow]:
        """!
        Gets readonly IList containing rows of the table
        """
        row_list = []
        for java_row in self.getJavaClass().getRowList():
            row_list.append(AbsorbedRow(java_row))

        return row_list

    @property
    def getRectangle(self):
        """!
        Gets rectangle that describes position of the table on page
        """
        return Api.Rectangle(self.getJavaClass().get_rectangle())

    @property
    def getPageNum(self):
        """!
        Gets number of the page containing this table
        """
        return self.getJavaClass().getPageNum()


class TableAbsorber(Assist.BaseJavaClass):
    """!
    Represents an absorber object of table elements. Performs search and provides access to search results via
    TableAbsorber collection.
    """

    javaClassName = "com.aspose.python.pdf.TableAbsorber"
    search_options = TextSearchOptions()

    def __init__(self, search_options=None, java_class=None):
        if java_class is None:
            self.search_options = search_options
            java_class_link = jpype.JClass(self.javaClassName)
            if search_options is None:
                self.javaClass = java_class_link()
            else:
                self.javaClass = java_class_link(self.search_options.getJavaClassName())
        else:
            super().__init__(java_class)

    def visit(self, page: Page = None, document: Document = None):
        """!
        Extracts tables on the specified page
        """

        if page is None:
            self.getJavaClass().visit(document.getJavaClass())
        elif document is None:
            self.getJavaClass().visit(page.getJavaClass())

    def setUseFlowEngine(self, useFlowEngine: bool):
        """!
        Extracts tables on the specified page
        """

        self.getJavaClass().setUseFlowEngine(useFlowEngine)

    @property
    def getTableList(self) -> List[AbsorbedTable]:
        """!
        Returns readonly List containing tables that were found
        """
        table_list = []
        for java_table in self.getJavaClass().getTableList():
            table_list.append(AbsorbedTable(java_table))

        return table_list


class TextFragmentAbsorber(Assist.BaseJavaClass):
    """!
    Represents an absorber object of text fragments. Performs text search and provides access to
    search results via TextFragments collection.
    """

    javaClassName = "com.aspose.python.pdf.TextFragmentAbsorber"
    search_options = TextSearchOptions()

    def __init__(self, text: str = None, extraction_options=None, search_options=None, java_class=None):
        if java_class is None:
            self.extraction_options = extraction_options
            self.search_options = search_options
            self.search_text = text
            java_class_link = jpype.JClass(self.javaClassName)
            if extraction_options is None and search_options is None:
                if text is None:
                    self.javaClass = java_class_link()
                elif extraction_options is None:
                    self.javaClass = java_class_link(text)
            elif extraction_options is None:
                self.javaClass = java_class_link(text, self.search_options.setJavaClass())
            elif search_options is None:
                if text is None:
                    self.javaClass = java_class_link(self.extraction_options.setJavaClass())
                elif extraction_options is None:
                    self.javaClass = java_class_link(text, self.extraction_options.setJavaClass())
            else:
                self.javaClass = java_class_link(text, self.extraction_options.setJavaClass(),
                                                 self.search_options.setJavaClass())
        else:
            super().__init__(java_class)

    def visit(self, page: Page = None, document: Document = None):
        """!
        Performs search on the specified page or whole document.
        """

        if page is None:
            self.getJavaClass().visit(document.getJavaClass())
        elif document is None:
            self.getJavaClass().visit(page.getJavaClass())

    @property
    def getText(self):
        """!
        Gets extracted text that the TextAbsorber extracts on the PDF document or page.
        """
        return str(self.getJavaClass().getText())

    @property
    def getTextFragments(self) -> Api.TextFragmentCollection:
        """!
        Gets collection of search occurrences that are presented with {@code TextFragment} objects.
        """

        return Api.TextFragmentCollection(self.getJavaClass().getTextFragments())
