import unittest
from logs import *


class FakeFileReader:
    def __init__(self, echo_text):
        self._echo_text = echo_text

    def read_file(self, filename):
        return self._echo_text


class LogReaderTests(unittest.TestCase):
    def test_read_log_runs(self):
        reader = LogReader(file_reader=FakeFileReader("test"))

        reader.read_log("")

    def test_read_log_returns_list(self):
        reader = LogReader(file_reader=FakeFileReader("test"))

        actual = reader.read_log("")

        self.assertIsInstance(actual, list)

    def test_read_log_returns_one(self):
        reader = LogReader(file_reader=FakeFileReader("test"))
        expected = 1

        actual = len(reader.read_log(""))

        self.assertEqual(expected, actual)

    def test_read_log_returns_three(self):
        reader = LogReader(file_reader=FakeFileReader("test\ntest\ntest"))
        expected = 3

        actual = len(reader.read_log(""))

        self.assertEqual(expected, actual)

    def test_read_log_correct_entry(self):
        reader = LogReader(file_reader=FakeFileReader("test"))

        actual = reader.read_log("")[0].entry()

        self.assertEqual(actual, "test")

    def test_read_log_correct_entries(self):
        reader = LogReader(file_reader=FakeFileReader("one\ntwo\nthree"))
        expected = "three"

        actual = reader.read_log("")[2].entry()

        self.assertEqual(expected, actual)


class LogItemTests(unittest.TestCase):
    def setUp(self):
        self.test_log_string = '111.1.1.1 [01/Jan/2017:00:00:00] ' \
                               '"TEST /TEST.test HTTP/1.1" 200 0 "http://test.com/tester" '

    def test_object_builds(self):
        LogItem("")

    def test_contains_log_entry(self):
        log_item = LogItem("")
        expected = ""

        actual = log_item.entry()

        self.assertEqual(expected, actual)

    def test_contains_ip(self):
        log_item = LogItem(self.test_log_string)
        expected = "111.1.1.1"

        actual = log_item.ip()

        self.assertEqual(expected, actual)

    def test_contains_date(self):
        log_item = LogItem(self.test_log_string)
        expected = "01/Jan/2017"

        actual = log_item.date()

        self.assertEqual(expected, actual)

    def test_contains_time(self):
        log_item = LogItem(self.test_log_string)
        expected = "00:00:00"

        actual = log_item.time()

        self.assertEqual(expected, actual)

    def test_contains_file(self):
        log_item = LogItem(self.test_log_string)
        expected = "TEST.test"

        actual = log_item.file()

        self.assertEqual(expected, actual)

    def test_contains_referer(self):
        log_item = LogItem(self.test_log_string)
        expected = "http://test.com/tester"

        actual = log_item.referrer()

        self.assertEqual(expected, actual)


class FakeLogReader:
    def read_log(self, filename):
        self.item1 = LogItem('111.1.1.1 [01/Jan/2017:01:00:00] "TEST /TEST1.test HTTP/1.1" 200 0 "http://test1.com" ')
        self.item2 = LogItem('222.2.2.2 [02/Jan/2017:02:00:00] "TEST /TEST2.test HTTP/1.1" 200 0 "http://test2.com" ')
        self.item3 = LogItem('333.3.3.3 [03/Jan/2017:03:00:00] "TEST /TEST3.test HTTP/1.1" 200 0 "http://test3.com" ')

        return [self.item1, self.item2, self.item3]


class LogSearchTests(unittest.TestCase):
    def test_object_builds(self):
        LogSearch()

    def test_execute_runs(self):
        search = LogSearch()

        search.execute()

    def test_execute_before_query_returns_empty(self):
        search = LogSearch()
        expected = []

        actual = search.execute()

        self.assertEqual(expected, actual)

    def test_inclusive_returns_original_object(self):
        search = LogSearch()
        expected = search

        actual = search.inclusive()

        self.assertIs(expected, actual)

    def test_exclusive_returns_original_object(self):
        search = LogSearch()
        expected = search

        actual = search.exclusive()

        self.assertIs(expected, actual)

    def test_ip_returns_correct_entry(self):
        search = LogSearch()
        expected = "111.1.1.1"

        actual = search.ip("111.1.1.1").execute()

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
