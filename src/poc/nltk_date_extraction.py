# coding=utf-8

import nltk
import timex
from datetime import datetime, date

if __name__ == "__main__" :
    now = date.today()
    basedate = date(now.year, now.month, now.day)

    text = "The Damascus Titan missile explosion refers to an incident where the fuel in a nuclear armed missile " \
           "exploded at missile launch facility Launch Complex 374-7 in Damascus, Arkansas, on September 18–19, " \
           "1980. The facility was part of the 374th Strategic Missile Squadron at the time of the explosion. On " \
           "11 November 2001."

    w_tokens = nltk.word_tokenize(text)
    pt = nltk.pos_tag(w_tokens)
    # print pt
    tagged = timex.tag(text)
    print tagged
    ne = timex.ground(tagged, basedate)
    # ne = nltk.ne_chunk(pt)
    print ne