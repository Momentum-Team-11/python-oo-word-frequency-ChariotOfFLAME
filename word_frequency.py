STOP_WORDS = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
    'he', 'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
    'were', 'will', 'with'
]

class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def read_contents(self):
        with open(self.filename) as file:
            words = file.read()
        return words


class WordList:
    def __init__(self, text):
        self.text = text

    def extract_words(self):
        import string
        self.list = self.text.replace("—", " ").translate(str.maketrans('', '', string.punctuation)).lower().split()
        return self.list
    
    def remove_stop_words(self):
        transformed_words = []
        for word in self.list:
            if word not in STOP_WORDS:
                transformed_words.append(word)
                self.list = transformed_words
        return self.list

    def get_freqs(self):
        finalWords = {}
        for word in self.list:
            if word in finalWords:
                finalWords[f"{word}"] += 1
            if word not in finalWords:
                finalWords[f"{word}"] = 1
        return finalWords


class FreqPrinter:
    def __init__(self, freqs):
        self.freqs = freqs

    def print_freqs(self):
        finalOutput = []
        finalLines = {}
        self.freqs = sorted(self.freqs.items(), key=lambda x: x[1], reverse=True)
        for finalWord, finalNumber in self.freqs:
            finalStar = "*" * int(finalNumber)
            finalOutput.append(f"""{finalWord} | {finalNumber} {finalStar}""")
        maximum = len(max(finalOutput, key=len))
        for finalItem in finalOutput:
            finalLength = len(finalItem)
            finalLines[f"{finalItem}"] = finalLength
        finalLines = finalLines.items()
        for output, outputIndent in finalLines:
            output = str(" " * ((maximum - outputIndent) + output.count('*') + len(str(output.count('*'))))) + output
            print(output)


if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Get the word frequency in a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        reader = FileReader(file)
        word_list = WordList(reader.read_contents())
        word_list.extract_words()
        word_list.remove_stop_words()
        printer = FreqPrinter(word_list.get_freqs())
        printer.print_freqs()
    else:
        print(f"{file} does not exist!")
        sys.exit(1)
