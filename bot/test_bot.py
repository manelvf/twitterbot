# -*- coding: UTF-8 -*-
import unittest
import tempfile

from bot import (
    choose_random_file,
    extract_title,
    extract_date,
    compose_tweet
) 


class TestAntigo(unittest.TestCase):

    def test_random_file_is_chosen(self):
        """ checks that a file is retrieved randomly """
        # create 10 random files
        for x in range(10):
                tempfile.TemporaryFile()

        for x in range(10):
                random_files = [
                        choose_random_file(tempfile.tempdir) for f in range(10)]
		
		self.assertTrue(len(set(random_files)) > 1)

    def test_title_is_extracted(self):
        """ Test that the title is extracted """
        html_string = "<b>asdfafd</b><h1><a>Title</a></h1>andereSachen"
        title = extract_title(html_string)
        self.assertEqual(u"Title", title)

    def test_date_is_extracted_from_file(self):
        date_str = "</a> hai 9 días 2 minutos"
        final_date = extract_date(date_str)
        self.assertEqual(final_date, "22-03-2016")

    def test_complete_date_is_extracted_from_file(self):
        date_str = "</a> o 25-06-2015"
        final_date = extract_date(date_str)
        self.assertEqual(final_date, "25-06-2015")

    def test_final_tweet_includes_title_date_url(self):
        compose = compose_tweet("title", "date", "filename")
        self.assertIn("http", compose)

    def test_tweet_no_longer_exceeds_characters(self):
        tweet = compose_tweet("aaaaa" * 120, "d" * 10, url="x" * 23)
        self.assertFalse(len(tweet) > 140)
