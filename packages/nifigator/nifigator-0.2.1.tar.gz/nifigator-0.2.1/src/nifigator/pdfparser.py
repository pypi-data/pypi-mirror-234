# -*- coding: utf-8 -*-

import regex
import logging
from collections import namedtuple
from io import BytesIO
from typing import Union

from lxml import etree
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class PDFDocument:
    def __init__(
        self,
        join_hyphenated_words: bool = True,
        ignore_control_characters: str = "[\x00-\x08\x0b-\x0c\x0e-\x1f]",
    ):
        self.join_hyphenated_words = join_hyphenated_words
        self.control_characters_to_ignore = regex.compile(ignore_control_characters)
        self.PDF_offset = namedtuple(
            "PDF_offset", ["pageNumber", "beginIndex", "endIndex"]
        )

    def parse(
        self,
        file: Union[str, BytesIO] = None,
        codec: str = "utf-8",
        password: str = "",
        laparams: LAParams = LAParams(),
    ):
        """Function to convert pdf to xml or text

        Args:

            file: location or stream of the file to be converted
            codec: codec to be used to conversion
            password: password to be used for conversion
            laparams: laparams for the pdfminer.six parser
            join_hyphenated_words: Join 'hyhen-\\n ated wor- \\nds' to 'hyphenated words'

        Returns:

        """
        rsrcmgr = PDFResourceManager()
        retstr = BytesIO()
        device = XMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        if isinstance(file, str):
            fp = open(file, "rb")
        else:
            fp = BytesIO(file)

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(
            fp,
            pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=False,
        ):
            interpreter.process_page(page)

        # in case the file is opened, it is closed (a stream is not closed)
        if not isinstance(file, BytesIO):
            fp.close()
        device.close()

        result = retstr.getvalue()
        retstr.close()

        self.tree = etree.fromstring(result)

        return self

    def open(self, input: Union[str, bytes]):
        """Function to open a PDFDocument in xml
        Args:
            input: the location of the PDFDocument in xml to be opened or a bytes object containing the file content
        """
        if isinstance(input, str):
            with open(input, "r", encoding="utf-8") as f:
                self.tree = etree.parse(f).getroot()
        elif type(input) == bytes:
            stream_data = io.BytesIO(input)
            self.tree = etree.parse(stream_data).getroot()
        else:
            raise TypeError(
                "invalid input, instead of bytes or string it is" + str(type(input))
            )
        return self

    def write(self, output: str) -> None:
        """Function to write an PDFDocument in xml
        Args:
            output: the location of the PDFDocument in xml to be stored
        """
        self.tree.getroottree().write(
            output, encoding="utf-8", pretty_print=True, xml_declaration=True
        )

    def getstream(self) -> bytes:
        """
        Function to stream the PDFDocument in xml
        Returns: Bytesstream of the PDFDocument in xml
        """
        output = io.BytesIO()
        super().write(output, encoding="utf-8", pretty_print=True, xml_declaration=True)
        return output

    @property
    def text(self):
        """
        Property to extract text from PDFDocument
        Return: str
        """
        # setup regexes
        _hyphens = "\u00AD\u058A\u05BE\u0F0C\u1400\u1806\u2010\u2011\u2012\u2e17\u30A0-"
        _hyphen_newline = regex.compile(
            r"(?<=\p{L})[" + _hyphens + "][ \t\u00a0\r]*\n{1,2}[ \t\u00a0]*(?=\\p{L})"
        )

        text = []
        for page in self.tree:
            for textbox in page:
                if textbox.tag == "textbox":
                    for textline in textbox:
                        for text_element in textline:
                            text.append(text_element.text)
                    text.append("\n")
                elif textbox.tag == "figure":
                    for text_element in textbox:
                        if (
                            text_element.text is not None
                            and text_element.text != "\n        "
                        ):
                            text.append(text_element.text)
                elif textbox.tag == "textline":
                    for text_element in textbox:
                        text.append(text_element.text)
        text = "".join([t for t in text if t is not None])

        # delete control characters
        text = self.control_characters_to_ignore.sub("", text)

        # delete hyphens
        if self.join_hyphenated_words:
            text = _hyphen_newline.subn("", text)[0]

        return text

    @property
    def page_offsets(self):
        """
        Property to extract page offsets from PDFDocument
        Return: list of PDF_offset elements (named tuples)
        """

        # setup regexes
        _hyphens = "\u00AD\u058A\u05BE\u0F0C\u1400\u1806\u2010\u2011\u2012\u2e17\u30A0-"
        _hyphen_newline = regex.compile(
            r"(?<=\p{L})[" + _hyphens + "][ \t\u00a0\r]*\n{1,2}[ \t\u00a0]*(?=\\p{L})"
        )

        page_offsets = []
        text = ""
        page_start_correction = 0
        page_end_correction = 0
        for idx, page in enumerate(self.tree):
            page_start = len(text)
            for textbox in page:
                if textbox.tag == "textbox":
                    for textline in textbox:
                        for text_element in textline:
                            if text_element.text is not None:
                                text += self.control_characters_to_ignore.sub(
                                    "", text_element.text
                                )
                    text += "\n"
                elif textbox.tag == "figure":
                    for text_element in textbox:
                        if (
                            text_element.text is not None
                            and text_element.text != "\n        "
                        ):
                            text += self.control_characters_to_ignore.sub(
                                "", text_element.text
                            )
                elif textbox.tag == "textline":
                    for text_element in textbox:
                        if text_element.text is not None:
                            text += self.control_characters_to_ignore.sub(
                                "", text_element.text
                            )
            page_end = len(text)

            if self.join_hyphenated_words:
                # retrieve all hyphens in text and calculate correction
                text_hyphens = regex.finditer(_hyphen_newline, text)
                page_end_correction = sum(
                    [hyphen.end() - hyphen.start() for hyphen in text_hyphens]
                )
                if logging.DEBUG and page_end_correction > 0:
                    logging.debug(
                        "nifigator.pdfparser.page_offsets: page_start "
                        + str(page_start)
                        + " corrected with "
                        + str(page_start_correction)
                    )
                    logging.debug(
                        "nifigator.pdfparser.page_offsets: page_end   "
                        + str(page_end)
                        + " corrected with "
                        + str(page_end_correction)
                    )
                # append corrected page offsets
                page_offsets.append(
                    self.PDF_offset(
                        idx + 1,
                        page_start - page_start_correction,
                        page_end - page_end_correction,
                    )
                )
                # set page_start_correction for next page
                page_start_correction = page_end_correction
            else:
                # append page offsets
                page_offsets.append(self.PDF_offset(idx, page_start, page_end))

        return page_offsets
