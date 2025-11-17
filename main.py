from BruteForce import BruteForce
from DictCompare import DictCompare
from WordDictionary import WordDictionary
from vigenere import decode_vig, decode_beaufort, decode_variant_beaufort, reverse_vig

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
encoded_text = "Ihgvq mbuvhmafvobac rvon. Jhfxvqnl xy xmkw gwa cotfibf qt aaw hnud."

# Main
word_dict = WordDictionary()

brute_force = BruteForce(encoded_text, word_dict, decode_vig, 4, separators=(6, 7, 12), starting_key_part=keys_1)
brute_force.solve()

# dict_compare = DictCompare(encoded_text, word_dict, decode_vig, min_valid_word_length=6, keys_to_test=keys_1)
# dict_compare.solve()
