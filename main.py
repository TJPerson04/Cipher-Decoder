from BruteForce import BruteForce
from DictCompare import DictCompare
from WordDictionary import WordDictionary
from vigenere import decode_vig, decode_beaufort, decode_variant_beaufort, reverse_vig

## This is the encoded text. The current value is the text I was trying to decode,
## feel free to change this to whatever your text is.
encoded_text = "Ihgvq mbuvhmafvobac rvon. Jhfxvqnl xy xmkw gwa cotfibf qt aaw hnud."

## Initialize a WordDictionary with my dictionary files.
## Change these file paths to change the list of words considered valid.
word_dict = WordDictionary(dictionary_file_paths=["word_lists/words.csv", "word_lists/dnd-monsters.csv", "word_lists/dnd-spells.csv"], small_words_max_length=3)

#### Brute force method. ####
## This will work best if the key is either small or
## does not contain a valid word. As you test more characters with this
## method, it will take exponentially more time to complete.
##
## Uncomment the following lines to try and find your key through brute force.
# brute_force = BruteForce(encoded_text, decode_vig, 4, word_dict=word_dict, separators=(6, 7, 12), num_cores=16)
# brute_force.solve()

#### Dictionary compare method. ####
## This works best if the key includes valid words.
##
## DictCompare.quick_solve will try and reverse engineer keys that give valid results,
## then check those keys for valid words themselves. This works especially well if one
## of your encoded words is long. This is the only function that will only log results
## to the console, and NOT a file.
##
## DictCompare.solve will go through every single valid word, testing it out as a key.
## This will only work if the key happens to be a single, real word, but it is comparatively
## very quick to test so it's usually good to start here just in case.
##
## DictCompare.solve_two_word_keys will go through every single combination of two valid words
## and use that combination as the key. This is significantly slower, but the time could be shortened
## by setting the key_to_test property in the DictCompare to word_dict.small_words. This will limit
## the words this will check to smaller words, assuming that if the key is two words combined, that those
## words aren't very long.
##
## To use, first make sure to uncomment the initailization of dict_compare, then uncomment the test you want to run.

dict_compare = DictCompare(encoded_text, decode_vig, word_dict=word_dict, rev_cipher_func=reverse_vig, keys_to_test=word_dict.small_words)
dict_compare.quick_solve(5)
# dict_compare.solve()
# dict_compare.solve_two_word_keys()
