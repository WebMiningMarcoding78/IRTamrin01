import re
from hazm import *

def extract_persian_text(file_path):
    with open(file_path, 'rb') as file:
        srt_content = file.read()

    encodings = ['utf-8', 'utf-16', 'latin-1']  # Add more encodings if needed

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
    output_file = f"{filename}_persian.txt"

    with open(output_file, 'w', encoding='utf-8') as file:
        for text in persian_text:
            file.write(text.strip() + '\n')


def main():
    # films = ["Skyscraper_persian.txt","Sleepless_persian.txt","Star_persian.txt","The_persian.txt","We_Have_Always_Lived_in_the_Castle_persian.txt"]
    films = ["We_Have_Always_Lived_in_the_Castle_persian.txt"]
    
    ## it must runs just for the first
    # srt_files = [
    #     'texts/Skyscraper.2018.720p.WEB-DL.H264.AC3-EVO.[UTF-8].srt',
    #     'texts/Sleepless.2017.BDRip.x264-GECKOS.(www.esubtitle.com).srt',
    #     'texts/Star.Wars.TheLast.Jedi.2017.HC.720p.HDTC.MkvCage.srt',
    #     'texts/The.Hateful.Eight.2015.720p.BluRay.x264.SPARKS.srt',
    #     'texts/We_Have_Always_Lived_in_the_Castle.srt'
    # ]

    # for file_path in srt_files:
    #     persian_text = extract_persian_text(file_path)
    #     save_persian_text(file_path, persian_text)

    for film in films :
        filmSentences = findallSentences(film)
        normalizer = Normalizer()
        normalize_text = normalizer.normalize(filmSentences)

        word_tokenizer = WordTokenizer()
        lexical_tokens = word_tokenizer.tokenize(normalize_text)

        splitter = TokenSplitter()
        splitted_tokens = [splitter.split_token_words(token) for token in lexical_tokens]
        print(splitted_tokens)
    

def findallSentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    temp = ""
    for line in lines:
        line = line.strip()
        if line:
           temp = temp + line
    return temp

if __name__ == "__main__":
    main()