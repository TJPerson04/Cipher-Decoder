import csv

class WordDictionary:
    ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    all_words = []
    small_words = []

    def __init__(self, file_path: str = "words.csv", monsters_file_path: str = "dnd-monsters.csv", spells_file_path: str = "dnd-spells.csv", small_words_max_length = 5):
        print("Initializing Word Dictionary")
        
        # Open the csv of all words
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                word = ', '.join(row)
                word = self.format_string(word)
                if word == " " or word == "":
                    continue

                self.all_words.append(word)

                if (len(word) <= small_words_max_length):
                    self.small_words.append(word)
        
        # Open the csv of all dnd monsters
        with open(monsters_file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                word = ', '.join(row)
                word = self.format_string(word)
                if word == " " or word == "":
                    continue
                
                self.all_words.append(word)

                if (len(word) <= small_words_max_length):
                    self.small_words.append(word)
        
        # Open the csv of all dnd spells
        with open(spells_file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                word = ', '.join(row)
                word = self.format_string(word)
                if word == " " or word == "":
                    continue
                
                self.all_words.append(word)

                if (len(word) <= small_words_max_length):
                    self.small_words.append(word)

        # Sort the dictionary alphabetically
        self.all_words: list[str] = sorted(self.all_words)
        self.all_words = self.remove_duplicates(self.all_words)

    # Takes a sorted list as an input and returns that list without duplicate values
    def remove_duplicates(self, words_list: list[str]) -> list[str]:
        output = []
        for i in range(len(words_list)):
            if i == 0:
                continue

            curWord = words_list[i]
            prevWord = words_list[i - 1]

            if (curWord != prevWord):
                output.append(curWord)
        
        return output

    def format_string(self, text):
        text = text.lower()
        text = text.split('(')[0]
        output = ""
        for letter in text:
            if (letter in self.ALPHABET):
                output += letter
        
        return output

    def is_word(self, word: str) -> bool:
        '''
        Binary search to determine if the word is a valid word (i.e. is it in the all_words list)
        '''
        upper = len(self.all_words) - 1
        lower = 0
        index = (upper + lower) // 2
        while (index != upper and index != lower):
            if (word == self.all_words[index]):
                return True
            elif (word < self.all_words[index]):
                upper = index
            else:
                lower = index
            index = (upper + lower) // 2
        return False
    
    def is_beginning_of_word(self, text: str) -> bool | list[str]:
        '''
        Binary search to determine if the string is the beginning of a valid word (i.e. is it in the all_words list)
        '''
        output = []

        upper = len(self.all_words) - 1
        lower = 0
        index = (upper + lower) // 2
        while (index != upper and index != lower):
            if (self.all_words[index].startswith(text)):
                break
            elif (text < self.all_words[index]):
                upper = index
            else:
                lower = index
            index = (upper + lower) // 2

        while (self.all_words[index].startswith(text)):
            output.append(self.all_words[index])
            index += 1
        if (len(output) == 0):
            return False
        else:
            return output
    

    def contains_valid_word(self, text: str) -> bool:
        '''
        Returns whether or not the given string of text contains any valid words
        '''
        # Remove all '.' from text and separate by spaces
        text_ar = text.replace('.', '').split(' ')

        # Check if any of the words in the string are valid words
        for word in text_ar:
            if self.is_word(word):
                return True
        return False
    
    def get_words_of_size(self, size):
        output = []
        for word in self.all_words:
            if len(word) == size:
                output.append(word)
        
        return output