import re, json, unicodedata

def strip_test(text):
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub('[^a-z0-9 ]+', '', str(text).lower())
    text = re.sub(' +', ' ', text)
    return text

def save_file(reviews, filename):
    file = open(filename, 'w')
    data = json.dumps(reviews)
    file.write(data)
    file.close()
