# from __future__ import absolute_import

from enum import Enum

import jpype
from asposepdf import Assist
from jpype import java
from strenum import StrEnum


class License(Assist.BaseJavaClass):
    javaClassName = "com.aspose.python.pdf.License"

    def __init__(self):
        javaLicense = jpype.JClass(self.javaClassName)
        self.javaClass = javaLicense()
        super().__init__(self.javaClass)

    def setLicense(self, licensePath):
        if licensePath is None:
            raise Exception("an argument is required")
        elif licensePath.__class__.__name__ == 'str':
            self.getJavaClass().setLicense(licensePath)


class ConvertErrorAction(Enum):
    """!
    This class represents action for conversion errors.
    """

    Delete = 0
    """!
    Delete convert errors
    """

    Nothing = 1
    """!
    Do nothing with convert errors
    """


class PdfFormat(StrEnum):
    """!
    This class represents an pdf format.
    """

    PDF_A_1A = 'PDF_A_1A'
    """!
    Pdf/A-1a format
    """

    PDF_A_1B = 'PDF_A_1B'
    """!
    Pdf/A-1b format
    """

    PDF_A_2A = 'PDF_A_2A'
    """!
    Pdf/A-2a format
    """

    PDF_A_3A = 'PDF_A_3A'
    """!
    Pdf/A-3a format
    """

    PDF_A_2B = 'PDF_A_2B'
    """!
    Pdf/A-2b
    """

    PDF_A_2U = 'PDF_A_2U'
    """!
    Pdf/A-2u format
    """

    PDF_A_3B = 'PDF_A_3B'
    """!
    Pdf/A-3b format
    """

    PDF_A_3U = 'PDF_A_3U'
    """!
    Pdf/A-3u format
    """

    v_1_0 = 'v_1_0'
    """!
    Adobe version 1
    """

    v_1_1 = 'v_1_1'
    """!
    Adobe version 1.1
    """

    v_1_2 = 'v_1_2'
    """!
    Adobe version 1.2
    """

    v_1_3 = 'v_1_3'
    """!
    Adobe version 1.3
    """

    v_1_4 = 'v_1_4'
    """!
    Adobe version 1.4
    """

    v_1_5 = 'v_1_5'
    """!
    Adobe version 1.5
    """

    v_1_6 = 'v_1_6'
    """!
    Adobe version 1.6
    """

    v_1_7 = 'v_1_7'
    """!
    Adobe version 1.7
    """

    v_2_0 = 'v_2_0'
    """!
    Adobe version 2.0
    """

    PDF_UA_1 = 'PDF_UA_1'
    """!
    PDF/UA-1 format
    """

    PDF_X_1A_2001 = 'PDF_X_1A_2001'
    """!
    PDF/X-1a-2001 format
    """

    PDF_X_1A = 'PDF_X_1A'
    """!
    PDF/X-1a format
    """

    PDF_X_3 = 'PDF_X_3'
    """!
    PDF/X-3 format
    """

    ZUGFeRD = 'ZUGFeRD'
    """!
    ZUGFeRD format
    """


class SaveFormat(StrEnum):
    """!
    Specifies save format
    """

    Pdf = 'Pdf'
    """!
    means saving without change of format, i.e. as PDF use it please instead of
    'SaveFormat.None', that is obsolete one
    """

    Doc = 'Doc'
    """!
    means saving in DOC format
    """

    Xps = 'Xps'
    """!
    means saving in XPS format
    """

    Html = 'Html'
    """!
    means saving in XML format
    """

    Xml = 'Xml'
    """!
    means saving in TEX format i.e. format suitable for Latex text editor
    """

    TeX = 'TeX'
    """!
    means saving in DOCX format
    """

    DocX = 'DocX'
    """!
    means saving in SVG format
    """

    Svg = 'Svg'
    """!
    means saving in SVG format
    """

    MobiXml = 'MobiXml'
    """!
    means saving in MsExcel format
    """

    Excel = 'Excel'
    """!
    means saving in MsExcel format
    """

    Epub = 'Epub'
    """!
    means saving in EPUB format(special format of e-books)
    """


class LoadFormat(StrEnum):
    """!
    Specifies load format
    """

    CGM = 'CGM'
    """!
    means loading of document in CGM format
    """

    HTML = 'HTML'
    """!
    means loading of document in HTML format
    """

    EPUB = 'EPUB'
    """!
    means loading of document in EPUB format(special format of e-books)
    """

    XML = 'XML'
    """!
    means loading of document in XML format(special XML that represent logical structure of PDF document)
    """

    XSLFO = 'XSLFO'
    """!
    means loading of document in XSLFO format
    """

    PCL = 'PCL'
    """!
    means loading of document in PCL format
    """

    XPS = 'XPS'
    """!
    means loading of document in XPS format
    """

    TEX = 'TEX'
    """!
    means loading of document in TEX format - format of Latex text editor
    """

    SVG = 'SVG'
    """!
    means loading of document in SVG format - format of Latex text editor
    """

    MHT = 'MHT'
    """!
    means loading of document in MHT format(that is packed HTML format)
    """

    PS = 'PS'
    """!
    means loading of document in PS format(format of PostScript document) 
    """

    MD = 'MD'
    """!
    means loading document is in MD format (markdown). 
    """

    TXT = 'TXT'
    """!
    means loading document is in TXT format. 
    """

    PDFXML = 'PDFXML'
    """!
    Internal PDF document structure in XML format. 
    """


class Document(Assist.BaseJavaClass):
    """!
    Class representing PDF document
    """

    javaClassName = "com.aspose.python.pdf.Document"

    def __init__(self, parameter1=None, options=None):

        if parameter1 is None:
            java_class_tmp = jpype.JClass(Document.javaClassName)
            super().__init__(java_class_tmp())
        elif options is None:
            if parameter1.__class__.__name__ == 'bytes':
                java_class_tmp = jpype.JClass(Document.javaClassName)
                # Convert the Python bytearray to a Java byte array
                j_byte_array = java.nio.ByteBuffer.wrap(parameter1)
                # Create a ByteArrayInputStream object from the Java byte array
                byte_input_stream = java.io.ByteArrayInputStream(j_byte_array.array())
                super().__init__(java_class_tmp(byte_input_stream))
            elif parameter1.__class__.__name__ == 'str':
                java_class_tmp = jpype.JClass(Document.javaClassName)
                super().__init__(java_class_tmp(parameter1))
        if parameter1.__class__.__name__ == 'str':
            java_class_tmp = jpype.JClass(Document.javaClassName)
            if isinstance(options, LoadFormat):
                super().__init__(java_class_tmp(parameter1, LoadOptions.getLoadOptions(options)))
            elif isinstance(options, LoadOptions):
                j_class = options.getJClass
                super().__init__(java_class_tmp(parameter1, j_class))
        elif parameter1.__class__.__name__ == 'bytes':
            java_class_tmp = jpype.JClass(Document.javaClassName)

            # Convert the Python bytearray to a Java byte array
            j_byte_array = java.nio.ByteBuffer.wrap(parameter1)

            # Create a ByteArrayInputStream object from the Java byte array
            byte_input_stream = java.io.ByteArrayInputStream(j_byte_array.array())

            if isinstance(options, LoadFormat):
                super().__init__(java_class_tmp(byte_input_stream, LoadOptions.getLoadOptions(options)))
            elif isinstance(options, LoadOptions):
                super().__init__(java_class_tmp(byte_input_stream, options))

    def close(self):
        """!
        Closes all resources used by this document.
        """
        self.getJavaClass().close()

    def save(self, fileName, options=None):
        """!
        Saves the document with a new name along with a file format.
        """

        if fileName is None:
            self.getJavaClass().save()
        elif options is None:
            self.getJavaClass().save(fileName)
        elif fileName.__class__.__name__ == 'str':
            if isinstance(options, SaveFormat):
                self.getJavaClass().save(fileName, SaveOptions.getSaveOptions(options))
            if isinstance(options, SaveOptions):
                self.getJavaClass().save(fileName, options.getJClass)

    def convert(self, output_log, pdf_format, convert_error_action):
        """!
        Convert document and save errors into the specified file.
        """

        if pdf_format is None or convert_error_action is None:
            raise Exception("an argument is required")
        else:
            self.getJavaClass().convert(output_log, jpype.JClass("com.aspose.python.pdf.PdfFormat").valueOf(pdf_format),
                                        convert_error_action.value)

    def save_in_bytes(self, options=None):
        """!
        Saves the document into byte array with a selected file format.
        :param options:
        :return: byte_array
        """

        SaveFormatClass = "com.aspose.python.pdf.SaveFormat"
        javaClass = jpype.JClass(SaveFormatClass)

        # Create a Java ByteArrayOutputStream object
        byte_output_stream = java.io.ByteArrayOutputStream()

        if options is None:
            self.getJavaClass().save(byte_output_stream);
        else:
            if isinstance(options, SaveFormat):
                self.getJavaClass().save(byte_output_stream, javaClass.valueOf(options))
            if isinstance(options, SaveOptions):
                self.getJavaClass().save(byte_output_stream, options.getJClass)

        # Convert the ByteArrayOutputStream to a Java byte array
        j_byte_array = byte_output_stream.toByteArray()

        # Convert the Java byte array to a Python bytearray
        py_byte_array = bytearray(j_byte_array)

        # Close the ByteArrayOutputStream object
        byte_output_stream.close()

        # Return the Python bytearray
        return py_byte_array

    def flatten(self):
        """!
        Removes all fields (and annotations) from the document and place their values instead.
        """
        self.getJavaClass().flatten()

    def optimize(self):
        """!
        Linearize document in order to - open the first page as quickly as possible; - display next
        page or follow by link to the next page as quickly as possible; - display the page
        incrementally as it arrives when data for a page is delivered over a slow channel (display
        the most useful data first); - permit user interaction, such as following a link, to be
        performed even before the entire page has been received and displayed. Invoking this method
        doesn't actually save the document. On the contrary the document only is prepared to have
        optimized structure, call then Save to get optimized document.
        """
        self.getJavaClass().optimize()

    def optimize_resources(self):
        """!
        Optimize resources in the document: 1. Resources which are not used on the document pages are
        removed; 2. Equal resources are joined into one object; 3. Unused objects are deleted.
        """
        self.getJavaClass().optimize_resources()

    @property
    def getJClass(self):
        return self.javaClass

    @property
    def pages(self):
        return PageCollection(self.getJavaClass().getPages())


class BaseParagraph(Assist.BaseJavaClass):
    """!
    Represents an abstract base object can be added to the page
    """

    javaClassName = "com.aspose.python.pdf.BaseParagraph"

    def __init__(self, java_class):
        super().__init__(java_class)


class Paragraphs(Assist.BaseJavaClass):
    """!
    This class represents paragraph collection.
    """

    javaClassName = "com.aspose.python.pdf.Paragraphs"

    def __init__(self, paragraph_collection):
        super().__init__(paragraph_collection)

    def get_item(self, paragraph_number) -> BaseParagraph:
        """
        Gets paragraph from collection.
        :param paragraph_number: Index of paragraph.
        :return: Retrieved paragraph.
        """
        return BaseParagraph(self.javaClass.get_item(paragraph_number))

    def add(self, paragraph: BaseParagraph):
        """
        Adds paragraph to collection.
        :param paragraph: Page to add
        :return: Added page.
        """
        self.javaClass.add(paragraph.javaClass)

    def insert(self, index, paragraph: BaseParagraph):
        """
        Insert paragraph to collection.
        :param index: The index for paragraph.
        :param paragraph: Page to add
        :return: Added page.
        """
        self.javaClass.insert(index, paragraph.javaClass)

    def set_item(self, index, paragraph: BaseParagraph):
        """
        Sets paragraph to collection.
        :param index: The index for paragraph.
        :param paragraph: Page to add
        :return: Added page.
        """
        self.javaClass.set_Item(index, paragraph.javaClass)

    def remove(self, paragraph: BaseParagraph):
        """
        Remove paragraph from collection.
        :param paragraph: Page to add
        :return: Added page.
        """
        self.javaClass.remove(index, paragraph.javaClass)

    def remove_range(self, index, count):
        """
        Remove paragraph from collection.
        :param count: The paragraphs count.
        :param index: The first paragraph index.
        :return: Added page.
        """
        self.javaClass.removeRange(index, count)

    @property
    def size(self):
        """
        Get paragraphs count.
        :param self:
        :return: paragraphs count.
        """
        return self.javaClass.getCount()


class Page(Assist.BaseJavaClass):
    """!
    Class representing PDF document's page
    """

    javaClassName = "com.aspose.python.pdf.Page"

    def __init__(self, java_class):
        super().__init__(java_class)

    @property
    def paragraphs(self) -> Paragraphs:
        """!
        Gets the paragraphs.
        """
        return Paragraphs(self.getJavaClass().getParagraphs())


class PageCollection(Assist.BaseJavaClass):
    """!
    Class representing PDF document's page collection
    """

    javaClassName = "com.aspose.python.pdf.PageCollection"

    def __init__(self, page_collection):
        super().__init__(page_collection)

    def get_item(self, page_number) -> Page:
        """
        Gets page by index.
        :param page_number: Index of page.
        :return: Retrieved page.
        """
        return Page(self.javaClass.get_Item(page_number))

    def add(self, page: Page = None) -> Page:
        """
        Adds page to collection.
        :param page: Page to add
        :return: Added page.
        """
        if page is not None:
            return Page(self.javaClass.add(page))
        else:
            return Page(self.javaClass.add())

    def insert(self, index, page: Page = None) -> Page:
        """
        Insert page into collection at the specified position.
        :param index: The index for page.
        :param page: Page to add
        :return: Added page.
        """
        if Page is None:
            return Page(self.javaClass.insert(index))
        else:
            return Page(self.javaClass.insert(index, page.javaClass))

    def delete(self, index):
        """
        Delete specified page.
        :param index: The index for page.
        """
        self.javaClass.delete(index)

    @property
    def size(self):
        return self.javaClass.size()


class LoadOptions:

    @staticmethod
    def getLoadOptions(loadFormat: LoadFormat):
        if loadFormat == LoadFormat.SVG:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.SvgLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XPS:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XpsLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.CGM:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.CgmLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XSLFO:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XslFoLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.PS:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PsLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.XML:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XmlLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.EPUB:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.EpubLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.HTML:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.HtmlLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.MD:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MdLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.MHT:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MhtLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.PCL:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PclLoadOptions')
            return Options()
        elif loadFormat == LoadFormat.TEX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.TeXLoadOptions')
            return Options()


    @property
    def getLoadFormat(self):
        return self.__loadFormat

    @property
    def getJClass(self):
        return self._jClass


class EpubLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.EPUB

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.EpubLoadOptions")()


class HtmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.HTML

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.HtmlLoadOptions")()


class MdLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MD

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.MdLoadOptions")()


class MhtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.MHT

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.MhtLoadOptions")()


class PclLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PCL

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.PclLoadOptions")()


class PdfXmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PDFXML

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.PdfXmlLoadOptions")()


class PsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.PS

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.PsLoadOptions")()


class SvgLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.SVG

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.SvgLoadOptions")()


class TeXLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TEX

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.TeXLoadOptions")()


class TxtLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.TXT

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.TxtLoadOptions")()


class XmlLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XML

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.XmlLoadOptions")()


class XpsLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XPS

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.XpsLoadOptions")()


class XslFoLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.XSLFO

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.XslFoLoadOptions")()


class CgmLoadOptions(LoadOptions):
    __loadFormat = LoadFormat.CGM

    def __init__(self):
        self._jClass = jpype.JClass("com.aspose.python.pdf.CgmLoadOptions")()


class SaveOptions:

    @staticmethod
    def getSaveOptions(saveFormat: SaveFormat):

        if saveFormat == SaveFormat.Svg:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.SvgSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.DocX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Pdf:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.PdfSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Excel:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.ExcelSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Html:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.HtmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Epub:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.EpubSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.DocX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')()
            Options.setFormat(
                jpype.JClass("com.aspose.python.pdf.DocSaveOptions.DocFormat.DocX"))
            return Options
        elif saveFormat == SaveFormat.Doc:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.DocSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.MobiXml:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.MobiXmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Xml:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XmlSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.Xps:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.XpsSaveOptions')
            return Options()
        elif saveFormat == SaveFormat.TeX:
            # Import the class
            Options = jpype.JClass('com.aspose.python.pdf.TeXSaveOptions')
            return Options()

    @property
    def getLoadFormat(self):
        return self.__loadFormat

    @property
    def getJClass(self):
        return self.__jClass


class DocSaveOptions(SaveOptions):
    class DocFormat(StrEnum):
        """!
        Allows to specify .doc or .docx file format.
        """

        Doc = 'Doc'
        """!
        [MS-DOC]: Word (.doc) Binary File Format
        """

        Docx = 'Docx'
        """!
        Office Open XML (.docx) File Format
        """

    class RecognitionMode(StrEnum):
        """!
        Allows to control how a PDF document is converted into a word processing document.
        """

        Textbox = 'Textbox'
        """!
        This mode is fast and good for maximally preserving original look of the PDF file, but
        editability of the resulting document could be limited.
        """

        Flow = 'Flow'
        """!
        Full recognition mode, the engine performs grouping and multi-level analysis to restore
        the original document author's intent and produce a maximally editable document. The
        downside is that the output document might look different from the original PDF file.
        """

        EnhancedFlow = 'EnhancedFlow'
        """!
        An early alfa version of a new Flow mode supporting recognition of tables.
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.DocSaveOptions")()
    format = DocFormat.Doc
    mode = RecognitionMode.Flow
    relative_horizontal_proximity = 1.5
    recognize_bullets = False

    @property
    def getJClass(self):

        if self.format == self.DocFormat.Doc:
            self.__jClass.setFormat(0)
        else:
            self.__jClass.setFormat(1)

        if self.mode == self.RecognitionMode.Textbox:
            self.__jClass.setMode(0)
        elif self.mode == self.RecognitionMode.Flow:
            self.__jClass.setMode(1)
        else:
            self.__jClass.setMode(2)

        self.__jClass.setRelativeHorizontalProximity(self.relative_horizontal_proximity)
        self.__jClass.setRecognizeBullets(self.recognize_bullets)
        return self.__jClass


class ExcelSaveOptions(SaveOptions):
    class ExcelFormat(StrEnum):
        """!
        Allows to specify .xls/xml or .xlsx file format. Default value is XLSX;
        """

        XMLSpreadSheet2003 = 'XMLSpreadSheet2003'
        """!
        Excel 2003 XML Format
        """

        XLSX = 'XLSX'
        """!
        Office Open XML (.xlsx) File Format
        """

        CSV = 'CSV'
        """!
        A comma-separated values (CSV) File Format
        """

        XLSM = 'XLSM'
        """!
        A macro-enabled Office Open XML (.xlsm) File Format
        """

        ODS = 'ODS'
        """!
        OpenDocument Spreadsheet
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.ExcelSaveOptions")()
    _format = ExcelFormat.XLSX
    _minimizeTheNumberOfWorksheets = False
    _insertBlankColumnAtFirst = False
    _uniformWorksheets = False

    @property
    def getJClass(self):
        if self._format == self.ExcelFormat.XMLSpreadSheet2003:
            self.__jClass.setFormat(0)
        elif self._format == self.ExcelFormat.XLSX:
            self.__jClass.setFormat(1)
        elif self._format == self.ExcelFormat.CSV:
            self.__jClass.setFormat(2)
        elif self._format == self.ExcelFormat.XLSM:
            self.__jClass.setFormat(3)
        elif self._format == self.ExcelFormat.ODS:
            self.__jClass.setFormat(4)

        self.__jClass.setInsertBlankColumnAtFirst(self._insertBlankColumnAtFirst)
        self.__jClass.setMinimizeTheNumberOfWorksheets(self._minimizeTheNumberOfWorksheets)
        self.__jClass.setUniformWorksheets(self._uniformWorksheets)
        return self.__jClass


class HtmlSaveOptions(SaveOptions):
    class FontSavingModes(StrEnum):
        """!
        Enumerates modes that can be used for saving of fonts referenced in saved PDF
        """

        AlwaysSaveAsWOFF = 'AlwaysSaveAsWOFF'
        """!
        All referenced fonts will be saved and referenced as WOFF-fonts
        """

        AlwaysSaveAsTTF = 'AlwaysSaveAsTTF'
        """!
        All referenced fonts will be saved and referenced as TTF-fonts
        """

        AlwaysSaveAsEOT = 'AlwaysSaveAsEOT'
        """!
        All referenced fonts will be saved and referenced as EOT-fonts
        """

        SaveInAllFormats = 'SaveInAllFormats'
        """!
        All referenced fonts will be saved (and referenced in CSS) as 3 independent files : EOT,
         * TTH,WOFF. It increases size of output data but makes output suitable for overwhelming
         * majority of web browsers
        """

        DontSave = 'DontSave'
        """!
        All referenced fonts will not be saved.
        """

    __jClass = jpype.JClass("com.aspose.python.pdf.HtmlSaveOptions")()
    _fontSavingMode = FontSavingModes.AlwaysSaveAsWOFF
    _splitIntoPages = False
    _splitCssIntoPages = False
    _useZOrder = False

    @property
    def getJClass(self):
        if self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsWOFF:
            self.__jClass.setFontSavingMode(0)
        elif self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsTTF:
            self.__jClass.setFontSavingMode(1)
        elif self._fontSavingMode == self.FontSavingModes.AlwaysSaveAsEOT:
            self.__jClass.setFontSavingMode(2)
        elif self._fontSavingMode == self.FontSavingModes.SaveInAllFormats:
            self.__jClass.setFontSavingMode(3)
        elif self._fontSavingMode == self.FontSavingModes.DontSave:
            self.__jClass.setFontSavingMode(4)

        self.__jClass.setSplitCssIntoPages(self._splitIntoPages)
        self.__jClass.setSplitCssIntoPages(self._splitCssIntoPages)
        self.__jClass.setUseZOrder(self._useZOrder)
        return self.__jClass


class PptxSaveOptions(SaveOptions):
    __jClass = jpype.JClass("com.aspose.python.pdf.PptxSaveOptions")()
    _ImageResolution = 192
    _SlidesAsImages = False
    _SeparateImages = False
    _OptimizeTextBoxes = False

    @property
    def getJClass(self):
        self.__jClass.setSlidesAsImages(self._SlidesAsImages)
        self.__jClass.setSeparateImages(self._SeparateImages)
        self.__jClass.setOptimizeTextBoxes(self._OptimizeTextBoxes)
        return self.__jClass


class PdfFileEditor(SaveOptions):
    __jClass = jpype.JClass("com.aspose.python.pdf.facades.PdfFileEditor")()

    def concatenate(self, firstInputFile, secInputFile, outputFile):
        self.__jClass.concatenate(firstInputFile, secInputFile, outputFile)


class TextFragment(Assist.BaseJavaClass):
    """!
    Represents fragment of Pdf text.
    """

    javaClassName = "com.aspose.python.pdf.TextFragment"

    def __init__(self, text=None, java_class=None):
        if java_class is None:
            self.text = text
            java_class_link = jpype.JClass(self.javaClassName)
            if text is None:
                self.javaClass = java_class_link()
            else:
                self.javaClass = java_class_link(self.text)
        else:
            super().__init__(java_class)

    @property
    def getPage(self) -> Page:
        """!
        Gets page that contains the TextFragment
        The value can be null in case the TextFragment object doesn't belong to any page.
        """
        return Page(self.getJavaClass().page())

    def getText(self) -> str:
        """!
        Gets string text object that the TextFragment object represents.
        :return: text
        """
        return str(self.getJavaClass().getText())

    def setText(self, replace_text):
        """!
        Sets {@code string} text object that the {@code TextFragment} object represents.
        :param replace_text: String value
        """
        return str(self.getJavaClass().setText(replace_text))

    @property
    def getRectangle(self):
        """!
        Gets rectangle of the TextFragment
        :return: Gets rectangle of the TextFragment
        """
        return Rectangle(self.getJavaClass().get_rectangle())


class TextFragmentCollection(Assist.BaseJavaClass):
    """!
    Represents a text fragments collection
    """

    javaClassName = "com.aspose.python.pdf.TextFragmentCollection"

    def __init__(self, java_class):
        super().__init__(java_class)

    def clear(self):
        """!
        Clears all items from the collection.
        """
        self.getJavaClass().clear()

    def get_item(self, index: int) -> TextFragment:
        """!
        Gets the text fragment element at the specified index.
        :return: TextFragment
        :param index:
        """
        return TextFragment(java_class=self.getJavaClass().get_Item(index))

    @property
    def size(self):
        """!
        Gets the number of {@code TextFragment} object elements actually contained in the collection.
        :return: TextFragment elements count
        """
        return self.getJavaClass().size()


class Rectangle(Assist.BaseJavaClass):
    """!
    Class represents rectangle.
    """

    javaClassName = "com.aspose.python.pdf.Rectangle"

    def __init__(self, llx=None, lly=None, urx=None, ury=None, java_class=None):
        """!
        Rectangle constructor.
       @param llx X of lower left corner.
       @param lly Y of lower left corner.
       @param urx of upper right corner.
       @param ury of upper right corner.
        """
        if java_class is None:
            java_class = jpype.JClass(self.javaClassName)
            self.javaClass = java_class(llx, lly, urx, ury)
            super().__init__(self.javaClass)
        else:
            super().__init__(java_class)

    def getLLX(self):
        """!
        Gets X-coordinate of lower - left corner.
        @return Gets X-coordinate of lower - left corner.
        """
        return int(self.getJavaClass().getLLX())

    def getLLY(self):
        """!
       Gets Y - coordinate of lower-left corner.
        @return Gets Y - coordinate of lower-left corner.
        """
        return int(self.getJavaClass().getLLY())

    def getURX(self):
        """!
        Gets X - coordinate of upper-right corner.
        @returns Gets X - coordinate of upper-right corner.
        """
        return self.getURX()

    def getURY(self):
        """!
        Gets Y - coordinate of upper-right corner.
        @returns Gets Y - coordinate of upper-right corner.
        """
        return self.getURY()

    def getWidth(self):
        """!
        Returns the width of the bounding Rectangle in
        double precision.
        @return the width of the bounding Rectangle.
        """
        return int(self.getJavaClass().getWidth())

    def getHeight(self):
        """!
        Returns the height of the bounding Rectangle in
        double precision.
        @return the height of the bounding Rectangle.
        """
        return int(self.getJavaClass().getHeight())

    def toString(self):
        return str(self.getJavaClass().toString())

    def equals(self, obj):
        return self.getJavaClass().equals(obj.getJavaClass())

    def intersect(self, rectangle: 'Rectangle'):
        """!
       Intersects to rectangles.
       @param rectangle
       @returns {boolean
        """
        return self.getJavaClass().intersect(rectangle.javaClass)

    @property
    def isEmpty(self) -> bool:
        """
        Checks if rectangle is empty.
        :return:
        """
        return self.getJavaClass().isEmpty
