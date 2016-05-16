# -*- coding: utf-8 -*-
import unittest

from graph.date_extractor import DateExtractor


class TestDateExtractor(unittest.TestCase) :
    @staticmethod
    def get_date_extractor(content) :
        return DateExtractor("Uprising of 1799", content)

    @staticmethod
    def get_base_date_extractor() :
        return DateExtractor("Uprising of 1799", '')

    def test_extract_from_template(self) :
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_date_from_template('start date', '{{start date|2013|11|24|df=y}}')
        date = date_extractor.date
        self.assertEqual(u"2013", date.year)
        self.assertEqual(u"11", date.month)
        self.assertEqual(u"24", date.day)

    def test_extract_from_title(self) :
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_title(date_extractor.title)
        date = date_extractor.date
        self.assertEqual(u"1799", date.year)

    @unittest.skip("Skipping")
    def test_extract_from_title2(self) :
        self.fail("Fail")
        pass

    def test_extract_from_infobox(self) :
        infobox = "{{Infobox military conflict\n|conflict=Tyrolean Rebellion\n|partof=the [[War of the Fifth " \
                  "Coalition]]\n|image=[[File:Franz von Defregger Heimkehrender Tiroler " \
                  "Landsturm.jpg|300px]]\n|caption=''Homecoming of Tyrolean Militia in the War of 1809'' by  [[Franz " \
                  "Defregger]]\n|date=April\u2013November 1809\n|place=[[County of Tyrol|Tyrol]]\n|result=French " \
                  "victory<br />Rebellion crushed\n|combatant1={{flagicon|France}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date
        self.assertEqual(u"1809", start_date.year)
        self.assertEqual(u"04", start_date.month)  # April
        self.assertEqual(u"1809", end_date.year)
        self.assertEqual(u"11", end_date.month)  # November

    def test_extract_from_infobox_year(self) :
        infobox = "{{Infobox military conflict\n|conflict=Tyrolean Rebellion\n|partof=the [[War of the Fifth " \
                  "Coalition]]\n|image=[[File:Franz von Defregger Heimkehrender Tiroler " \
                  "Landsturm.jpg|300px]]\n|caption=''Homecoming of Tyrolean Militia in the War of 1809'' by  [[Franz " \
                  "Defregger]]\n|date=18 April\n|year=1809|place=[[County of " \
                  "Tyrol|Tyrol]]\n|result=French victory<br />Rebellion crushed\n|combatant1={{flagicon|France}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        date = date_extractor.date
        self.assertEqual(u"1809", date.year)
        self.assertEqual(u"04", date.month)  # April
        pass

    def test_extract_from_infobox_year_both_dates(self) :
        infobox = "{{Infobox military conflict\n|conflict=Tyrolean Rebellion\n|partof=the [[War of the Fifth " \
                  "Coalition]]\n|image=[[File:Franz von Defregger Heimkehrender Tiroler " \
                  "Landsturm.jpg|300px]]\n|caption=''Homecoming of Tyrolean Militia in the War of 1809'' by  [[" \
                  "Franz " \
                  "Defregger]]\n|date=April\u2013November\n|year=1809\n|place=[[County of " \
                  "Tyrol|Tyrol]]\n|result=French victory<br />Rebellion crushed\n|combatant1={{flagicon|France}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date
        self.assertEqual(u"1809", start_date.year)
        self.assertEqual(u"04", start_date.month)  # April
        self.assertEqual(u"1809", end_date.year)
        self.assertEqual(u"11", end_date.month)  # November
        pass

    def test_extract_from_content(self) :
        date_extractor = self.get_base_date_extractor()

    # Test helper methods

    def test_split_date_day(self) :
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('September 18-19, 2013')
        self.assertEqual("September 18 2013", from_date)
        self.assertEqual("September 19, 2013", till_date)

    def test_split_date_months(self) :
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('September 18-October 19, 2013')
        self.assertEqual("September 18 2013", from_date)
        self.assertEqual("October 19, 2013", till_date)

    def test_split_date_years_only(self) :
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('2011-2013')
        self.assertEqual("2011", from_date)
        self.assertEqual("2013", till_date)

    def test_split_date_unicode_dash(self) :
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('2011\\u20132013')
        self.assertEqual("2011", from_date)
        self.assertEqual("2013", till_date)

    def test_split_date_with_spaces(self) :
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str("22 July - 25 September 1800")
        self.assertEqual("22 July 1800", from_date)
        self.assertEqual("25 September 1800", till_date)

    def test_fill_years(self) :
        from_datestr, till_datestr = DateExtractor.fill_years('18 September', '19 September 1999')
        self.assertEqual('18 September 1999', from_datestr)
        self.assertEqual('19 September 1999', till_datestr)

    def test_fill_months(self) :
        pass

    def test_BC_dates(self) :
        pass

    def test_etract_infobox_parameter(self) :
        pass

    def test_extract_infobox_year(self) :
        year = DateExtractor.extract_infobox_year("|ma=ma||year=1809|alamakota=ma|")
        self.assertEqual("1809", year)

    def test_infobox(self) :
        content = u"""{{Infobox military conflict\n|date=22 July - 25 September 1800\n|conflict=Invasion of
        Cura\xe7ao\n|partof=[[French Revolutionary Wars]] and the [[Quasi-War]]\n|image=\n|caption=\n|place=[[
        Cura\xe7ao]], territory of Batavian Republic\n|result=Anglo-American victory\n* Withdrawal of French
        forces\n* British occupation of Cura\xe7ao \n|combatant1={{flag|Batavian Republic}}<br/>{{flag|United
        States|1795}}<br/>{{flagcountry|Kingdom of Great Britain}}\n|combatant2={{flagcountry|French First
        Republic}}\n*{{flagicon|French First Republic}} [[Guadeloupe]]\n|commander1={{flag icon|Batavian Republic}}
        Johan Lausser<br/>{{flag icon|Kingdom of Great Britain}} Frederick Watkins<br>{{flagicon|United States|1795}}
        Moses Brown<br>{{flagicon|United States|1795}} Henry Geddes\n|commander2={{flagicon|French First Republic}}
        Unknown\n|strength1={{flagicon|United States|1795}} '''American:'''<br>2 [[ship-sloop]]s<br>[[U.S.
        Navy]]<br>[[U.S. Marines]]<br>1 [[Artillery battery|gun battery]]<br>{{flagicon|Kingdom of Great Britain}}
        '''British:'''<br>1 [[frigate]]<br>[[Royal Navy]]<br>[[Royal Marines]]\n|strength2=2 [[brig-sloop]]s<br>3 [[
        schooner]]s<br>10 additional vessels<br>At least 1,400 troops, sailors and
        militia\n|casualties1='''American:'''<br>2 wounded<br>'''British:'''<br>None\n|casualties2=150 killed or
        wounded<ref name="Commandant">{{cite web |title=Wars of the Early American
        Republic|url=https://books.google.com/books?id=sApvBAAAQBAJ&pg=PA419&lpg=PA419&dq=Invasion+of+Curacao+(
        1800)+casualties&source=bl&ots=ablLLa_X7d&sig=TA3LizqS_EXbqKB5PAMMmNY7N-g&hl=en&sa=X&ved
        =0CCkQ6AEwAmoVChMIguGo3IityAIVQ5ENCh0CbQBO#v=onepage&q=Invasion%20of%20Curacao%20(
        1800)%20casualties&f=false}}</ref>\n|campaignbox={{Campaignbox Quasi-War}}\n}}"""

        date_extractor = DateExtractor("Test", content)
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"22", start_date.day)
        self.assertEqual(u"07", start_date.month)
        self.assertEqual(u"1800", start_date.year)
        self.assertEqual(u"25", end_date.day)
        self.assertEqual(u"09", end_date.month)
        self.assertEqual(u"1800", end_date.year)

    def test_infofobox2(self) :
        content = """{{Infobox military conflict\n|conflict=Battle of Mindoro\n|image=\n|caption=\n|partof=the [[
        Pacific War|Pacific Theater]] of [[World War II]]\n|date=December 13\u201316, 1944\n|place=[[Mindoro|Mindoro
        Island]], Philippines\n|result=American and Filipino Commonwealth victory\n|combatant1={{flag|United
        States|1912}}\n*{{flag|Commonwealth of the Philippines}}\n|combatant2={{flagicon|Empire of Japan}} [[Empire
        of Japan]]\n*{{flag|Second Philippine Republic}}\n|commander1={{flagicon|United States|1912}} [[George M.
        Jones]]<br/>{{flagicon|United States|1912}} [[Roscoe B. Woodruff]] \n|commander2={{flagicon|Empire of Japan}}
        [[Rikichi Tsukada]]\n|strength1=10,000 American troops \n|strength2=1,200 Japanese troops \n|casualties1=18
        killed and 81 wounded\n|casualties2=~200 dead<br>15 captured<br>375 wounded\n}}"""

        date_extractor = DateExtractor("Test", content)
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"13", start_date.day)
        self.assertEqual(u"12", start_date.month)
        self.assertEqual(u"1944", start_date.year)
        self.assertEqual(u"16", end_date.day)
        self.assertEqual(u"12", end_date.month)
        self.assertEqual(u"1944", end_date.year)

    def test_extract_from_content_month_only(self):
        content = u"""The '''Edict of Boulogne''', also called the '''Edict of Pacification of Boulogne''' and the
        '''Peace of La Rochelle''', was signed in July, 1573 <ref>Jouanna, p. 213. The Catholic Encyclopedia gives 25 June 1573 as the date of signing.</ref> by King [[Charles IX of France]] in the [[Ch\xe2teau de Madrid]] in the [[Bois de Boulogne]]. """
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_content(content)
        self.assertEqual(u"1573", date_extractor.date.year)
        self.assertEqual(u"07", date_extractor.date.month)

    def test_extract_from_content_year_only(self):
        content = u"""The First Congress of Vienna was held in 1515, attended by the Holy Roman Emperor, Maximilian
        I, and the Jagiellonian brothers, Vladislaus II, King of Hungary and King of Bohemia, and Sigismund I, King of Poland and Grand Duke of Lithuania. Vladislaus II made a Habsburg-Jagiellon mutual succession treaty with Emperor Maximilian in 1506.[1] It became a turning point in the history of central Europe. After the death of the childless king Louis II at the Battle of Mohács against the Ottomans in 1526, the Habsburg-Jagellion mutual succession treaty ultimately increasing the power of the Habsburgs and diminishing that of the Jagiellonians."""
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_content(content)
        self.assertEqual(u"1515", date_extractor.date.year)

    def test_extract_from_infobox_two_dates_BC(self):
        content = "{{Infobox military conflict|conflict=Siege of Massilia|partof=the [[Caesar's Civil War]]|image=Siege of Massilia 49 BC.jpg|caption=Map of the siege|date=April 19-September 6, 49 BC|place=Massilia and Western [[Mediterranean Sea]]|result=Caesarian Victory, Roman annexation of Massilia|combatant1=Massilia and [[Optimates]]|combatant2=[[Populares]]|commander1=[[Lucius Domitius Ahenobarbus (consul 54 BC)|Lucius Domitius Ahenobarbus]]|commander2=[[Julius Caesar|Gaius Julius Caesar]]<br>[[Decimus Junius Brutus Albinus]]<br>[[Gaius Trebonius]]|strength1=8,000|strength2= 15,000 - 3 Roman legions (XVII, XVIII, and XIX)|casualties1=4,000|casualties2=1,100|}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"19", start_date.day)
        self.assertEqual(u"04", start_date.month)
        self.assertEqual(u"-2049", start_date.year)
        self.assertEqual(u"06", end_date.day)
        self.assertEqual(u"09", end_date.month)
        self.assertEqual(u"-2049", end_date.year)

    def test_extract_from_infobox_two_dates_not_four_digit_year(self):
        content = "{{Infobox military conflict|conflict=Siege of Massilia|partof=the [[Caesar's Civil War]]|image=Siege of Massilia 49 BC.jpg|caption=Map of the siege|date=April 19-September 6, 49|place=Massilia and Western [[Mediterranean Sea]]|result=Caesarian Victory, Roman annexation of Massilia|combatant1=Massilia and [[Optimates]]|combatant2=[[Populares]]|commander1=[[Lucius Domitius Ahenobarbus (consul 54 BC)|Lucius Domitius Ahenobarbus]]|commander2=[[Julius Caesar|Gaius Julius Caesar]]<br>[[Decimus Junius Brutus Albinus]]<br>[[Gaius Trebonius]]|strength1=8,000|strength2= 15,000 - 3 Roman legions (XVII, XVIII, and XIX)|casualties1=4,000|casualties2=1,100|}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"19", start_date.day)
        self.assertEqual(u"04", start_date.month)
        self.assertEqual(u"0049", start_date.year)
        self.assertEqual(u"06", end_date.day)
        self.assertEqual(u"09", end_date.month)
        self.assertEqual(u"0049", end_date.year)

    def test(self):
        content = "{{Infobox Treaty\n|name=Barbados-France Maritime Delimitation Agreement\n|long_name=Agreement between the Government of the French Republic and the Government of Barbados on the delimitation of maritime areas between France and Barbados\n|image=\n|image_width=\n|caption=\n|type=[[boundary delimitation]]\n|date_drafted=\n|date_signed=15 October 2009\n|location_signed=[[Bridgetown]], [[Barbados]]\n|date_sealed=\n|date_effective=15 January 2010\n|condition_effective=\n|date_expiration=\n|signatories=\n|parties={{flag|Barbados}}<br>{{flag|France}}\n|ratifiers=\n|depositor={{flagicon|United Nations}} [[United Nations Secretariat]]\n|language=English; French\n|languages=\n|wikisource=\n}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(content)
        date = date_extractor.date
        self.assertEqual(u"15", date.day)
        self.assertEqual(u"10", date.month)
        self.assertEqual(u"2009", date.year)

    def test_century_to_year(self):
        content = u"{{Infobox military conflict\n|conflict=\n|width=\n|partof=\n|image=\n|caption=\n|date=5th-century" \
                  u"-562\n|place=[[Greater Khorasan|Khorasan]] and [[Transoxiana]]\n|coordinates=\n|map_type=\n|map_relief=\n|latitude=\n|longitude=\n|map_size=\n|map_marksize=\n|map_caption=\n|map_label=\n|territory=\n|result=Sasanian victory\n*The Hephthalite state breaks into several minor kingdoms\n|status=\n|combatants_header=\n|combatant1=[[Sasanian Empire]]<br>[[Western Turkic Khaganate]]<small> (557-562) </small>\n|combatant2=[[Hephthalite Empire]]\n|commander1=[[Peroz I]] {{KIA}}<br>[[Mihran (general)|Mihran]] {{KIA}}<br>[[Sukhra]]<br>[[Kavadh I]]<br>[[Khosrow I]]<br>[[Ist\xe4mi]]\n|commander2=[[Khushnavaz]]<br>Ghaftar\n|units1=\n|units2=\n|notes=\n|campaignbox={{Campaignbox Hephthalite-Persian Wars}}\n}}"
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"0500", start_date.year)
        self.assertEqual(u"0562", end_date.year)

def test_3(self) :
    content = u"{{Infobox military conflict\n|conflict=\n|width=\n|partof=\n|image=\n|caption=\n|date=April" \
              u"-September 562\n|place=[[Greater Khorasan|Khorasan]] and [[" \
              u"Transoxiana]]\n|coordinates=\n|map_type=\n|map_relief=\n|latitude=\n|longitude=\n|map_size=\n" \
              u"|map_marksize=\n|map_caption=\n|map_label=\n|territory=\n|result=Sasanian victory\n*The Hephthalite " \
              u"state breaks into several minor kingdoms\n|status=\n|combatants_header=\n|combatant1=[[Sasanian " \
              u"Empire]]<br>[[Western Turkic Khaganate]]<small> (557-562) </small>\n|combatant2=[[Hephthalite " \
              u"Empire]]\n|commander1=[[Peroz I]] {{KIA}}<br>[[Mihran (general)|Mihran]] {{KIA}}<br>[[Sukhra]]<br>[[" \
              u"Kavadh I]]<br>[[Khosrow I]]<br>[[Ist\xe4mi]]\n|commander2=[[" \
              u"Khushnavaz]]<br>Ghaftar\n|units1=\n|units2=\n|notes=\n|campaignbox={{Campaignbox Hephthalite-Persian " \
              u"Wars}}\n}}"
    date_extractor = self.get_base_date_extractor()
    date_extractor.extract_from_infobox(content)
    start_date = date_extractor.start_date
    end_date = date_extractor.end_date
    self.assertEqual(u"04", start_date.month)
    self.assertEqual(u"0562", start_date.year)
    self.assertEqual(u"09", end_date.month)
    self.assertEqual(u"0562", end_date.year)

    def test_4(self):
        content = "{{Infobox SCC |case-name=R v Eastern Terminal Elevator Co |full-case-name=The King v. Eastern Terminal Elevator Co. |heard-date=9{{endash}}10 March 1925 |decided-date=5 May 1925 |citations=1925 CanLII 82 (SCC) , [1925] SCR 434 |docket=|history=APPEAL from the judgment of the [[Exchequer Court of Canada]], [1924] ExCR 167 |subsequent=|ruling=Judgment of the Exchequer Court affirmed. |ratio=It is not within the power of Parliament to regulate in the provinces particular occupations by a licensing system and otherwise, and of local works and undertakings, as such, however important and beneficial the ultimate purpose of the legislation may be. |chief-justice=[[Francis Alexander Anglin|Anglin CJC]] |puisne-justices=[[John Idington|Idington]], [[Lyman Poore Duff|Duff]], [[Pierre-Basile Mignault|Mignault]] and [[Thibaudeau Rinfret|Rinfret]] JJ |Unanimous=|Majority=[[Lyman Poore Duff|Duff J]] |JoinMajority=[[Thibaudeau Rinfret|Rinfret J]] |Majority2=[[Pierre-Basile Mignault|Mignault J]] |JoinMajority2=|Majority3=[[John Idington|Idington J]] |Concurrence=|JoinConcurrence=|Concurrence/Dissent=|JoinConcurrence/Dissent=|Dissent=[[Francis Alexander Anglin|Anglin CJC]] |JoinDissent=|NotParticipating=|LawsApplied=}}"

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(content)
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"04", start_date.month)
        self.assertEqual(u"0562", start_date.year)
        self.assertEqual(u"09", end_date.month)
        self.assertEqual(u"0562", end_date.year)