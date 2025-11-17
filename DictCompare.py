from collections.abc import Callable
import os
import time
from WordDictionary import WordDictionary
import threading

class DictCompare:
    def __init__(self, encoded_text: str, word_dict: WordDictionary, cipher_func: Callable[[str, str], str], num_cores: int = 16, min_valid_word_length = 5, separators: tuple[bool, bool, bool] = (4, 6, 12), starting_key_part: list[str]=[""], keys_to_test=None):
        '''
        Will try and solve the given cipher using keys determined from the dictionary of words.\n

        encoded_text: The encoded string of text\n
        word_dict: The associated WordDictionary\n

        cipher_func: The cipher function to call that encodes a given string\n
        num_cores: The number of separate threads to run at once\n
        starting_key_part: If given, this will add the given string to the beginning of each key
        '''
        self.encoded_text = encoded_text
        self.word_dict = word_dict
        self.cipher_func = cipher_func
        self.num_cores = num_cores
        self.min_valid_word_length = min_valid_word_length
        self.separators = separators
        self.starting_key_part = starting_key_part

        if (keys_to_test == None):
            self.keys_to_test = word_dict.all_words
        else:
            self.keys_to_test = keys_to_test
    
    def get_size_of_section(self, start: int, total_length: int):
        length = total_length - start
        return length // self.num_cores
    
    def filter_string(self, text: str, size: int) -> str:
        '''
        Removes all words under size in the string
        '''
        text_ar = text.replace('.', '').split(' ')
        output = ""

        for word in text_ar:
            if (len(word) < size):
                continue

            output += word + " "
        
        output = output.removesuffix(" ")
        return output
    
    def get_estimated_run_time(self):
        startTime = time.time_ns()

        # Run a couple checks and see how long that takes
        for i in range(20):
            word = self.starting_key_part[0] + self.keys_to_test[i]
            decoded_text = self.cipher_func(self.encoded_text, word)
            decoded_text_filtered = self.filter_string(decoded_text, self.min_valid_word_length)
            self.word_dict.contains_valid_word(decoded_text_filtered)

        endTime = time.time_ns()

        timeMult = len(self.starting_key_part) * len(self.keys_to_test) / self.num_cores

        return (endTime - startTime) * timeMult
    
    def print_estimated_run_time(self, is_two_word=False):
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
        # Log start
        print("Starting thread: " + str(thread_index))
        
        # Check all words in section
        with open(f'one_word_output_{thread_index}.txt', 'a') as out_file:
            for keyStart in self.starting_key_part:
                for i in range(end - start):
                    index = start + i
                    word = keyStart + self.keys_to_test[index]
                    decoded_text = self.cipher_func(self.encoded_text, word)
                    decoded_text_filtered = self.filter_string(decoded_text, self.min_valid_word_length)
                    ### TEMP
                    decoded_text_arr = decoded_text_filtered.split(' ')
                    decoded_text_filtered = ""
                    for i in range(len(decoded_text_filtered)):
                        if i > 1:
                            decoded_text_filtered += decoded_text_arr[i]
                    ### END TEMP
                    if (self.word_dict.contains_valid_word(decoded_text_filtered)):
                        output_text = f'key: {word} | text: {decoded_text}\n'
                        print(output_text)
                        out_file.write(output_text)
            
                    # if (i % 1000 == 0):
                        # print(f'Thread {thread_index} checking key {word}')
        print(f'Ending thread: {thread_index}')
    
    def thread_func_two_word_keys(self, start: int, end: int, thread_index: int):
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

    def run_func_across_dict(self, func):
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
        the length of the valid word in the given string
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
        if (not is_valid[0]):
            return
    
        output_text = f'key: {word} | text: {decoded_text}\n'
    
        file_1.write(output_text)

        if (is_valid[1]):
            print("-------")
            print(output_text)
            file_2.write(output_text)
    
        if (is_valid[2]):
            file_3.write(output_text)

    def solve(self):
        self.print_estimated_run_time()
        self.run_func_across_dict(self.thread_func)
        self.concat_output_files(fname_prefix="one_word_output")
    
    def solve_two_word_keys(self):
        self.print_estimated_run_time(True)
        self.run_func_across_dict(self.thread_func_two_word_keys)
        self.concat_output_files()
