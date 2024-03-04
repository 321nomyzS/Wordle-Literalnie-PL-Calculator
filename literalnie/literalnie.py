from literalnie.models import FiveLetterWords
from morfeusz2 import Morfeusz

alfabet = "aąbcćdeęfghijklłmnńoóprsśtuwyzżź"


def literalnie_cheat(not_in_word, somewhere_in_word, in_specific_place, not_in_specific_place):
    words_base = FiveLetterWords.objects.all()

    # Filtering words_base | part 1
    for letter in not_in_word:
        words_base = words_base.exclude(word__icontains=letter)

    # Filtering words_base | part 2
    for letter in somewhere_in_word:
        words_base = words_base.filter(word__icontains=letter)

    result_words = []
    for obj in words_base:
        word = obj.word

        temp_sum = 0
        for i in range(len(word)):
            # Filtering words_base | part 3
            if in_specific_place[i] != '_':
                if in_specific_place[i] != word[i]:
                    break

            # Filtering words_base | part 4
            if len(not_in_specific_place[i]) > 0:
                if word[i] in not_in_specific_place[i]:
                    break

            temp_sum += 1

        if temp_sum >= 5:
            result_words.append(word)

    return result_words


def words_tier_level(words):
    alfabetTier = 'źńfćśżóąhęgbłljwumpdkyctsqrnzeoia'
    tier = []
    for word in words:
        sum_score = 0
        for letter in list(set(word)):
            sum_score += alfabetTier.find(letter) + 1
        tier.append([sum_score, word])

    tier.sort(reverse=True)
    tier = tier[:300]

    for word_tier in tier:
        morfeusz = Morfeusz()
        analyses = morfeusz.analyse(word_tier[1])

        if is_nominative(analyses):
            word_tier[0] += 30

        if is_singular(analyses):
            word_tier[0] += 10

    tier.sort(reverse=True)

    return tier[:100]


def is_nominative(analyses):
    for analyse in analyses:
        if "nom" in analyse[2][2]:
            return True

    return False


def is_singular(analyses):
    for analysis in analyses:
        if "sg" in analysis[2][2]:
            return True

    return False

def not_in_word_error_check(not_in_word):
    for i in range(len(not_in_word)):
        if len(not_in_word[i]) != 1:
            result = "Błąd w formule (1): Litery należy oddzielać spacją"
            return result

        if not_in_word[i].lower() not in alfabet:
            result = "Błąd w formule (1): Można wpisywać tylko litery z polskiego alfabetu: 'aąbcćdeęfghijklłmnńoóprsśtuwyzżź'"
            return result

    return True


def somewhere_in_word_error_check(somewhere_in_word):
    for i in range(len(somewhere_in_word)):
        if len(somewhere_in_word[i]) != 1:
            result = "Błąd w formule (2): Litery należy oddzielać spacją"
            return result

        if somewhere_in_word[i].lower() not in alfabet:
            result = "Błąd w formule (2): Można wpisywać tylko litery z polskiego alfabetu: 'aąbcćdeęfghijklłmnńoóprsśtuwyzżź'"
            return result
    return True


def in_specific_place_error_check(in_specific_place):
    for i in range(len(in_specific_place)):
        if len(in_specific_place[i]) != 1:
            result = "Błąd w formule (3): Na każdej pozycji może być tylko jedna pewna litera"
            return result
        if in_specific_place[i].lower() not in alfabet+ "_":
            result = "Błąd w formule (3): Można wpisywać tylko litery z polskiego alfabetu: 'aąbcćdeęfghijklłmnńoóprsśtuwyzżź'"
            return result
    return True


def not_in_specific_place_error_check(not_in_specific_place):
    for i in range(len(not_in_specific_place)):
        position = not_in_specific_place[i]
        for j in range(len(position)):
            if len(position[j]) != 1:
                result = "Błąd w formule (4): Na każdej pozycji może być tylko jedna pewna litera"
                return result

            if position[j].lower() not in alfabet + "_":
                result = "Błąd w formule (4): Można wpisywać tylko litery z polskiego alfabetu: 'aąbcćdeęfghijklłmnńoóprsśtuwyzżź'"
                return result
    return True


def add_word_error_check(word):
    if len(word) > 5:
        result = "Słowo jest za długie. Musi być 5 literowe."
        return result

    if len(word) < 5:
        result = "Słowo jest za krótkie. Musi być 5 literowe."
        return result

    for letter in word:
        if letter not in alfabet:
            result = "Słowo musi zawierać wyłączeni litery z polskiego alfabetu."
            return result

    if FiveLetterWords.objects.filter(word=word).exists():
        result = "Takie słowo już istnieje w bazie"
        return result

    return True