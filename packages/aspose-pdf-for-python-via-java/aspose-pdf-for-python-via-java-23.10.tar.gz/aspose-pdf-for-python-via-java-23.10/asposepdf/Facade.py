import jpype
from asposepdf import Assist
from asposepdf.Api import Document
from asposepdf.Assist import JavaRectangle


class Facade(Assist.BaseJavaClass):
    """!
    Base facade class.
    """

    javaClassName = "com.aspose.python.pdf.facades.Facade"
    sourceFileName = None
    document = None

    def __init__(self, document: Document = None, sourceFileName: str = None):
        if document is not None:
            self.document = document
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(document.getJavaClass())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(sourceFileName)
        else:
            self.javaClass = jpype.JClass(self.javaClassName)()

    def getJavaClass(self):
        return self.javaClass

    def setJavaClass(self, javaClass):
        self.javaClass = javaClass

    def getJavaClassName(self):
        return self.javaClassName

    def bindPdf(self, document: Document = None, sourceFileName: str = None):
        """!
        Initializes the facade.
        """

        if document is not None:
            self.document = document
            self.javaClass.bindPdf(document.getJavaClass())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            self.javaClass.bindPdf(sourceFileName)
        else:
            raise ValueError("Either 'document' or 'sourceFileName' must be specified")

    def bindPdfFile(self, sourceFileName: str, password: str = None):
        """!
        Initializes the facade from pdf protected by password.
        """

        if password is not None:
            self.sourceFileName = sourceFileName
            self.javaClass.bindPdf(sourceFileName)
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            self.javaClass.bindPdf(sourceFileName, password)
        else:
            raise ValueError("'sourceFileName' must be specified")


class Signature(Assist.BaseJavaClass):
    """!
    An abstract class which represents signature object in the pdf document. Signatures are fields
    with values of signature objects, the last contain data which is used to verify the document
    validity.
    """

    javaClassName = "com.aspose.python.pdf.Signature"

    def close(self):
        """!
        Destructor which closes temporary streams (if necessary).
        """
        self.javaClass.close()


class PKCS7(Signature):
    """!
    Represents the PKCS#7 object that conform to the PKCS#7 specification in Internet
    RFC 2315, PKCS#7: Cryptographic Message Syntax, Version 1.5. The SHA1 digest of the document's byte range is
    encapsulated in the PKCS#7 SignedData field.
    """

    javaClassName = "com.aspose.python.pdf.PKCS7"

    def __init__(self, pfx, password):
        """!
        Initializes new instance of the Signature class.
        """
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(pfx, password)


class PKCS7Detached(Signature):
    """!
    Represents the PKCS#7 object that conform to the PKCS#7 specification in Internet RFC 2315, PKCS
    #7: Cryptographic Message Syntax, Version 1.5. The original signed message digest over the
    document's byte range is incorporated as the normal PKCS#7 SignedData field. No data shall is
    encapsulated in the PKCS#7 SignedData field.
    """

    javaClassName = "com.aspose.python.pdf.PKCS7Detached"

    def __init__(self, pfx, password):
        """!
        Initializes new instance of the Signature class.
        """
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(pfx, password)


class PdfFileSignature(Facade):
    """!
    Represents a class to sign a pdf file with a certificate.
    """

    javaClassName = "com.aspose.python.pdf.facades.PdfFileSignature"

    def __init__(self, document: Document = None):
        """!
        Initializes new PdfFileSignature object.
        """
        if document is None:
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass()
        else:
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(document.getJavaClass())

    @property
    def containsSignature(self):
        """!
        Checks if the pdf has a digital signature or not.
        """
        return self.javaClass.containsSignature()

    @property
    def containsUsageRights(self):
        """!
        Checks if the pdf has a usage rights or not.
        """
        return self.javaClass.containsUsageRights()

    @property
    def isCertified(self):
        """!
        Gets the flag determining whether a document is certified or not.
        """
        return self.javaClass.isCertified()

    @property
    def isLtvEnabled(self):
        """!
        Gets the LTV enabled flag.
        """
        return self.javaClass.isLtvEnabled()

    def delete(self, fieldName: str):
        """!
        Deletes field from the form by its name.
        """
        self.javaClass.delete(fieldName)

    def close(self):
        """!
        Closes the facade.
        """
        self.javaClass.close()

    def removeUsageRights(self):
        """!
        Removes the usage rights entry.
        """
        self.javaClass.removeUsageRights()

    def setCertificate(self, pfx, password):
        """!
        Set certificate file and password for signing routine.
        Args:
        pfx (str): Path to the certificate file (PFX format).
        password (str): Password for the certificate file.
        """
        self.javaClass.setCertificate(pfx, password)

    def sign(self, page: int, SigReason: str, SigContact: str, SigLocation: str, visible: bool, annotRect: JavaRectangle):
        """!
        Make a signature on the pdf document with PKCS1 certificate
        """
        self.javaClass.sign(page, SigReason, SigContact, SigLocation, visible, annotRect.getJavaClass())

    def signWithCertificate(self, page: int, visible: bool, annotRect: JavaRectangle, certificate: Signature):
        """!
        Make a signature on the pdf document with added certificate
        """
        self.javaClass.sign(page, visible, annotRect.getJavaClass(), certificate.getJavaClass())

    def save(self, fileName):
        """!
        Saves the result PDF to file.
        """

        if fileName is None:
            self.getJavaClass().save()
        else:
            self.getJavaClass().save(fileName)


class Form(Facade):
    """!
    Class representing Acro form object.
    """

    javaClassName = "com.aspose.python.pdf.facades.Form"
    sourceFileName = None
    document = None

    def __init__(self, document: Document = None, sourceFileName: str = None):
        if document is not None:
            self.document = document
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(document.getJavaClass())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(sourceFileName)
        else:
            self.javaClass = jpype.JClass(self.javaClassName)()

    def delete(self, fieldName):
        """!
        Deletes field from the form by its name.
        """
        self.javaClass.delete(fieldName)

    def flatten(self):
        """!
        Removes all static form fields and place their values directly on the page.
        """
        self.javaClass.flatten()

    def hasField(self, fieldName):
        """!
        Determines if the field with specified name already added to the Form.
        """
        return self.javaClass.hasField(fieldName)

    def hasXfa(self):
        """!
        Determines if the form has Xfa
        """
        return self.javaClass.hasXfa()

    def isReadOnly(self):
        """!
        Determines if collection is readonly. Always returns false.
        """
        return self.javaClass.isReadOnly()

    def isSignaturesExist(self):
        """!
        If set, the document contains at least one signature field.
        """
        return self.javaClass.getSignaturesExist()

    def size(self):
        """!
        Gets number of the fields on this form.
        """
        return self.javaClass.size()

