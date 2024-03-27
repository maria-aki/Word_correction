from tqdm import tqdm
from spellchecker import SpellChecker

ITERATIONS = 100000
DICTIONARY_FILE = "dict.txt"
QUESTIONS_FILE_NAME = "queries.txt"
OUTPUT_FILE_NAME = "answers_words_v.6.txt"


def make_dict(filename: str):
    dict_file = open(filename, "r")
    dictionary = dict()
    for word in dict_file:
        word = word.strip()
        dictionary[word] = dictionary.get(word, 0) + 1
    dict_file.close()
    return dictionary


def make_output_data(flag: int, word: str, first: str, second: str):
    output_string = ""
    if flag == 0:
        output_string = word + " " + '0' + '\n'
    elif flag == 1:
        output_string = word + " " + '1' + " " + first + '\n'
    elif flag == 2:
        output_string = word + " " + '2' + " " + first + " " + second + '\n'
    elif flag == 3:
        output_string = word + " " + "3+" + '\n'
    return output_string


if __name__ == "__main__":

    pbar = tqdm(total=ITERATIONS)
    spell = SpellChecker(language='ru')
    input_file = open(QUESTIONS_FILE_NAME, "r")
    dictionary = make_dict(DICTIONARY_FILE)

    for damaged_word in input_file:
        damaged_word = damaged_word.strip()
        word_status = 3
        first_correction = ""
        second_correction = ""
        if dictionary.get(damaged_word, 0) > 0:
            word_status = 0
        else:
            array_of_first_correction = spell.edit_distance_1(damaged_word)
            for first_variant in array_of_first_correction:
                if dictionary.get(first_variant, 0) > 0:
                    word_status = 1
                    first_correction = first_variant
                    break
            if word_status != 1:
                for first_variant in array_of_first_correction:
                    array_of_second_correction = spell.edit_distance_1(first_variant)
                    for second_variant in array_of_second_correction:
                        if dictionary.get(second_variant, 0) > 0:
                            first_correction = first_variant
                            second_correction = second_variant
                            word_status = 2
                            break
                    if word_status == 2:
                        break

        with open(OUTPUT_FILE_NAME, "a+") as output:
            strn = make_output_data(word_status, damaged_word, first_correction, second_correction)
            output.write(strn)
            pbar.update(1)

    input_file.close()
    pbar.close()
