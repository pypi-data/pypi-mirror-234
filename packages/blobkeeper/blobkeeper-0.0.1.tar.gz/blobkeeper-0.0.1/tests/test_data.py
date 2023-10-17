import unittest
import tempfile
import os
from blobkeeper import Data


class TestData(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.filepath = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        # Remove the temporary file after testing
        os.remove(self.filepath)

    def test_read_and_write(self):
        # Create a Data object
        data = Data(self.filepath, 0, ro=False)
        # Write data to the file
        data.write(0, b'Hello, ')
        data.write(7, b'world!')
        # Read data from the file
        result1 = data.read(0, 7)
        result2 = data.read(7, 6)
        # Close the file
        data.close()
        # Check if the read data matches what was written
        self.assertEqual(result1, b'Hello, ')
        self.assertEqual(result2, b'world!')

    def test_append(self):
        # Create a Data object
        data = Data(self.filepath, 0, ro=False)
        # Append data to the file
        offset, length = data.append(b'Hello, world!')
        # Read the appended data
        result = data.read(offset, length)
        # Close the file
        data.close()
        # Check if the appended data matches what was expected
        self.assertEqual(result, b'Hello, world!')

    def test_len(self):
        # Create a Data object
        data = Data(self.filepath, 0, ro=False)
        # Append data to the file
        data.append(b'Hello, world!')
        # Check the length of the file
        length = len(data)
        # Close the file
        data.close()
        # Check if the length matches the expected length
        self.assertEqual(length, 13)
