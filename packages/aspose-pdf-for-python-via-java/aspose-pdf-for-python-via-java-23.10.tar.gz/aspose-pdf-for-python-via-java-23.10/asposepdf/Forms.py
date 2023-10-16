from enum import Enum, IntEnum

import jpype
from asposepdf import Assist, Api
from jpype import java


class FieldType(IntEnum):
    Text = 0
    ComboBox = 1
    ListBox = 2
    Radio = 3
    CheckBox = 4
    PushButton = 5
    MultiLineText = 6
    Barcode = 7
    InvalidNameOrType = 8
    Signature = 9
    Image = 10
    Numeric = 11
    DateTime = 12


class PropertyFlag(Enum):
    """!
    Enumeration of possible field flags.
    """

    ReadOnly = 0
    """!
    Field is read-only.
    """

    Required = 1
    """!
    Field is required.
    """

    NoExport = 2
    """!
    Field is not exportable.
    """

    InvalidFlag = 3
    """!
    Invalid field flag.
    """


class Form(Assist.BaseJavaClass):
    """!
    Class representing Acro form object.
    """

    javaClassName = "com.aspose.python.pdf.facades.Form"
    sourceFileName = None
    document = None

    def __init__(self, document: Api.Document = None, sourceFileName: str = None):
        if document is not None:
            self.document = document
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(document.getJavaClass())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(sourceFileName)
        else:
            raise ValueError("Either 'document' or 'sourceFileName' must be specified")

    def bindPdf(self, sourceFileName: str, password: str = None):
        """!
        Initializes the Form from pdf protected by password.
        """

        if password is not None:
            self.sourceFileName = sourceFileName
            self.javaClass.bindPdf(sourceFileName)
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            self.javaClass.bindPdf(sourceFileName, password)
        else:
            raise ValueError("'sourceFileName' must be specified")

    def exportFdf(self, output_stream):
        """!
        Exports the content of the fields of the pdf into the fdf stream.
        """

        if output_stream is None:
            raise Exception("an argument is required")
        else:

            # Create a Java ByteArrayOutputStream object
            byte_output_stream = java.io.ByteArrayOutputStream()

            self.getJavaClass().exportFdf(byte_output_stream)

            # Convert the ByteArrayOutputStream to a Java byte array
            j_byte_array = byte_output_stream.toByteArray()

            # Convert the Java byte array to a Python bytearray
            py_byte_array = bytearray(j_byte_array)

            output_stream.write(py_byte_array)

            # Close the ByteArrayOutputStream object
            byte_output_stream.close()

    def importFdf(self, input_stream):
        """!
        Imports the content of the fields of the pdf from the fdf stream.
        """

        if input_stream is None:
            raise Exception("an argument is required")
        else:

            # Convert Python InputStream to Java ByteArrayInputStream
            java_byte_array_input_stream = jpype.java.io.ByteArrayInputStream(input_stream.read())

            self.getJavaClass().importFdf(java_byte_array_input_stream)

            # Close the ByteArrayInputStream object
            java_byte_array_input_stream.close()

    def close(self):
        """!
        Closes opened files without any changes.
        """

        self.getJavaClass().close()

    def exportXfdf(self, output_stream):
        """!
        Exports the content of the fields of the pdf into the xml stream. The button field's value will not be exported.
        """

        if output_stream is None:
            raise Exception("an argument is required")
        else:
            # Create a Java ByteArrayOutputStream object
            byte_output_stream = java.io.ByteArrayOutputStream()

            self.getJavaClass().exportXfdf(byte_output_stream)

            # Convert the ByteArrayOutputStream to a Java byte array
            j_byte_array = byte_output_stream.toByteArray()

            # Convert the Java byte array to a Python bytearray
            py_byte_array = bytearray(j_byte_array)

            output_stream.write(py_byte_array)

            # Close the ByteArrayOutputStream object
            byte_output_stream.close()

    def importXfdf(self, input_stream):
        """!
        Imports the content of the fields from the xfdf(xml) file and put them into the new pdf.
        """

        if input_stream is None:
            raise Exception("an argument is required")
        else:
            # Convert Python InputStream to Java ByteArrayInputStream
            java_byte_array_input_stream = jpype.java.io.ByteArrayInputStream(input_stream.read())

            self.getJavaClass().exportXfdf(java_byte_array_input_stream)

            # Close the ByteArrayOutputStream object
            java_byte_array_input_stream.close()

    def exportXml(self, output_stream):
        """!
        Exports the content of the fields of the pdf into the xml stream. The button field's value will not be exported.
        """

        if output_stream is None:
            raise Exception("an argument is required")
        else:
            # Create a Java ByteArrayOutputStream object
            byte_output_stream = java.io.ByteArrayOutputStream()

            self.getJavaClass().exportXml(byte_output_stream)

            # Convert the ByteArrayOutputStream to a Java byte array
            j_byte_array = byte_output_stream.toByteArray()

            # Convert the Java byte array to a Python bytearray
            py_byte_array = bytearray(j_byte_array)

            output_stream.write(py_byte_array)

            # Close the ByteArrayOutputStream object
            byte_output_stream.close()

    def importXml(self, input_stream, ignoreFormTemplateChanges=None):
        """!
        Imports the content of the fields from the xml file and put them into the new pdf.
        """

        if input_stream is None:
            raise Exception("an argument is required")
        else:
            # Convert Python InputStream to Java ByteArrayInputStream
            java_byte_array_input_stream = jpype.java.io.ByteArrayInputStream(input_stream.read())
            if ignoreFormTemplateChanges is None:
                self.getJavaClass().importXml(java_byte_array_input_stream)
            else:
                self.getJavaClass().importXml(java_byte_array_input_stream,ignoreFormTemplateChanges)

            # Close the ByteArrayOutputStream object
            java_byte_array_input_stream.close()

    def extractXfaData(self, output_stream):
        """!
        Extracts XFA data packet
        """

        if output_stream is None:
            raise Exception("an argument is required")
        else:
            # Create a Java ByteArrayOutputStream object
            byte_output_stream = java.io.ByteArrayOutputStream()

            self.getJavaClass().extractXfaData(byte_output_stream)

            # Convert the ByteArrayOutputStream to a Java byte array
            j_byte_array = byte_output_stream.toByteArray()

            # Convert the Java byte array to a Python bytearray
            py_byte_array = bytearray(j_byte_array)

            output_stream.write(py_byte_array)

            # Close the ByteArrayOutputStream object
            byte_output_stream.close()

    def setXfaData(self, input_stream):
        """!
        Replaces XFA data with specified data packet. Data packet may be extracted using extractXfaData
        """

        if input_stream is None:
            raise Exception("an argument is required")
        else:
            # Convert Python InputStream to Java ByteArrayInputStream
            java_byte_array_input_stream = jpype.java.io.ByteArrayInputStream(input_stream.read())
            self.getJavaClass().setXfaData(java_byte_array_input_stream)

            # Close the ByteArrayOutputStream object
            java_byte_array_input_stream.close()

    def fillBarcodeField(self, fieldName, data):
        """!
        Fill a barcode field according to its fully qualified field name.
        Args:
            fieldName (str): The fully qualified field name.
            data (str): The new barcode value.

        Returns:
            type (bool): If filling succeed, return true; otherwise, false.
        """

        if fieldName is None or data is None:
            raise Exception("arguments are required")
        else:
            result = self.getJavaClass().extractXfaData(fieldName, data)
            return bool(result)

    def fillField_checkBox(self, fieldName, beChecked):
        """!
        Fills the checkbox field with a boolean value. Notice: Only be applied to Check Box. Please
       note that Facades supports only full field names and does not work with partial
       field names in contrast with Aspose.Pdf.Kit; For example if field has full name
       "Form.Subform.CheckBoxField" you should specify full name and not "CheckBoxField". You can
       use FieldNames property to explore existing field names and search required field by its
       partial name.
        Args:
            fieldName (str): The field's name to be filled.
            beChecked (bool): A boolean flag: true means to check the box, while false to uncheck it.

        Returns:
            type (bool): true if field was found and successfully filled.
        """

        if fieldName is None or beChecked is None:
            raise Exception("arguments are required")
        else:
            result = self.getJavaClass().fillField(fieldName, beChecked)
            return bool(result)

    def fillField_radioBox(self, fieldName, index):
        """!
        Fills the radio-box field with a valid index value according to a fully qualified field name.
        Before filling the fields, only field's name must be known. While the value can be specified
        by its index. Notice: Only be applied to Radio Box, Combo Box and List Box fields. Please
        note that Facades supports only full field names and does not work with partial
        field names in contrast with Aspose.Pdf.Kit; For example if field has full name
        "Form.Subform.ListBoxField" you should specify full name and not "ListBoxField". You can use
        FieldNames property to explore existing field names and search required field by its partial
        name.
        Args:
            fieldName (str): The field's name to be filled.
            index (int): Index of chosen item.

        Returns:
            type (bool): true if field was found and successfully filled.
        """

        if fieldName is None or index is None:
            raise Exception("arguments are required")
        else:
            result = self.getJavaClass().fillField(fieldName, index)
            return bool(result)

    def fillField(self, fieldName, fieldValue, fitFontSize=None):
        """!
        Fills the field with a valid value according to a fully qualified field name. Before filling
        the fields, every field's names and its corresponding valid values must be known. Both the
        fields' name and values are case-sensitive. Please note that Facades supports only
        full field names and does not work with partial field names in contrast with Aspose.Pdf.Kit;
        For example if field has full name "Form.Subform.TextField" you should specify full name and
        not "TextField". You can use FieldNames property to explore existing field names and search
        required field by its partial name.
        Args:
            fieldName (str): The field's name to be filled.
            fieldValue (str): The field's value which must be a valid value for some fields.
            fitFontSize (bool): If true, the font size in the edit boxes will be fitted.

        Returns:
            type (bool): true if field was found and successfully filled.
        """

        if fieldName is None or fieldValue is None:
            raise Exception("arguments are required")
        else:
            if fitFontSize is None:
                result = self.getJavaClass().fillField(fieldName, fieldValue)
                return bool(result)
            else:
                result = self.getJavaClass().fillField(fieldName, fieldValue, fitFontSize)
                return bool(result)

    def fillField_listBox(self, fieldName, fieldValues):
        """!
        Fill a field with multiple selections.Note: only for AcroForm List Box Field.
        Args:
            fieldName (str): The field's name to be filled.
            fieldValues (List[str]): A String array which contains several items to be selected.

        Returns:
            type (bool): true if field was found and successfully filled.
        """

        if fieldName is None or fieldValues is None:
            raise Exception(" arguments are required")
        else:
            result = self.getJavaClass().fillField(fieldName, jpype.JArray(java.lang.String)(fieldValues))
            return bool(result)

    def fillImageField(self, fieldName, imageFileName):
        """!
        Pastes an image onto the existing button field as its appearance according to its fully
        qualified field name.
        Args:
            fieldName (str): The fully qualified field name of the image button field.
            imageFileName (str): The path of the image file, relative and absolute are both ok.
        """

        if fieldName is None or imageFileName is None:
            raise Exception("arguments are required")
        else:
            self.getJavaClass().fillImageField(fieldName, imageFileName)

    def flattenAllFields(self):
        """!
        Flattens all the fields.
        """

        self.getJavaClass().flattenAllFields()

    def flattenField(self, fieldName):
        """!
        Flattens a specified field with the fully qualified field name. Any other field will remain
        unchangeable. If the fieldName is invalid, all the fields will remain unchangeable.
        Args:
            fieldName (str): The name of the field to be flattened.
        """

        if fieldName is None:
            raise Exception("an argument are required")
        else:
            self.getJavaClass().flattenField(fieldName)

    def getButtonOptionCurrentValue(self, fieldName):
        """!
        Gets name of attachment when result of operation is stored into HttpResponse objects as attachment.
        Args:
            fieldName (str): String value for the current radio group option.
        Returns:
            type (str): Field Name
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            result = self.getJavaClass().getButtonOptionCurrentValue(fieldName)
            return str(result)

    @staticmethod
    def convert_hashtable_to_dict(java_hashtable):
        # Convert the Java Hashtable to a Python dictionary
        py_dict = {str(key): str(value) for key, value in java_hashtable.items()}
        return py_dict

    def getButtonOptionValues(self, fieldName):
        """!
        Gets the radio button option fields and related values based on the field name. This method
        has meaning for radio button groups.
        Args:
            fieldName (str): String value for the current radio group option.
        Returns:
            type (dict): Hash table of option values keyed by form item name
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            result = self.getJavaClass().getButtonOptionValues(fieldName)
            return self.convert_hashtable_to_dict(result)

    def getField(self, fieldName):
        """!
        Gets the field's value according to its field name.
        Args:
            fieldName (str): The fully qualified field name.
        Returns:
            type (str): The field's value.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            result = self.getJavaClass().getField(fieldName)
            return str(result)

    def getFieldFlag(self, fieldName):
        """!
        Get the limitation of text field.
        Args:
            fieldName (str): The qualified field name.
        Returns:
            type (str): list of field names on the form.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            result = self.getJavaClass().getFieldFlag(fieldName)
            return PropertyFlag(result)

    def getFieldNames(self, fieldName):
        """!
        Gets list of field names on the form.
        Args:
            fieldName (str): The field's name.

        Returns:
            type (list): list of field names on the form.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            result = self.getJavaClass().getFieldNames(fieldName)
            return list(result)

    def getFieldType(self, fieldName):
        """!
        Returns type of field.
        Args:
            fieldName (str): The field's name.

        Returns:
            type (list): Element of FileType enumeration corresponding to field type.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            java_enum_element = self.getJavaClass().getFieldType(fieldName)
            return FieldType(java_enum_element.getValue())

    def getFormSubmitButtonNames(self):
        """!
        Gets all form submit button names.

        Returns:
            type (list): list of all form submit button names.
        """

        result = self.getJavaClass().getFormSubmitButtonNames()
        return list(result)

    def getFullFieldName(self, fieldName):
        """!
        Gets the full field name according to its short field name.
        Args:
            fieldName (str): The field's name.

        Returns:
            type (str): The fully qualified field name.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            return self.getJavaClass().getFullFieldName(fieldName)

    def getRichText(self, fieldName):
        """!
        Get a Rich Text field's value, including the formatting information of every character.
        Args:
            fieldName (str): The field's name.

        Returns:
            type (str): The fully qualified field name of the Rich Text field.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            return self.getJavaClass().getRichText(fieldName)

    def isRequiredField(self, fieldName):
        """!
        Determines whether field is required or not.
        Args:
            fieldName (str): The field's name.

        Returns:
            type (bool): True - the field is required; otherwise, false.
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            return self.getJavaClass().isRequiredField(fieldName)

    def renameField(self, fieldName, newFieldName):
        """!
        Determines whether field is required or not.
        Args:
            fieldName (str): The field's name.
            newFieldName (str): The new field name
        """

        if fieldName is None:
            raise Exception("an argument is required")
        else:
            return self.getJavaClass().renameField(fieldName, newFieldName)

    def save(self, destFile):
        """!
        Saves document into specified file.
        Args:
            destFile (str): File where document will be saved.
        """

        if destFile is None:
            raise Exception("an argument is required")
        else:
            return self.getJavaClass().save(destFile)
