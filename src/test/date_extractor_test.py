# -*- coding: utf-8 -*-
import unittest

from graph.dataextraction.date_extractor import DateExtractor


class TestDateExtractor(unittest.TestCase):
    @staticmethod
    def get_date_extractor(content):
        return DateExtractor("Uprising of 1799", content)

    @staticmethod
    def get_base_date_extractor():
        return DateExtractor("Uprising of 1799", '')

    def test_extract_from_template(self):
        date_extractor = self.get_base_date_extractor()
        date = date_extractor.extract_date_from_template('start date', '{{start date|2013|11|24|df=y}}')
        self.assertEqual(u"2013", date.year)
        self.assertEqual(u"11", date.month)
        self.assertEqual(u"24", date.day)

    def test_extract_from_title(self):
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_title(date_extractor.title)
        date = date_extractor.date
        self.assertEqual(u"1799", date.year)

    @unittest.skip("Skipping")
    def test_extract_from_title2(self):
        self.fail("Fail")
        pass

    def test_extract_from_infobox(self):
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

    def test_extract_from_infobox_year(self):
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

    def test_extract_from_infobox_year_both_dates(self):
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

    def test_extract_from_infobox_birth_and_death_not_formatted(self):
        infobox = "{{Infobox pirate|name=Hasan Pasha |birth_date=c. 1517|death_date=4 July " \
                  "1572|image=|caption=|nickname=|type=[[Turkish people|Turkish]] [[Admiral]]|birth_place=[[" \
                  "Algiers]]|death_place=[[Istanbul]], [[Ottoman Empire]]|allegiance=[[Ottoman " \
                  "Empire]]|serviceyears=c. 1545-1572|base of " \
                  "operations=Mediterranean|rank=Admiral|commands=|battles=|wealth=|laterwork=}} "
        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        birth_date, death_date = date_extractor.start_date, date_extractor.end_date
        self.assertEqual(u"Note 'circa' : c. 1517", birth_date.qualifier)
        self.assertEqual("04", death_date.day)
        self.assertEqual("07", death_date.month)
        self.assertEqual("1572", death_date.year)

    def test_extract_from_content(self):
        # TODO
        pass

    # Test helper methods

    def test_split_date_day(self):
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('September 18-19, 2013')
        self.assertEqual("September 18 2013", from_date)
        self.assertEqual("September 19, 2013", till_date)

    def test_split_date_months(self):
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('September 18-October 19, 2013')
        self.assertEqual("September 18 2013", from_date)
        self.assertEqual("October 19, 2013", till_date)

    def test_split_date_years_only(self):
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('2011-2013')
        self.assertEqual("2011", from_date)
        self.assertEqual("2013", till_date)

    def test_split_date_unicode_dash(self):
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str('2011\\u20132013')
        self.assertEqual("2011", from_date)
        self.assertEqual("2013", till_date)

    def test_split_date_with_spaces(self):
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str("22 July - 25 September 1800")
        self.assertEqual("22 July 1800", from_date)
        self.assertEqual("25 September 1800", till_date)

    def test_split_two_dates_with_multiple_dashes(self):
        content = """10--28 May 1941"""
        date_extractor = self.get_base_date_extractor()
        start_date, end_date = date_extractor.get_two_dates_from_one_str(content)
        self.assertEqual("May 10 1941", start_date)
        self.assertEqual("28 May 1941", end_date)

    def test_fill_years(self):
        from_datestr, till_datestr = DateExtractor.fill_years('18 September', '19 September 1999')
        self.assertEqual('18 September 1999', from_datestr)
        self.assertEqual('19 September 1999', till_datestr)

    def test_fill_months(self):
        pass

    def test_BC_dates(self):
        pass

    def test_etract_infobox_parameter(self):
        pass

    def test_extract_infobox_year(self):
        year = DateExtractor.extract_infobox_year("|ma=ma||year=1809|alamakota=ma|")
        self.assertEqual("1809", year)

    def test_infobox(self):
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

    def test_infofobox2(self):
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
        self.assertEqual(u"-0049", start_date.year)
        self.assertEqual(u"06", end_date.day)
        self.assertEqual(u"09", end_date.month)
        self.assertEqual(u"-0049", end_date.year)

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

    def test_3(self):
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

    def test_two_dates_trom_one_str_days_unicode_char(self):
        datestr = '21–25 May 1982'
        date_extractor = self.get_base_date_extractor()
        from_date, till_date = date_extractor.get_two_dates_from_one_str(datestr)

        self.assertEqual(u'May 21 1982', from_date)
        self.assertEqual(u'25 May 1982', till_date)

    def test_infobox_birth_date(self):
        infobox = '{{Infobox military person|name=Sir Christopher Lloyd Courtney|image=The Independent Air Force ' \
                  'Dinner - Prince Albert, Trenchard and Courtney.jpg|image_size=300px|caption=Courtney (shown on ' \
                  'right) with Trenchard and [[King George VI|Prince Albert]] in 1919|nickname=|birth_date={{Birth ' \
                  'date|1890|06|27|df=yes}}|death_date={{Death date and ' \
                  'age|1976|10|22|1890|06|27|df=yes}}|birth_place=|death_place=|placeofburial=|allegiance={{' \
                  'flag|United Kingdom}}|branch={{navy|United Kingdom}} (1905-18)<br/>{{air force|United Kingdom}} (' \
                  '1918-45)|serviceyears=1905-1945|rank=[[Air Chief Marshal]]|servicenumber=|unit=|commands=[[Air ' \
                  'Member for Supply and Organisation]] (1940-45)<br/>[[RAF Home Command|Reserve Command]] (' \
                  '1939)<br/>[[RAF Iraq Command|British Forces in Iraq]] (1937-39)<br/>[[Deputy Chief of the Air ' \
                  'Staff]] (1935-37)<br/>No. 2 (Indian) Wing (1920-24)<br/>[[Independent Air Force]] (1918)<br/>11th ' \
                  'Brigade (1918)<br/>[[No. 207 Squadron RAF|No. 7 Squadron RNAS]] (1916-17)<br/>[[No. 4 Wing RNAS]] ' \
                  '(1916)<br/>RNAS Dover (1915-16)<br/>[[No. 4 Squadron RNAS]] (1915)<br/>[[RAF North ' \
                  'Killingholme|Killingholme Naval Air Station]] (1914-15)|battles=[[First World War]]<br/>[[Second ' \
                  'World War]]|awards=[[Knight Grand Cross of the Order of the British Empire]]<br/>[[Knight ' \
                  'Commander of the Order of the Bath]]<br/>[[Distinguished Service Order]]<br/>[[Mentioned in ' \
                  'Despatches]]<br/>[[Order of St. Anna|Order of St. Anna, 3rd Class]] (Russia)<br/>[[Legion of ' \
                  'Honour|Chevalier of the Legion of Honour]] (France)<br/>[[Legion of Merit|Commander of the Legion ' \
                  'of Merit]] (United States)|relations=|laterwork=Businessman}} '

        date_extractor = self.get_base_date_extractor()
        date_extractor.content = infobox
        date_extractor.fill_dates()
        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"27", start_date.day)
        self.assertEqual(u"06", start_date.month)
        self.assertEqual(u"1890", start_date.year)
        self.assertEqual(u"22", end_date.day)
        self.assertEqual(u"10", end_date.month)
        self.assertEqual(u"1976", end_date.year)

    def test_ignore_keyword_late(self):
        infobox = '{{Infobox military conflict|conflict=Operation Neuland|partof=the [[Battle of the Atlantic]] of [[World War II]]|image=File:CaribbeanIslands.png|caption=Map of the Caribbean Sea|date=16 February - late March 1942|place=[[Caribbean Sea]]|result=Axis [[tactical victory]]|combatant1={{flag|Nazi Germany|name=Germany}}<br/>{{flagicon|Italy|1861|30px}} [[Kingdom of Italy (1861-1946)|Kingdom of Italy]]|combatant2={{flag|United States|1912}}<br/>{{flag|United Kingdom}}<br>{{flag|Netherlands}}|commander1=[[File:War Ensign of Germany 1938-1945.svg|25px|border]] [[Karl Dönitz]]|commander2=[[File:US Naval Jack 48 stars.svg|23px]] [[John H. Hoover]]|strength1=11 submarines|strength2={{USS|Barney|DD-149|6}}<br/>{{USS|Blakeley|DD-150|6}}<br/>{{USS|Lapwing|AM-1|6}} with<br/>VP-12 (12 × [[PBY]])<br/>2 × [[Eagle class patrol craft]]<ref>Morison p.145</ref>|casualties1=1 killed<br>1 wounded<br>1 submarine damaged|casualties2=45 cargo ships sunk<br/>1 lighthouse tender sunk<br/>10 cargo ships damaged|notes=<br/>*''German casualties were caused by an accident.''|campaignbox={{Campaignbox Atlantic Campaign}}}}'

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)

        start_date = date_extractor.start_date
        end_date = date_extractor.end_date
        self.assertEqual(u"16", start_date.day)
        self.assertEqual(u"02", start_date.month)
        self.assertEqual(u"1942", start_date.year)
        self.assertEqual(u"03", end_date.month)
        self.assertEqual(u"1942", end_date.year)

    def test_handle_uncertainity(self):
        infobox = ' {{Infobox military conflict|conflict=Battle of Amorgos|partof=the [[Lamian War]]|date=May or June 322 BC|place=[[Amorgos]], [[Cyclades]], Greece|result=Macedonian victory|combatant1=[[Classical Athens|Athens]]|commander1=[[Euetion]]|combatant2=[[Ancient Macedonia|Macedonia]]|commander2=[[Cleitus the White]]|strength1=170 warships|strength2=240 warships|casualties1=|casualties2=}}'

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        date = date_extractor.date
        self.assertEqual(u"-0322", date.year)

    def test_parse_2_dates_in_infobox(self):
        infobox = '''{{Infobox Military Conflict|conflict=Battle of Palo Hincado|partof=the [[Spanish reconquest of Santo Domingo]]<br> and the [[Napoleonic Wars]]|image=[[Image:Palo Hincado monument.gif|300px]]|caption=The Battle of Palo Hincado Monument,<br/>in the [[Dominican Republic]].|date=7 November 1808|place=Palo Hincado savanna, near [[El Seibo]], Spanish colonial [[Captaincy General of Santo Domingo]].|result=Decisive Spanish victory|combatant1=[[File:Flag of New Spain.svg|23px]] [[Captaincy General of Santo Domingo]]|combatant2={{flagicon|France}} [[First French Empire|French Empire]]|commander1=[[File:Flag of New Spain.svg|23px]] Gen. [[Juan Sánchez Ramírez]]|commander2={{flagicon|France}} Gen. Marie-Louis Ferrand †|strength1=1700 regulars and militia <br/> 300 [[Captaincy General of Puerto Rico|Puerto Rican]] [[tercios]]|strength2=600 regulars|casualties1=7|casualties2=560<ref>{{cite book|title=L'art de verifier les dates|date=1837}}</ref>|campaignbox={{Campaignbox Reconquista (Santo Domingo)}}{{Campaignbox Napoleonic Wars: West Indies}}}}'''

        date_extractor = self.get_base_date_extractor()
        date_extractor.content = infobox
        date_extractor.fill_dates()
        date = date_extractor.date
        self.assertEqual(u"07", date.day)
        self.assertEqual(u"11", date.month)
        self.assertEqual(u"1808", date.year)

    @unittest.skip("Skipping")
    def test_infobox_slash(self):
        infobox = '''{{Infobox military conflict|conflict=Second Arab Siege of Constantinople|image=[[File:Constantinople area map.svg|280px|alt=Geophysical map of the Marmara Sea and its shores, with main settlements of medieval times]]|caption=Map of the environs of Constantinople in Byzantine times|partof=the [[Arab-Byzantine wars]]|date=15 July/August{{cref|a}} 717&nbsp;- 15 August 718|place=[[Thrace]], [[Bithynia]] and [[Sea of Marmara]]|result=Decisive [[Byzantine Empire|Byzantine]]-[[First Bulgarian Empire|Bulgar]] victory<br>Climax of the [[Arab-Byzantine wars]]|combatant1=[[File:Umayyad Flag.svg|24px|border]] [[Umayyad Caliphate]]|combatant2=[[File:Simple Labarum2.svg|15px]] [[Byzantine Empire]]<br>[[First Bulgarian Empire|Bulgar Khanate]]|commander1=[[Maslama ibn Abd al-Malik]]<br>Sulayman ibn Mu'ad<br>[[Umar ibn Hubayra]]|commander2=[[File:Simple Labarum2.svg|15px]] [[Leo III the Isaurian|Leo III]]<br>[[Tervel of Bulgaria|Tervel]]|strength1=120,000 men<ref name="Treadgold346">{{harvnb|Treadgold|1997|p=346}}.</ref><br>2,560 ships<ref>{{harvnb|Treadgold|1997|pp=346-347}}.</ref>|strength2=unknown|casualties1=|casualties2=|campaignbox={{Campaignbox Arab-Byzantine Wars}}}}'''

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)

        start_date, end_date  = date_extractor.start_date, date_extractor.end_date
        # TODO
        self.assertEqual(u"15", start_date.day)
        self.assertEqual(u"07", start_date.month)
        self.assertEqual(u"717", start_date.year)
        self.assertEqual(u"15", end_date.day)
        self.assertEqual(u"08", end_date.month)
        self.assertEqual(u"718", end_date.year)

    def test_date_signed(self):
        # given
        infobox = """{{Infobox treaty|name=Council of Europe Convention on the Protection of Children against Sexual Exploitation and Sexual Abuse|long_name=|image=|image_width=|caption=|type=|date_drafted=|date_signed=25 October 2007|location_signed=[[Lanzarote]], [[Canary Islands]], [[Spain]]|date_sealed=|date_effective=1 July 2010|condition_effective=five ratifications, three of which are by Council of Europe states|date_expiration=|signatories=47|parties=41|depositor=Secretary General of the [[Council of Europe]]|language=|languages=English and French|website=|wikisource=}}"""
        date_extractor = self.get_base_date_extractor()

        # when
        date_extractor.extract_from_infobox(infobox)

        # then
        date = date_extractor.date
        self.assertEqual(u"25", date.day)
        self.assertEqual(u"10", date.month)
        self.assertEqual(u"2007", date.year)

    def test_parse_from_content_date_period(self):
        content = "Brigadier-General Alfred Cecil Critchley, CMG, CBE, DSO (23 February 1890 – 9 February 1963) was " \
                  "an entrepreneur and politician in the United Kingdom."
        date_extractor = self.get_base_date_extractor()

        date_extractor.extract_from_content(content)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date

        self.assertEqual(u"23", start_date.day)
        self.assertEqual(u"02", start_date.month)
        self.assertEqual(u"1890", start_date.year)
        self.assertEqual(u"09", end_date.day)
        self.assertEqual(u"02", end_date.month)
        self.assertEqual(u"1963", end_date.year)

    def test_parse_from_content_date_period_additional_info(self):
        content = """Roger Barlet (nom de guerre Rożek; 12 April 1914, Metz - 29 or 30 August 1944, Warsaw) was a
        French soldier. Born in Metz, after the Battle of France he was conscripted to the German Wehrmacht and dispatched to the East Front. """

        # TODO

        """Claude François Bidal, marquis d'Asfeld (Paris, July 2, 1665 – Paris, March 7, 1743), was a French Marshal of France."""""""""
        """Kenneth de Moravia (also known as Kenneth Sutherland[1] ) (died 19 July 1333) was the 4th Earl of Sutherland and chief of Clan Sutherland. He was the second son of William de Moravia, 2nd Earl of Sutherland. Kenneth’s mother is unknown."""

    def test_parse_from_content_circa(self):
        content = """John Okemos (Chief Okemos) (ca. 1775-1858) was a Michigan Ojibwe (Chippewa) chief."""

        date_extractor = self.get_base_date_extractor()

        date_extractor.extract_from_content(content)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date

        self.assertEqual(u"1775", start_date.year)
        self.assertEqual(u"1858", end_date.year)

    def test_5(self):
        infobox = """{{Infobox military conflict|conflict=Battle of Arsal|partof=The [[Syrian Civil War spillover in Lebanon]] and the [[Qalamoun offensive (June-August 2014)]]|image=|caption=|date=2-7 August 2014<br>({{Age in months, weeks and days|month1=08|day1=2|year1=2014|month2=08|day2=7|year2=2014}}) |place=[[Arsal]], [[Lebanon]]|coordinates=|map_type=Lebanon|map_relief=yes|latitude=|longitude=|map_size=290px|map_marksize=|map_caption=|map_label=|territory=|result=Lebanese Armed forces victory|status=|combatants_header=|combatant1={{Flagicon image|Flag of Jabhat al-Nusra.jpg}} [[al-Nusra Front]]<br>{{flagicon image|ShababFlag.svg}} [[Islamic State of Iraq and the Levant]]|combatant2={{flagicon|Lebanon}} '''[[Lebanon]]'''*[[Lebanese Armed Forces]]*[[Internal Security Forces]]----{{flagicon|Syria}} '''[[Syrian Arab Republic]]'''* {{flagicon image|Syrian Air Force Flag.svg}} [[Syrian Arab Air Force]]|commander1={{flagicon image|ShababFlag.svg}} Abu Hasan al-Homsi{{KIA}}<ref name="commander"/><br>{{flagicon image|ShababFlag.svg}} Abu Ahmed Jumaa{{POW}}<ref name="conditions">{{cite web|url=http://english.al-akhbar.com/content/lebanon-islamist-militants-threaten-reinvade-ersal-unless-conditions-are-met|title=Lebanon: Islamist militants threaten to reinvade Ersal unless conditions are met|publisher=Al Akhbar English|date=2014-08-07|accessdate=2014-08-22}}</ref>|commander2=General [[Jean Kahwaji]]<br> Brig. General [[Chamel Roukoz]]|units1=Unknown|units2=[[Lebanese Commando Regiment|Lebanese Rangers Regiment]]<br>[[8th Infantry Brigade (Lebanon)]]<br>[[Lebanese Air Force]]|strength1=700 total militants<ref name="Hezbollah prepares for Qalamoun offensive">[http://america.aljazeera.com/articles/2015/3/24/hezbollah-prepares-major-offensive-against-isil.html Hezbollah Prepares Major Offensive Against ISIL |Al Jazeera America]</ref>|strength2=Unknown|casualties1=60 killed<ref name="utmost"/> |casualties2=20 soldiers killed,<ref name="utmost"/><ref name="captured"/> 85 wounded<ref name="borderarea"/> and 24 captured (14 released, 4 executed)<ref name="behead"/><ref>2 freed (2 August),[http://www.channelnewsasia.com/news/world/8-lebanon-soldiers-killed/1294652.html] 2 freed (3 August),[http://www.dailystar.com.lb/News/Lebanon-News/2014/Aug-04/265988-army-to-insulate-arsal-from-syria.ashx#axzz39B6nb6Tv] 3 freed (5 August),[http://www.dailystar.com.lb/News/Lebanon-News/2014/Aug-05/266095-syria-vows-to-back-lebanon-army-against-terrorism.ashx#axzz39P7yJw5T] 3 freed (6 August),[http://america.aljazeera.com/articles/2014/8/6/lebanon-syria-truce.html] 4 freed (30 August),[http://af.reuters.com/article/worldNews/idAFKBN0GU0J420140830] total of 14 soldiers freed {{wayback|url=http://www.channelnewsasia.com/news/world/8-lebanon-soldiers-killed/1294652.html |date=20141015212156 }}</ref><ref>[http://hosted2.ap.org/RIPRJ/e0478123c3cf489bb836130ffdbd2b5f/Article_2014-12-05-ML-Islamic-State/id-fc1b6b7e39c9483a93404feedc659c90 Militants announce killing of Lebanese soldier]</ref><br>20 policemen captured (6 released)<ref name="captured">[http://www.dailystar.com.lb/News/Lebanon-News/2014/Aug-23/268253-captured-soldiers-they-will-kill-us-if-hezbollah-remains-in-syria.ashx#axzz3BDF3z6Ht Captured soldiers: They will kill us, if Hezbollah remains in Syria]</ref><ref name="collapses"/><ref>[http://dailystar.com.lb/News/Lebanon-News/2014/Aug-18/267528-militants-free-two-isf-members-captured-in-arsal-clashes.ashx#axzz3BH2VvhLd Militants free two ISF members captured in Arsal clashes]</ref><ref name="behead">[http://af.reuters.com/article/worldNews/idAFKBN0GU0J420140830 Islamic State militants behead captive Lebanese soldier - video]</ref>|casualties3=42<ref name="captives"/>-50<ref name="borderarea"/> civilians killed|notes=|campaignbox={{Campaignbox Syrian civil war spillover in Lebanon}}{{Campaignbox Lebanon}}}}"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_content(infobox)

        # TODO

        """The Combined Raw Materials Board was a temporary World War II government agency that allocated the combined economic resources of the United States and Britain. It was set up by President Franklin D. Roosevelt and Prime Minister Winston Churchill on January 26, 1942.[1] Later Canada participated as an associated member in many of the Board's decisions."""


    def test_extract_from_content_additional_info(self):
        content = """Yoon Jang-ho (Hangul: 윤장호; Hanja: 尹章豪; September 21, 1980 – February 27, 2007) was a staff
        sergeant (posthumous) serving as an English translator in Afghanistan as a member of the Task Force Dasan,"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_content(content)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date

        self.assertEqual(u"21", start_date.day)
        self.assertEqual(u"09", start_date.month)
        self.assertEqual(u"1980", start_date.year)
        self.assertEqual(u"27", end_date.day)
        self.assertEqual(u"02", end_date.month)
        self.assertEqual(u"2007", end_date.year)

    def test_2digit_BC_date(self):
        infobox = """{{Infobox military conflict|conflict=Siege of Alexandria|partof=[[Ptolemy XIII Theos Philopator#Civil war|Alexandrine Civil War]]||image=|caption=|date=Late 48 BC - early or mid 47 BC|place=[[Alexandria]], [[Egypt]]|casus=|territory=|result=Roman victory|combatant1=[[Roman Republic]]|combatant2=[[Ptolemaic Kingdom]]|commander1=[[Julius Caesar|Gaius Julius Caesar]]<br />[[Cleopatra|Cleopatra VII]]<br />[[Mithridates I of the Bosporus|Mithridates of Pergamum]]|commander2=[[Ptolemy XIII Theos Philopator|Ptolemy XIII]]<br />[[Achillas]]<br /> [[Arsinoe IV of Egypt|Arsinoe IV]]<br /> [[Ganymedes (eunuch)|Ganymedes]]|strength1=1 legion ([[Legio VI Ferrata|Legio VI ''Ferrata'']])|strength2=Reportedly 20,000 and 2,000 horse|casualties1=Unknown|casualties2=Unknown}}"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)
        start_date, end_date = date_extractor.start_date, date_extractor.end_date

        self.assertEqual(u"-0048", start_date.year)
        self.assertEqual(u"-0047", end_date.year)

    def test_extract_from_content_semicolon_separated(self):
        """René Carmille (born Trémolat, Dordogne, 1886; died Dachau, Bavaria, January 25, 1945) was a punched card computer expert and comptroller general of the French Army in the early 20th century."""

    def test_extract_infobox_common_era(self):
        infobox = """{{Infobox military conflict|conflict=Expedition of Hamzah ibn 'Abdul Muttalib|date=March, 623 CE, 1 AH|place=Al-‘Īṣ|result=Intercession by a third party|combatant1=[[Muhajirun]] (Muslim exiles to [[Medina]])|combatant2=[[Quraysh (tribe)|Quraish]] of [[Mecca]]|commander1=[[Hamza ibn 'Abdul-Muttalib]]|commander2=[[Abu Jahl]]|strength1=30-40|strength2=300|casualties1=None|casualties2=None}}"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.extract_from_infobox(infobox)

        self.assertEqual("0623", date_extractor.date.year)

    def test_content_2(self):
        content = """The Zimmermann Telegram (or Zimmermann Note) was an internal diplomatic communication issued from the German Foreign Office in January 1917 that proposed a military alliance between Germany and Mexico in the event of the United States' entering World War I against Germany. The proposal was intercepted and decoded by British intelligence. Revelation of the contents enraged American public opinion and helped generate support for the United States declaration of war on Germany in April of the same year.[1]"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.content = content
        date_extractor.fill_dates()
        date = date_extractor.date

        self.assertEqual("01", date.month)
        self.assertEqual("1917", date.year)

    """Marcus Licinius Crassus (86 or 85 BC–ca. 49 BC[1]) was a quaestor of the Roman Republic in 54 BC. He was the elder son of the Marcus Crassus who formed the political alliance known as the "First Triumvirate" with Pompeius Magnus ("Pompey the Great") and Julius Caesar. """

    # region test static methods

    def test_remove_in_place(self):
        text = 'January 10, 1644 in Crillon, Oise'

        stripped = DateExtractor.remove_in_place(text)

        self.assertEqual('January 10, 1644', stripped)

    def test_6(self):
        content = """'''Tracy E. Perkins''' (?1971) is a  (reduced in rank by court martial to ) in the .On 3 January 2004, he forced, at gunpoint, civilian plumbers Zaidoun Hassoun and Marwan Fadel to leap from a road bridge in , , into the waters of the  below. The cousins Hassoun and Fadel had been caught by a U.S. checkpoint after . Fadel managed to reach the riverbank, but claims that he saw Hassoun drown and that the family later retrieved and buried the body.The battalion commander of the four soldiers,  , was reprimanded for impeding investigators.  On 8 January 2005, a  in , , , acquitted Perkins of  but convicted him of  and . He received a prison term of six months and a ."""

        date_extractor = self.get_base_date_extractor()
        date_extractor.content = content
        date_extractor.fill_dates()

        date = date_extractor.date
        self.assertEqual("1971", date.year)

    def test_inf(self):
        content = """The '''Intermediate-Range Nuclear Forces Treaty''' ('''INF''') is a 1987 agreement between the  and the  (and later its , in particular the ). Signed in  by   and   on 8 December 1987, it was ratified by the  on 27 May 1988 and came into force on 1 June of that year. The treaty was formally titled '''''The Treaty Between the United States of America and the Union of Soviet Socialist Republics on the Elimination of Their Intermediate-Range and Shorter-Range Missiles'''''.The treaty eliminated  and  ground-launched  and s with intermediate , defined as between 500-5,500&nbsp;km (300-3,400 miles). The treaty did not cover sea launched missiles.On 13 December 2001, President of the US, George W. Bush gave Russia a 6-month notice of US intent to withdraw from the  so that the United States could pursue development of the program at that time known as National Missile Defense (NMD)-already under way, in potential violation of US INF treaty obligations.<ref>Keir Giles with Dr. Andrew Monaghan , Strategic Studies Institute, 17 July 2014.</ref><ref>http://news.bbc.co.uk/1/hi/world/americas/1707812.stm</ref>In July 2014, the United States formally notified Russia that it considered them in breach of the treaty for developing and possessing prohibited weapons, while Russian officials called the restrictions of the treaty unsuitable for Russia given the then current Asian strategic situation.<ref></ref>"""

        date_extractor = self.get_base_date_extractor()
        date_extractor.content = content
        date_extractor.fill_dates()
        date = date_extractor.date
        self.assertEqual(u"1987", date.year)
        self.assertEqual(u"12", date.month)
        self.assertEqual(u"08", date.day)