from __future__ import division
import re

def char_count_words(words):
    return sum(len(word.decode("utf-8")) for word in words)

def char_count_text(text):
    return len(re.sub(r'[^\w]','',text))

def get_words_text(text):
    return re.sub("[^\w]", " ",  text).split()

def word_count_text(text):
    return len(get_words_text(text))

def unique_words_text(text):
    return list(set(get_words_text(text)))

def unique_words_count_text(text):
    return len(unique_words_text(text))

def get_sentences_text(text):
    return re.split(r'''[.!?]['"]?\s{1,2}(?=[A-Z])''',text)

def sentence_count_text(text):
    return len(get_sentences_text(text))

def avg_words_sentence(text):
    return word_count_text(text)/sentence_count_text(text)

def lexical_diversity(text):
    return unique_words_count_text(text)/word_count_text(text)

def unique_words_p_N(text,N):
    return N*lexical_diversity(text)

def syllables_count(text):
    return sum([syllable_count(x) for x in get_words_text(text)])

def complex_words_count(text):
    return sum([1 for x in get_words_text(text) if syllable_count(x)>=3])

syl_problem_words = {
    'every': 2,
    'family': 2,
    'something': 2,
}

# Syllables counted as two but should be one
subsyl = (
    re.compile(r'cial'),
    re.compile(r'tia'),
    re.compile(r'cius'),
    re.compile(r'cious'),
    re.compile(r'giu'),
    re.compile(r'ion'),
    re.compile(r'iou'),
    re.compile(r'^evevry'),
    re.compile(r'sia$'),
    re.compile(r'.ely$'),
    re.compile(r'[^szaeiou]es$'),
    re.compile(r'[^tdaeiou]ed$'),
    re.compile(r'^ninet'),
    re.compile(r'^awe'),
)

# Syllables counted as one but should be two
addsyl = (
    re.compile(r'ia'),
    re.compile(r'rie[rt]'),
    re.compile(r'dien'),
    re.compile(r'ieth'),
    re.compile(r'iu'),
    re.compile(r'io'),
    re.compile(r'ii'),
    re.compile(r'les?$'),
    re.compile(r'[aeiouym][bp]l$'),
    re.compile(r'[aeiou]{3}'),
    re.compile(r'ndl(ed)?$'),
    re.compile(r'mpl(ed)?$'),
    re.compile(r'^mc'),
    re.compile(r'ism$'),
    re.compile(r'([^aeiouy])\1l(ed)?$'),
    re.compile(r'[^l]lien'),
    re.compile(r'^coa[dglx].'),
    re.compile(r'[^gq]ua[^aeiou]'),
    re.compile(r'[sd]nt$'),
    re.compile(r'\wshes$'),
    re.compile(r'\wches$'),
    re.compile(r'\wghes$'),
    re.compile(r'\wches$'),
    re.compile(r'\w[aeiouy]ing[s]?$'),
)

# Syllable prefixes and suffixes
syl_prefix_suffix = (
    re.compile(r'^un'),
    re.compile(r'^fore'),
    re.compile(r'ly$'),
    re.compile(r'less$'),
    re.compile(r'ful$'),
    re.compile(r'ers?$'),
    re.compile(r'ings?$'),
)

def syllable_count(word):
    # Based on Tyler Kendall's work
    # Improved on Greg Fast's Lingua::EN::Syllable Perl Module
    # http://ncslaap.lib.ncsu.edu/tools/scripts/english_syllable_counter-101.R
    syl_count = 0
    word = word.lower()
    # Remove non-alpha characters
    word = re.sub(r'[^\w]','', word)
    # Adjusting for common exceptions
    if word in syl_problem_words:
        return syl_problem_words[word]

    # Remove prefixes and suffixes
    prefix_suffix_count = 0
    for sps in syl_prefix_suffix:
        prefix_suffix_count += len(sps.findall(word))
        word = sps.sub('', word)

    # Remove non-word characters
    word = re.sub(r'[^a-z]','', word)

    # For syllables exceptions
    for s_syl in subsyl:
        if s_syl.search(word):
            syl_count -= 1

    for a_syl in addsyl:
        if a_syl.search(word):
            syl_count += 1

    if len(word) == 1:
        syl_count = 1
    else:
        word_parts = re.split(r'[^aeiouy]+',word)
        word_part_count = 0;
        for word_part in word_parts:
            if word_part != '':
                word_part_count += 1
        syl_count = word_part_count + prefix_suffix_count

    return syl_count
