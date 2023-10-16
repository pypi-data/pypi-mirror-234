import os
import unittest
from io import BytesIO
from tempfile import TemporaryDirectory

import pytest

from scoamp.utils.helper import SliceFileObj, format_datetime, str_to_int, humanreadable_str_to_int


class TestSliceFileObj(unittest.TestCase):
    def setUp(self) -> None:
        self.content = b"RANDOM self.content uauabciabeubahveb" * 1024

    def test_slice_fileobj_BytesIO(self):
        fileobj = BytesIO(self.content)
        prev_pos = fileobj.tell()

        # Test read
        with SliceFileObj(fileobj, seek_from=24, read_limit=18) as fileobj_slice:
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.read(), self.content[24:42])
            self.assertEqual(fileobj_slice.tell(), 18)
            self.assertEqual(fileobj_slice.read(), b"")
            self.assertEqual(fileobj_slice.tell(), 18)

        self.assertEqual(fileobj.tell(), prev_pos)

        with SliceFileObj(fileobj, seek_from=0, read_limit=990) as fileobj_slice:
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.read(200), self.content[0:200])
            self.assertEqual(fileobj_slice.read(500), self.content[200:700])
            self.assertEqual(fileobj_slice.read(200), self.content[700:900])
            self.assertEqual(fileobj_slice.read(200), self.content[900:990])
            self.assertEqual(fileobj_slice.read(200), b"")

        # Test seek with whence = os.SEEK_SET
        with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
            self.assertEqual(fileobj_slice.tell(), 0)
            fileobj_slice.seek(2, os.SEEK_SET)
            self.assertEqual(fileobj_slice.tell(), 2)
            self.assertEqual(fileobj_slice.fileobj.tell(), 102)
            fileobj_slice.seek(-4, os.SEEK_SET)
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.fileobj.tell(), 100)
            fileobj_slice.seek(100 + 4, os.SEEK_SET)
            self.assertEqual(fileobj_slice.tell(), 100)
            self.assertEqual(fileobj_slice.fileobj.tell(), 200)

        # Test seek with whence = os.SEEK_CUR
        with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
            self.assertEqual(fileobj_slice.tell(), 0)
            fileobj_slice.seek(-5, os.SEEK_CUR)
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.fileobj.tell(), 100)
            fileobj_slice.seek(50, os.SEEK_CUR)
            self.assertEqual(fileobj_slice.tell(), 50)
            self.assertEqual(fileobj_slice.fileobj.tell(), 150)
            fileobj_slice.seek(100, os.SEEK_CUR)
            self.assertEqual(fileobj_slice.tell(), 100)
            self.assertEqual(fileobj_slice.fileobj.tell(), 200)
            fileobj_slice.seek(-300, os.SEEK_CUR)
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.fileobj.tell(), 100)

        # Test seek with whence = os.SEEK_END
        with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
            self.assertEqual(fileobj_slice.tell(), 0)
            fileobj_slice.seek(-5, os.SEEK_END)
            self.assertEqual(fileobj_slice.tell(), 95)
            self.assertEqual(fileobj_slice.fileobj.tell(), 195)
            fileobj_slice.seek(50, os.SEEK_END)
            self.assertEqual(fileobj_slice.tell(), 100)
            self.assertEqual(fileobj_slice.fileobj.tell(), 200)
            fileobj_slice.seek(-200, os.SEEK_END)
            self.assertEqual(fileobj_slice.tell(), 0)
            self.assertEqual(fileobj_slice.fileobj.tell(), 100)

    def test_slice_fileobj_file(self):
        self.content = b"RANDOM self.content uauabciabeubahveb" * 1024

        with TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "file.bin")
            with open(filepath, "wb+") as f:
                f.write(self.content)
            with open(filepath, "rb") as fileobj:
                prev_pos = fileobj.tell()
                # Test read
                with SliceFileObj(fileobj, seek_from=24, read_limit=18) as fileobj_slice:
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.read(), self.content[24:42])
                    self.assertEqual(fileobj_slice.tell(), 18)
                    self.assertEqual(fileobj_slice.read(), b"")
                    self.assertEqual(fileobj_slice.tell(), 18)

                self.assertEqual(fileobj.tell(), prev_pos)

                with SliceFileObj(fileobj, seek_from=0, read_limit=990) as fileobj_slice:
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.read(200), self.content[0:200])
                    self.assertEqual(fileobj_slice.read(500), self.content[200:700])
                    self.assertEqual(fileobj_slice.read(200), self.content[700:900])
                    self.assertEqual(fileobj_slice.read(200), self.content[900:990])
                    self.assertEqual(fileobj_slice.read(200), b"")

                # Test seek with whence = os.SEEK_SET
                with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
                    self.assertEqual(fileobj_slice.tell(), 0)
                    fileobj_slice.seek(2, os.SEEK_SET)
                    self.assertEqual(fileobj_slice.tell(), 2)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 102)
                    fileobj_slice.seek(-4, os.SEEK_SET)
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 100)
                    fileobj_slice.seek(100 + 4, os.SEEK_SET)
                    self.assertEqual(fileobj_slice.tell(), 100)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 200)

                # Test seek with whence = os.SEEK_CUR
                with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
                    self.assertEqual(fileobj_slice.tell(), 0)
                    fileobj_slice.seek(-5, os.SEEK_CUR)
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 100)
                    fileobj_slice.seek(50, os.SEEK_CUR)
                    self.assertEqual(fileobj_slice.tell(), 50)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 150)
                    fileobj_slice.seek(100, os.SEEK_CUR)
                    self.assertEqual(fileobj_slice.tell(), 100)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 200)
                    fileobj_slice.seek(-300, os.SEEK_CUR)
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 100)

                # Test seek with whence = os.SEEK_END
                with SliceFileObj(fileobj, seek_from=100, read_limit=100) as fileobj_slice:
                    self.assertEqual(fileobj_slice.tell(), 0)
                    fileobj_slice.seek(-5, os.SEEK_END)
                    self.assertEqual(fileobj_slice.tell(), 95)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 195)
                    fileobj_slice.seek(50, os.SEEK_END)
                    self.assertEqual(fileobj_slice.tell(), 100)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 200)
                    fileobj_slice.seek(-200, os.SEEK_END)
                    self.assertEqual(fileobj_slice.tell(), 0)
                    self.assertEqual(fileobj_slice.fileobj.tell(), 100)


class TestDatetimeFormatting(unittest.TestCase):
    def test_format_datetime(self):
        time_str = '2023-05-31T12:30:19.962417Z'
        rs = format_datetime(time_str)
        self.assertEqual(rs, '2023-05-31 20:30:19')

        time_str = '2023-05-31T12:30:19.962417+12:00'
        rs = format_datetime(time_str)
        self.assertEqual(rs, '2023-05-31 08:30:19')


class TestStrToInt(unittest.TestCase):
    def test_humanreadable_str_to_int(self):
        test_table = (
            ('12.3k', 12300),
            ('12.3m', 12_300_000),
            ('12.3g', 12_300_000_000),
        )
        for input, output in test_table:
            self.assertEqual(humanreadable_str_to_int(input), output)

        with pytest.raises(
            ValueError,
            match=r"could not convert string to float",
        ):
            humanreadable_str_to_int('abc')

        with pytest.raises(
            ValueError,
            match=r"x not in tuple",
        ):
            humanreadable_str_to_int('12.34')

    def test_str_to_int(self):
        self.assertEqual(str_to_int(None), 0)
        self.assertEqual(str_to_int(''), 0)

        self.assertEqual(str_to_int('1'), 1)
        self.assertEqual(str_to_int('123456'), 123456)
        self.assertEqual(str_to_int('123456.789k'), 123456789)

        with pytest.raises(
            ValueError,
            match=r"x not in tuple",
        ):
            humanreadable_str_to_int('12.34')