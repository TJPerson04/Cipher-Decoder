from collections.abc import Callable
import os
import time
from WordDictionary import WordDictionary
import threading

class DictCompare:
    def __init__(self, encoded_text: str, cipher_func: Callable[[str, str], str], rev_cipher_func: Callable[[str, str], str] | None=None, word_dict: WordDictionary = WordDictionary(), num_cores: int = 16, min_valid_word_length = 5, separators: tuple[bool, bool, bool] = (4, 6, 12), starting_key_part: list[str]=[""], keys_to_test=None):
        '''
        Will try and solve the given cipher using keys determined from the dictionary of words.\n

        encoded_text: The encoded string of text\n
        cipher_func: The cipher function to call that encodes a given string\n

        rev_cipher_func: A function to reverse engineer a key given the plaintext and the ciphertext\n
        word_dict: The associated WordDictionary\n
        num_cores: The number of separate threads to run at once\n
        starting_key_part: If given, this will add the given string to the beginning of each key.\n
        keys_to_test: This is a list of keys to test. By default this will be the word dictionary's all_words list.\n
        '''
        self.encoded_text = encoded_text
        self.cipher_func = cipher_func

        self.rev_cipher_func = rev_cipher_func
        self.word_dict = word_dict
        self.num_cores = num_cores
        self.min_valid_word_length = min_valid_word_length
        self.separators = separators
        self.starting_key_part = starting_key_part

        if (keys_to_test == None):
            self.keys_to_test = word_dict.all_words
        else:
            self.keys_to_test = keys_to_test
    
    def get_size_of_section(self, start: int, total_length: int):
        '''
        Used by threads to determine the size of data that a single thread gets.\n
        Note: This is not exact, just gives a good estimate.
        '''
        length = total_length - start
        return length // self.num_cores
    
    def get_estimated_run_time(self):
        '''
        Try and estimate how long the current testing will take.\n
        Note: THIS IS VERY INACCURATE ATM, BUT IT DOES GIVE A CLOSE ESTIMATE.
        '''
        startTime = time.time_ns()

        # Run a couple checks and see how long that takes
        for i in range(20):
            word = self.starting_key_part[0] + self.keys_to_test[i]
            decoded_text = self.cipher_func(self.encoded_text, word)
            decoded_text_filtered = self.word_dict.filter_string(decoded_text, self.min_valid_word_length)
            self.word_dict.contains_valid_word(decoded_text_filtered)

        endTime = time.time_ns()

        timeMult = len(self.starting_key_part) * len(self.keys_to_test) / self.num_cores

        return (endTime - startTime) * timeMult
    
    def print_estimated_run_time(self, is_two_word=False):
        '''
        Try and display how long the current testing will take.\n
        Note: THIS IS VERY INACCURATE ATM, BUT IT DOES GIVE A CLOSE ESTIMATE.
        '''
        estimated_time_ns = self.get_estimated_run_time()
        if (is_two_word):
            estimated_time_ns = estimated_time_ns ** 2
        
        seconds = estimated_time_ns // 1_000_000_000
        minutes = seconds // 60
        hours = minutes // 60

        seconds %= 60
        minutes %= 60
        hours %= 60

        print(f'TEST: {estimated_time_ns}')
        print(f'Estimated Completion Time: {hours}h {minutes}m {seconds}s')
    

    
    def thread_func(self, start: int, end: int, thread_index: int):
        '''
        This is the function that is meant to be run by each thread. This will
        test keys within the given indices (inclusive).
        '''
        # Log start
        print("Starting thread: " + str(thread_index))
        
        # Check all words in section
        with open(f'one_word_output_{thread_index}.txt', 'a') as out_file:
            for keyStart in self.starting_key_part:
                for i in range(end - start):
                    index = start + i
                    word = keyStart + self.keys_to_test[index]
                    decoded_text = self.cipher_func(self.encoded_text, word)
                    decoded_text_filtered = self.word_dict.filter_string(decoded_text, self.min_valid_word_length)
                    if (self.word_dict.contains_valid_word(decoded_text_filtered)):
                        output_text = f'key: {word} | text: {decoded_text}\n'
                        print(output_text)
                        out_file.write(output_text)
            
        print(f'Ending thread: {thread_index}')
    
    def thread_func_two_word_keys(self, start: int, end: int, thread_index: int):
        '''
        This is the function that is meant to be run by each thread. This will
        test keys within the given indices (inclusive), adding every key on top of 
        it.
        '''
        # Log start
        print("Starting thread: " + str(thread_index))
        
        # Check all words in section
        with open(f'two_word_output_{self.separators[0] + 1}_letters_{thread_index}.txt', 'w') as output_1, open(f'two_word_output_{self.separators[1] + 1}_letters_{thread_index}.txt', 'w') as output_2, open(f'two_word_output_{self.separators[2] + 1}_letters_{thread_index}.txt', 'w') as output_3:
            for keyStart in self.starting_key_part:
                for i in range(end - start):
                    index = start + i
                    # Add a second word to the key
                    for j in range(len(self.keys_to_test)):
                        word = keyStart + self.keys_to_test[index] + self.keys_to_test[j]
                        decoded_text = self.cipher_func(self.encoded_text, word)
                        is_valid = self.contains_valid_word_by_size(decoded_text)
                        self.check_solution(word, decoded_text, output_1, output_2, output_3, is_valid)
                
                        if (j % 100000 == 0):
                            output_1.flush()
                            output_2.flush()
                            output_3.flush()
                            print(f'Checking {word}')
            
        print(f'Ending thread: {thread_index}')

    def run_func_across_dict(self, func: Callable[[int, int, int], any]):
        '''
        Run the given function across every word in the given WordDictionary.\n
        The function must accept a start_index, end_index, and thread_id as parameters.
        '''
        # Make the threads
        threads = []
        section_size = self.get_size_of_section(0, len(self.keys_to_test))
        for i in range(self.num_cores - 1):
            start_index = section_size * i
            end_index = start_index + section_size - 1
            print(f'{start_index}, {end_index}')
            new_thread = threading.Thread(target=func, args=(start_index, end_index, i))
            threads.append(new_thread)
        
        last_thread_start_index = len(self.keys_to_test) - section_size - 15
        last_thread_end_index = len(self.keys_to_test) - 1
        print(f'{last_thread_start_index}, {last_thread_end_index}')
        last_thread = threading.Thread(target=func, args=(last_thread_start_index, last_thread_end_index, self.num_cores - 1))
        threads.append(last_thread)

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for the threads to join
        print("Now waiting for threads to finish")
        for thread in threads:
            thread.join()

    def concat_output_files(self, fname_prefix="two_word_output"):
        '''
        Combines multiple text files created by different threads into one,
        deleting the old files.
        '''
        filenames = []
        for i in range(self.num_cores):
            filenames.append(f'{fname_prefix}_{i}.txt')
        with open(f'{fname_prefix}.txt', 'a') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

                os.remove(fname)

    def contains_valid_word_by_size(self, text: str) -> tuple[bool, bool, bool]:
        '''
        Returns three bools of decreasing security, using the separators property to separate the output by 
        the length of the valid word in the given string.
        '''
        out1 = False
        out2 = False
        text_ar = text.replace('.', '').split(' ')
        for word in text_ar:
            if (len(word) < self.separators[0]):
                continue

            if (self.word_dict.is_word(word)):
                out1 = True

                if (len(word) > self.separators[1]):
                    out2 = True
            
                if (len(word) > self.separators[2]):
                    return (True, True, True)
    
        return (out1, out2, False)
    
    def check_solution(self, word: str, decoded_text: str, file_1, file_2, file_3, is_valid: tuple[bool, bool, bool]):
        '''
        Will output the results of a tested word according to the is_valid tuple.\n
        If the result satisfies is_valid[0], it will be logged in file_1.\n
        If it also satisfies is_valid[1], it will also be logged in file_2, as well as being printed to the console.\n
        And if it also satisfies is_valid[2], it will be logged to file_3.
        '''
        # If it does not satisfy the first condition
        if (not is_valid[0]):
            return
    
        # The text to log
        output_text = f'key: {word} | text: {decoded_text}\n'
    
        # If it does satisfy the first condition
        file_1.write(output_text)

        # If it also satisfies the second condition
        if (is_valid[1]):
            print("-------")
            print(output_text)
            file_2.write(output_text)
    
        # If it also satisfies the third condition
        if (is_valid[2]):
            file_3.write(output_text)

    def get_possible_keys(self, min_word_size=1) -> list[list[str]]:
        '''
        Get a list of keys that result in a valid word for every encoded word in the encoded_text.\n
        If a minimum word size is specified, it will ignore any encoded words smaller than that.\n

        Returns: A list of keys for every word (ex: return_value[0] will be a list of valid keys for the first encoded word
        that is at least min_word_size characters long)
        '''
        
        if (self.rev_cipher_func == None):
            print("Error: No reverse cipher function provided")
            return

        # Get a list of words that are at least min_word_size characters long
        text_list = self.word_dict.filter_string(self.encoded_text, min_word_size).split(' ')

        # For every word in the encoded text, loop through every valid word
        # of the same size. Then, using the encoded text as the ciphertext, and 
        # the valid word as the plaintext, reverse engineer the key using rev_cipher_func,
        # adding that key to the overall list for that encoded word.
        possible_keys = []
        for i in range(len(text_list)):
            word = text_list[i]
            keys_list = []
            for valid_word in self.word_dict.get_words_of_size(len(word)):
                key = self.rev_cipher_func(valid_word, word)
                keys_list.append(key)
            
            possible_keys.append(keys_list)
        
        return possible_keys

    
    ### SOLVING FUNCTIONS ###
    
    def quick_solve(self, min_word_size=5):
        '''
        Gets a list of all keys that give valid outputs for each letter,
        then searchs through those keys for ones that contain a valid word.\n

        min_word_size: The minimum size a word can be in a key to be considered valid.
            Increase this value for more results.
            The max value this should be is the length of your longest encoded word.
        '''
        if (self.rev_cipher_func == None):
            print("Error: No reverse cipher function provided")
            return

        text_list = self.word_dict.filter_string(self.encoded_text, min_word_size).split(' ')
        possible_keys = self.get_possible_keys(min_word_size)

        for i in range(len(possible_keys)):
            word = text_list[i]
            possible_keys_for_word = possible_keys[i]
            print(f'Checking {word}')
            for key in possible_keys_for_word:
                if (self.word_dict.key_contains_valid_word(key, min_word_size)):
                    print(f'\033[31mPossible key for {word}:')
                    print(f'\tKey: {key}')
                    print(f'\tDecoded: {self.cipher_func(word, key)}\033[0m')


    def solve(self):
        '''
        Try every single valid word as a key, reporting which results
        have a valid word in themselves.
        '''
        self.print_estimated_run_time()
        self.run_func_across_dict(self.thread_func)
        self.concat_output_files(fname_prefix="one_word_output")
    
    def solve_two_word_keys(self):
        '''
        Try every single combination of two valid words as a key, 
        reporting which results have a valid word in themselves.
        '''
        self.print_estimated_run_time(True)
        self.run_func_across_dict(self.thread_func_two_word_keys)
        self.concat_output_files()
