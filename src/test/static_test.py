import unittest

from tools.data_extraction import DateExtractor


class TestDateExtractor(unittest.TestCase) :

    def test_remove_files(self):
        text = """[[File:Zimmermann Telegram as Received by the German Ambassador to Mexico - NARA - 302025.jpg|thumb|The Zimmermann Telegram as it was sent from [[Washington, D.C.|Washington]] to Ambassador [[Heinrich von Eckardt]] (who was the German ambassador to [[Mexico]])]][[File:Zimmermann Telegram.svg|thumb|[[Mexico|Mexican]] territory in 1916 (dark green), territory promised to Mexico in the Zimmermann telegram (light green), the pre-1836 original Mexican territory (red line)]]{{Campaignbox Battles of the Mexican Revolution involving the United States}}The '''Zimmermann Telegram''' (or '''Zimmermann Note''') was an internal diplomatic communication issued from the [[German Foreign Office]] in January 1917 that proposed a military alliance between [[German Empire|Germany]] and [[Mexico]] in the event of the United States' entering [[World War I]] against Germany. """

        cleaned = DateExtractor.remove_files_etc(text)
        cleaned = DateExtractor.remove_files_etc(cleaned, left_sign = '{', right_sign = '}')
        print(cleaned)