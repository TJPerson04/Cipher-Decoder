import csv

class WordDictionary:
    # A constant list of the used alphabet
    ALPHABET: list[str] = []
    
    # A list of all valid words according to the input .csv files
    all_words: list[str] = []

    # This isn't used internally atm, but in the future it could be used to speed up searches that are
    # unlikely to need larger words
    small_words: list[str] = []

    def __init__(self, dictionary_file_paths: list[str] = ["word_lists/words.csv"], small_words_max_length = 5, alphabet: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']):
        '''
        A holder for a dictionary of valid words.\n

        dictionary_file_paths: A list of file paths to .csv files containing the valid words for the dictionary\n
        small_words_max_length: The maximum length a word can be to be considered a "small" word\n
        alphabet: A list of characters representing the possible characters in the alphabet.
        '''
        
        # Initialize
        print("Initializing Word Dictionary")

        self.ALPHABET = alphabet
        
        # Open the csv of all words
        for file_path in dictionary_file_paths:
            with open(file_path) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    word = row[0]
                    word = self.format_string(word)
                    word = self.filter_string(word, 1)
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
        '''
        Takes an alphabetically sorted list as an input and returns that list without duplicate values.
        '''

        # Loop through every word, adding it to the output if it isn't there already,
        # ignoring it otherwise
        output = []
        for i in range(len(words_list)):
            if i == 0:
                output.append(words_list[i])
                continue

            curWord = words_list[i]
            prevWord = words_list[i - 1]

            if (curWord != prevWord):
                output.append(curWord)
        
        return output

    def format_string(self, text):
        '''
        A specific helper function to format strings from a D&D spells list.
        If you are looking for a function to format a string, you should probably use filter_string.
        '''
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
        Binary search to determine if the string is the beginning of a valid word (i.e. is it in the all_words list)\n
        
        Returns: A list of the words that begin with the given text, or False if none exist
        '''
        output = []

        # Use a binary search to go through all_words, finding a valid word that begins with
        # the given text
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

        # Since all_words is sorted alphabetically, we can search the surrounding words
        # adding all the words that begin with the given text
        back_index = index - 1
        while (self.all_words[back_index].startswith(text)):
            output.append(self.all_words[back_index])
            back_index -= 1

        while (self.all_words[index].startswith(text)):
            output.append(self.all_words[index])
            index += 1
        
        # Return
        if (len(output) == 0):
            return False
        else:
            return output
        
    def key_contains_valid_word(self, key: str, min_size: int = 1) -> bool:
        '''
        Returns whether or not the given key contains a valid word\n
        This is not as efficient as the other methods since it doesn't use binary search, 
        instead looping through every valid word.\n

        key: The key to check\n
        min_size: The minimum size of the valid word
        '''
        # Loop through every valid word
        for word in self.all_words:
            # Ignore any word less than the minimum size
            if (len(word) < min_size):
                continue

            # Check if the key includes the valid word anywhere in it
            if (key.find(word) != -1):
                return True
        
        return False
    

    def contains_valid_word(self, text: str) -> bool:
        '''
        Returns whether or not the given sentence of text contains any valid words
        '''
        # Remove all special characters from text and separate it by spaces
        text = self.filter_string(text, 1)
        text_ar = text.split(' ')

        # Check if any of the words in the string are valid words
        for word in text_ar:
            if self.is_word(word):
                return True
        return False
    
    def get_words_of_size(self, size: int) -> list[str]:
        '''
        Gets a list of all valid words that are the given size
        '''
        output = []
        for word in self.all_words:
            if len(word) == size:
                output.append(word)
        
        return output
    
    def filter_string(self, text: str, min_word_size: int) -> str:
        '''
        Removes all words under size in the string. Also removes
        any characters not in the alphabet.
        '''
        # Make sure the text is all lowercase
        text = text.lower()

        # new_text will be the old text but only with spaces and characters that
        # are in the supplied alphabet
        new_text = ""
        for character in text:
            if (character == " " or character in self.ALPHABET):
                new_text += character

        # Split the sentence into an array of words
        text_ar = new_text.split(' ')
        
        # Loop through the array of words, only keeping those that are
        # at least min_word_size letters long
        output = ""
        for word in text_ar:
            if (len(word) < min_word_size):
                continue

            output += word + " "
        
        # Remove the trailing space from the output string and return it
        output = output.removesuffix(" ")
        return output
    
    def is_promising_key(key: str) -> int:
        '''
        Check if a given key is "promising", which here is checked by seeing
        if the key repeats at all.\n

        key: The key to check\n

        Returns: The length of the repeating substring (or 0 if doesn't exist)
        '''

        # Get the key in reverse
        key_rev = key[::-1]

        # See if there is another instance of the first letter in the key
        # If there is, keep track of where it is in the key
        # If there isn't, the key can't be repeating, so return 0
        try:
            rev_index = key_rev.index(key[0], 1, len(key_rev) - 1)
        except:
            return 0
        
        # Loop through the key and its reverse, starting at the obtained index,
        # checking that each character matches until you reach the beginning of the reverse
        # key (which is the end of the forward key)
        #
        # for_index will be the index of the character we are looking at in the forward key
        # repeat_length is kept track of for returning purposes, as that is eqal to the length
        #   of the repeating substring if it exists
        for_index = 0
        repeat_length = rev_index
        while rev_index >= 0:
            if (key_rev[rev_index] != key[for_index]):
                return 0
            for_index += 1
            rev_index -= 1
        return repeat_length