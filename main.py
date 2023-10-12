import re
from hazm import *
import os
import codecs
import sets
import wordcloud
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def extract_persian_text(file_path):
    with open(file_path, 'rb') as file:
        srt_content = file.read()

    encodings = ['utf-8', 'utf-16', 'latin-1']

    for encoding in encodings:
        try:
            srt_content = srt_content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    persian_text = re.findall(r'[\u0600-\u06FF\s]+', srt_content)
    return persian_text


def save_persian_text(file_path, persian_text):
    filename = file_path.split('/')[-1].split('.')[0]

    output_directory = "extractedText"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = f"extractedText/{filename}_persian.txt"

    with open(output_file, 'w', encoding='utf-8') as file:
        for text in persian_text:
            file.write(text.strip() + '\n')


def loadFirstTime():
    srt_files = [
        'texts/Skyscraper.2018.720p.WEB-DL.H264.AC3-EVO.[UTF-8].srt',
        'texts/Sleepless.2017.BDRip.x264-GECKOS.(www.esubtitle.com).srt',
        'texts/Star.Wars.TheLast.Jedi.2017.HC.720p.HDTC.MkvCage.srt',
        'texts/The.Hateful.Eight.2015.720p.BluRay.x264.SPARKS.srt',
        'texts/We_Have_Always_Lived_in_the_Castle.srt'
    ]

    for file_path in srt_files:
        persian_text = extract_persian_text(file_path)
        save_persian_text(file_path, persian_text)


def saveListTofiles(file_path, my_list):
    with open(file_path, 'w') as file:
        for item in my_list:
            file.write(str(item) + "\n")
        file.write("\n")


def normalizer(filmSentences):
    normalizer = Normalizer(
        remove_diacritics=True,
        remove_specials_chars=True,
        decrease_repeated_chars=True,
        unicodes_replacement=True,
        persian_numbers=True,
        seperate_mi=True
    )
    normalize_text = normalizer.normalize(filmSentences)
    return normalize_text


def tokenize(normalize_text):
    tokenizer = WordTokenizer()
    tokenizedTokens = tokenizer.tokenize(normalize_text)
    return tokenizedTokens


def findallSentences(file_path):
    with open("extractedText/" + file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    temp = ""
    for line in lines:
        line = line.strip()
        if line:
            temp = temp + line + " "
    return temp


def removeStopWords(tokens):
    stopWords = set(codecs.open('stopWords/persian',
                    encoding='utf-8').read().split('\n'))

    temp = []
    for t in tokens:
        if not t in stopWords:
            temp.append(t)
    return temp


def createWordCloud(file_path, tokenList):
    prefix = "wordClouds_"

    wc = wordcloud.WordCloud(width=800,
                             height=400,
                             background_color='white',
                             font_path='fonts/B-NAZANIN.TTF',
                             max_words=200)

    output_directory = "wordClouds"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    text = " ".join(tokenList)
    faWc = wc.generate(text)

    fig = plt.figure(figsize=(10, 5))
    plt.imshow(faWc, interpolation='bilinear')
    plt.axis("off")

    output_filename = os.path.join(
        output_directory, f"{prefix}{os.path.basename(file_path).split('.txt')[0]}.png")
    plt.savefig(output_filename, bbox_inches='tight', pad_inches=0, dpi=300)

    # plt.show()


def lemmatizer(tokenList):
    lemmatizer = Lemmatizer()
    temp = []
    for token in tokenList:
        res = lemmatizer.lemmatize(token)
        temp.append(res)
    return temp


def stemmer(tokenList):
    stemmer = Stemmer()
    temp = []
    for token in tokenList:
        res = stemmer.stem(token)
        temp.append(res)
    return temp


def main():
    loadFirstTime()
    films = ["Skyscraper_persian.txt", "Sleepless_persian.txt", "Star_persian.txt",
             "The_persian.txt", "We_Have_Always_Lived_in_the_Castle_persian.txt"]
    # films = ["Skyscraper_persian.txt"]

    for film in films:
        filmSentences = findallSentences(film)
        normalize_text = normalizer(filmSentences)
        tokenizedTokens = tokenize(normalize_text)
        filteredTokens = removeStopWords(tokenizedTokens)
        saveListTofiles("tokens/" + film, filteredTokens)
        lemmatizeFilter = lemmatizer(tokenizedTokens)
        saveListTofiles("lemma/" + film, lemmatizeFilter)
        stemFilter = stemmer(filteredTokens)
        saveListTofiles("stem/" + film, filteredTokens)
        output = removeStopWords(lemmatizeFilter)
        createWordCloud(film, output)
        saveListTofiles("outputs/" + film, output)


if __name__ == "__main__":
    main()
