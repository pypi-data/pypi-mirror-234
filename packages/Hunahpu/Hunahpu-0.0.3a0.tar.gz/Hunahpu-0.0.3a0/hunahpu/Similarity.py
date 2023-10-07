from nltk import ngrams
from unidecode import unidecode
from thefuzz import fuzz, process
from langid import classify
from googletrans import Translator

import re


def __parse_string(text):
    '''
    This function allows to remove unneeded characters

    Parameters
    ----------
    text : str
        text to parse
    '''
    data = str(text).lower()
    data = re.sub(r'<[^>]+>', '', data)
    data = re.sub(r'[\$_\^]', '', re.sub(r'\\\w+', '', data))
    data = unidecode(data)
    return data

def parse_string(text):
    return __parse_string(text)

def __jc_similarity_base(title1, title2, n=3):
    '''
    Utility function to avoid code duplication, implementation below.
    '''
    n1 = ngrams(title1.split(), n)
    n2 = ngrams(title2.split(), n)
    n1 = set(n1)
    n2 = set(n2)
    unilen = len(n1.union(n2))
    lenmin = min([len(n1), len(n2)])

    if unilen == 0 or lenmin == 0:
        S = 0
    else:
        J = len(n1.intersection(n2)) / unilen
        C = len(n1.intersection(n2)) / lenmin
        if J + C != 0:
            S = 2 * J * C / (J + C)
        else:
            S = 0
    return S


def JCSimilarity(
        title1,
        title2,
        n=3,
        boolean=False,
        threshold=0.8,
        use_translation=True,
        use_parsing=True):
    '''
    Computes titles similarity according to section 2.6 of
    https://arxiv.org/pdf/1911.02782.pdf

    Parameters
    ----------
    title1 : str
        text to compare
    title2 : str
        second text to compare
    n : int (optional)
        number n in n-gram partition of titles
    boolean : bool
        If you want the output to be a bool
    threshold : float
        Threshold for the boolean outpput
    use_translation : str
        enable translation support
    use_parsing: boolean
        use parsing to remove unneeded characters

    Returns
    -------
    similarity : float/bool
        Number between 0 and 1. 1 means the titles are the same and 0 means completely different
        Or True if similarity is avobe threshold, false otherwise
    '''
    title1 = unidecode(title1.lower())
    title2 = unidecode(title2.lower())

    if use_parsing:
        S = __jc_similarity_base(__parse_string(
            title1), __parse_string(title2), n)
    else:
        S = __jc_similarity_base(title1, title2, n)

    if S < threshold and use_translation:
        lang, _ = classify(title1)
        if lang != "en":
            translator = Translator()
            title1 = translator.translate(title1).text
        lang, _ = classify(title2)
        if lang != "en":
            translator = Translator()
            title2 = translator.translate(title2).text

        if use_parsing:
            S = __jc_similarity_base(__parse_string(
                title1), __parse_string(title2), n)
        else:
            S = __jc_similarity_base(title1, title2, n)

    if boolean:
        if S >= threshold:
            return True
        else:
            return False
    else:
        return S


def __colav_similarity(
        paper1,
        paper2,
        ratio_thold=90,
        partial_thold=95,
        low_thold=80,
        use_translation=False,
        verbose=0):
    '''
    Utility function to avoid code duplication, public implementation below.
    '''
    label = False

    title1 = paper1['title']
    journal1 = paper1['journal']
    year1 = paper1['year']

    title2 = paper2['title']
    journal2 = paper2['journal']
    year2 = paper2['year']

    year_check = False
    if year1 and year2:
        if year1 == year2:
            year_check = True

    journal_check = False
    if journal1 and journal2:
        if fuzz.ratio(
            unidecode(
                journal1.lower()), unidecode(
                journal2.lower())) > ratio_thold:
            journal_check = True

    length_check = False
    if len(title1.split()) > 3 and len(title2.split()) > 3:
        length_check = True

    if verbose == 5:
        if journal_check:
            print("Journals are the same")
        if year_check:
            print("Years are the same")

    ratio = fuzz.ratio(title1, title2)
    if verbose == 5:
        print("Initial ratio: ", ratio)
    if ratio > ratio_thold and length_check:
        label = True
    else:
        title1_list = title1.split("[")
        title2_list = title2.split("[")
        if min([len(item) for item in title1_list]) > 10 and min([len(item) for item in title2_list]) > 10:
            for title in title1_list:
                _, ratio = process.extractOne(
                    title, title2_list, scorer=fuzz.ratio)
                if ratio > ratio_thold:
                    label = True
                    break
            if verbose == 5:
                print("ratio over list: ", ratio)
            if not label:
                for title in title1_list:
                    _, ratio = process.extractOne(
                        title, title2_list, scorer=fuzz.partial_ratio)
                    if ratio > partial_thold:
                        label = True
                        break
                    elif ratio > low_thold:
                        if journal_check and year_check:
                            label = True
                            break
                if verbose == 5:
                    print("partial ratio over list: ", ratio)

    # Partial ratio section
    if label == False:

        ratio = fuzz.partial_ratio(title1, title2)
        if verbose == 5:
            print("partial ratio: ", ratio)

        if ratio > partial_thold and length_check:
            label = True
        elif ratio > low_thold:
            if journal_check and year_check:
                label = True

    # Translation section
    if label is False and use_translation:
        lang1, _ = classify(title1)
        lang2, _ = classify(title2)
        if lang1 != "en" or lang2 != "en":
            if lang1 != "en":
                translator = Translator()
                try:
                    title1 = translator.translate(title1).text
                except Exception as e:
                    if verbose == 5:
                        print(e)
                if verbose == 5:
                    print("Title 1 translated to ", title1)
            if lang2 != "en":
                translator = Translator()
                try:
                    title2 = translator.translate(title2).text
                except Exception as e:
                    print(e)
                if verbose == 5:
                    print("Title 2 translated to ", title2)

            ratio = fuzz.ratio(title1, title2)
            if verbose == 5:
                print("Ratio over translation: ", ratio)
            if ratio > ratio_thold:
                label = True
            if label is False:
                ratio = fuzz.partial_ratio(title1, title2)
                if verbose == 5:
                    print("partial ratio over translation: ", ratio)
                if ratio > partial_thold:
                    label = True
                elif ratio > low_thold:
                    if journal_check and year_check:
                        label = True

    return label


def ColavSimilarity(
        paper1,
        paper2,
        ratio_thold=96,
        partial_thold=98,
        low_thold=76,
        use_translation=False,
        use_parsing=True):
    '''
    custom metric for similarity using multiple nested metrics from fuzzywuzzy

    Parameters
    ----------
    paper1: dictionary
        dictionary with keys title,journal and year is required
    paper2: dictionary
        dictionary with keys title,journal and year is required
    ratio_thold: int
        threshold for  ratio matric
    partial_thold: int
        threshold for partial ratio
    low_thold: int
        low threshold for ratios
    use_translation : boolean
        enable translation support
    use_parsing: boolean
        use parsing to remove unneeded characters
    '''

    if paper1['title']  is None:
        paper1['title']  = ""
    if paper2['title']  is None:
        paper2['title']  = ""
    if not isinstance(paper1['journal'], str):
        paper1['journal'] = str(paper1['journal'])
    if not isinstance(paper2['journal'], str):
        paper2['journal'] = str(paper2['journal'])

    paper1['title'] = unidecode(paper1['title'].lower())
    paper2['title'] = unidecode(paper2['title'].lower())

    if paper1['year']:
        paper1['year'] = int(paper1['year'])
    if paper2['year']:
        paper2['year'] = int(paper2['year'])

    label = False

    if not use_parsing:
        label = __colav_similarity(
            paper1,
            paper2,
            ratio_thold,
            partial_thold,
            low_thold,
            use_translation)
    elif use_parsing:
        paper1['title'] = __parse_string(paper1['title'])
        paper2['title'] = __parse_string(paper2['title'])
        label = __colav_similarity(
            paper1,
            paper2,
            ratio_thold,
            partial_thold,
            low_thold,
            use_translation)
    return label
