__date__ = "2023/02/04"
__license__ = "MIT"
__version__ = "1.0"

"""
Checks if a character is a vowel based on Tagalog language rules.

Attributes:
    char {string} -- the single-character string to be checked

Returns:
    bool -- true if the string is a vowel; otherwise, false
"""
def is_vowel(char):
    vowels = ["a", "e", "i", "o", "u"]
    if char.lower() in vowels:
        return True
    return False


"""
Checks if a character is a consonant based on Tagalog language rules.

Attributes:
    char {string} -- the single-character string to be checked

Returns:
    bool -- true if the string is a consonant; otherwise, false
"""
def is_consonant(char):
    # note: '^' represents 'ng'
    consonants = [
        "^",
        "b",
        "c",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        "m",
        "n",
        "ñ",
        "p",
        "q",
        "r",
        "s",
        "t",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    if char.lower() in consonants:
        return True
    return False


"""
Converts all instances of the string "ng" into the single-character representation "^".

Attributes:
    word {string} -- the word to be processed

Returns:
    string -- the word with all its "ng" converted into "^" (if applicable)
"""
def preprocess_ng(word):
    if not "ng" in word:
        return word

    return word.replace("ng", "^")


"""
Converts all instances of the string "^" into "ng" in a list of string-based syllables.

Attributes:
    syllables {list} -- the list of syllables to be processed

Returns:
    list -- the list of syllables with all its "^" converted into "ng" (if applicable)
"""
def postprocess_ng(syllables):
    new_syllables = []

    for s in syllables:
        if not "^" in s:
            new_syllables.append(s)
        else:
            new_syllables.append(s.replace("^", "ng"))

    return new_syllables


"""
Converts each vowel into the character 'V' and each consonants into the character 'C'. 
Example: aanhin -> VVCCVC, ngayon -> CCVCVC

Attributes:
    word {list} -- the word to be converted

Returns:
    string -- the pattern generated
"""
def get_pattern(word):
    pattern = ""
    for letter in word:
        if is_vowel(letter):
            pattern += "V"
        elif is_consonant(letter):
            pattern += "C"
        else:
            pattern += letter
    return pattern


"""
Extracts the syllables of a given Tagalog word. 

Attributes:
    word {string} -- the Tagalog word to be syllabized

Returns:
    {list} -- the list of extracted syllables
"""
def get_syllables(word):
    # SPECIAL CASE: if word is exactly 'ng'
    if word == "ng":
        return [word]

    # convert representations of letters 'ng' into '^'
    word = preprocess_ng(word)
    # get the vowel-consonant pattern of the word
    pattern = get_pattern(word)

    # go through each letter in pattern
    result = []
    i = 0
    while i < len(pattern):
        # VC pattern; exempt VCV cases (i.e., nguYAIn, paANO, maaARI)
        if pattern[i:].startswith("VC") and not pattern[i:].startswith("VCV"):
            result.append(word[i] + word[i + 1])
            i += 1
        # V pattern
        elif pattern[i:].startswith("V"):
            result.append(word[i])
        # CVC pattern; exempt CVCV - this is for another case (i.e., TUMAkbo, NAPAkalakas, PAMAntasang)
        elif pattern[i:].startswith("CVC") and not pattern[i:].startswith("CVCV"):
            result.append(word[i] + word[i + 1] + word[i + 2])
            i += 2
        # CV pattern
        elif pattern[i:].startswith("CV"):
            result.append(word[i] + word[i + 1])
            i += 1
        # if all else fails
        else:
            result.append(word[i])

        i += 1

    # return resulting syllabication along with original word
    return postprocess_ng(result)