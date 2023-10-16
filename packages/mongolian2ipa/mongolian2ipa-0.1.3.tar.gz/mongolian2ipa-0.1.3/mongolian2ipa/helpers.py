from enum import Enum

vowels = ['а', 'э', 'о', 'ө', 'ү', 'у', 'я', 'ё', 'е', 'ю', 'и']
male_vowels = ['а', 'о', 'у', 'я', 'ё']
female_vowels = ['э', 'ө', 'ү', 'е']


class WordGender(Enum):
    MALE = 1
    FEMALE = 0


def check_male_female_word(word: str) -> WordGender:
    # Check for the presence of specific characters
    if any(char in word for char in male_vowels):
        return WordGender.MALE
    elif any(char in word for char in female_vowels):
        return WordGender.FEMALE
    else:
        return WordGender.FEMALE  # Default to female if none of the characters are found


def check_first_level_vowel(word: str, index: int) -> bool:
    if word[index] not in vowels:
        return False

    for i in range(len(word)):
        c = word[i]

        if c in vowels:
            if i == index:
                return True
            else:
                return False

    return False
