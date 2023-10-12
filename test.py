import codecs 
import sets

def removeStopWords(tokens):
    stopWords = set(codecs.open('stopWords/persian',
                    encoding='utf-8').read().split('\n'))
    temp = []
    for t in tokens:
        if not t in stopWords:
            temp.append(t)
    return temp


if __name__ == '__main__':
    print(removeStopWords(["من","گل","زیبا","زیباتر","گل های","های"]))