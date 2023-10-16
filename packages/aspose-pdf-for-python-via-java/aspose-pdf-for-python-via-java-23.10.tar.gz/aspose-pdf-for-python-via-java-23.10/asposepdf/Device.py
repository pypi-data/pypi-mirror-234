from enum import Enum

import jpype
from asposepdf import Assist, Api
from jpype import java


class CompressionType(Enum):
    """!
    Used to specify the parameter value passed to a Tiff image device.
    """

    LZW = 0
    """!
    Specifies the LZW compression scheme. Can be passed to the Tiff encoder as a parameter that
      belongs to the Compression category.
    """

    CCITT4 = 1
    """!
    Specifies the CCITT4 compression scheme. Can be passed to the CCITT4 encoder as a parameter
      that belongs to the Compression category.
    """

    CCITT3 = 2
    """!
    Specifies the CCITT3 compression scheme. Can be passed to the CCITT3 encoder as a parameter
      that belongs to the Compression category.
    """

    RLE = 3
    """!
    Specifies the RLE compression scheme. Can be passed to the RLE encoder as a parameter that
      belongs to the Compression category.
    """

    NoCompression = 4
    """!
    Specifies no compression. Can be passed to the Tiff encoder as a parameter that belongs to
      the compression category.
    """


class ColorDepth(Enum):
    """!
    Used to specify the parameter value passed to a Tiff image device.
    """

    Default = 0
    """!
     Default color depth
    """

    Format8bpp = 1
    """!
     8 bits per pixel. 
    """

    Format4bpp = 2
    """!
     4 bits per pixel.
    """

    Format1bpp = 3
    """!
     1 bit per pixel.
    """


class Resolution(Assist.BaseJavaClass):
    """!
    Represents class for holding image resolution.
    """

    javaClassName = "com.aspose.python.pdf.devices.Resolution"

    def __init__(self, parameter1, parameter2=None):
        javaClass = jpype.JClass(self.javaClassName)
        if parameter2 is None:
            self.javaClass = javaClass(parameter1)
        else:
            self.javaClass = javaClass(parameter1, parameter2)

    @property
    def getJClass(self):
        return self.javaClass


class TiffSettings(Assist.BaseJavaClass):
    """!
    This class represents settings for importing pdf to Tiff.
    """

    javaClassName = "com.aspose.python.pdf.devices.TiffSettings"
    _Skip_blank_pages = False
    _ColorDepth = ColorDepth.Default
    _CompressionType = CompressionType.LZW

    def __init__(self):
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass()

    @property
    def getJClass(self):
        self.javaClass.setDepth(self._ColorDepth.value)
        self.javaClass.setCompression(self._CompressionType.value)
        return self.javaClass


class TiffDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page by page into the one tiff image.
    """

    javaClassName = "com.aspose.python.pdf.devices.TiffDevice"
    _Settings = TiffSettings()
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution, settings):
        self._Settings = settings
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass, self._Settings.getJClass)

    def process(self, document, output_pdf):
        """!
        Converts certain document pages into tiff and save it in the output stream.
        """
        self.javaClass.process(document.getJClass, output_pdf)


class BmpDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one bmp image.
    """

    javaClassName = "com.aspose.python.pdf.devices.BmpDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass)

    def process(self, page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into bmp and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.javaClass, outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.javaClass, byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class EmfDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one bmp image.
    """

    javaClassName = "com.aspose.python.pdf.devices.EmfDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        java_class_tmp = jpype.JClass(self.javaClassName)
        self.javaClass = java_class_tmp(self._width, self._height, self._Resolution.getJClass)

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into emf and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
            print(outputStream.length())
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class JpegDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one jpeg image.
    """

    javaClassName = "com.aspose.python.pdf.devices.JpegDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass)

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into jpeg and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class PngDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one Png image.
    """

    javaClassName = "com.aspose.python.pdf.devices.PngDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass)

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into Png and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class GifDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one gif image.
    """

    javaClassName = "com.aspose.python.pdf.devices.GifDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass)

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into gif and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class GifDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one gif image.
    """

    javaClassName = "com.aspose.python.pdf.devices.GifDevice"
    _Resolution = Resolution(150)
    _width = 0
    _height = 0

    def __init__(self, resolution):
        self._Resolution = resolution
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass(self._width, self._height, self._Resolution.getJClass)

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into gif and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")


class TextDevice(Assist.BaseJavaClass):
    """!
    This class helps to save pdf document page into the one txt document.
    """

    javaClassName = "com.aspose.python.pdf.devices.TextDevice"

    def __init__(self):
        javaClass = jpype.JClass(self.javaClassName)
        self.javaClass = javaClass()

    def process(self, page: Api.Page, outputFileName=None, outputStream=None):
        """!
        Converts certain document page into gif and save it in the output stream or file.
        """
        if outputFileName is not None:
            self.javaClass.process(page.getJavaClass(), outputFileName)
        elif outputStream is not None:
            byte_output_stream = java.io.ByteArrayOutputStream()
            self.javaClass.process(page.getJavaClass(), byte_output_stream)
            outputStream.write(bytearray(byte_output_stream.toByteArray()))
        else:
            raise ValueError("Either 'outputFile' or 'outputStream' must be specified")
