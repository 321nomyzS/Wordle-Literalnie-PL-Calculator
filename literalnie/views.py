from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render, redirect
from literalnie.literalnie import *
from django.urls import reverse


@requires_csrf_token
def literalnie(request):
    if request.method == "POST":
        # Getting data from request
        option_1 = request.POST["option-1"]
        option_2 = request.POST["option-2"]

        option_3_1 = request.POST["option-3-1"]
        option_3_2 = request.POST["option-3-2"]
        option_3_3 = request.POST["option-3-3"]
        option_3_4 = request.POST["option-3-4"]
        option_3_5 = request.POST["option-3-5"]

        option_4_1 = request.POST["option-4-1"]
        option_4_2 = request.POST["option-4-2"]
        option_4_3 = request.POST["option-4-3"]
        option_4_4 = request.POST["option-4-4"]
        option_4_5 = request.POST["option-4-5"]

        words_list = eval(request.POST["words-list"])

        # Set default content
        content = {
            "option_1": option_1,
            "option_2": option_2,
            "option_3_1": option_3_1,
            "option_3_2": option_3_2,
            "option_3_3": option_3_3,
            "option_3_4": option_3_4,
            "option_3_5": option_3_5,
            "option_4_1": option_4_1,
            "option_4_2": option_4_2,
            "option_4_3": option_4_3,
            "option_4_4": option_4_4,
            "option_4_5": option_4_5,
            "words_list": words_list,
        }

        # Check for errors
        not_in_word = option_1.split()
        error = not_in_word_error_check(not_in_word)
        if error is not True:
            content["error_mess_1"] = error
            return render(request, 'literalnie/literalnie.html', content)

        somewhere_in_word = option_2.split()
        error = somewhere_in_word_error_check(somewhere_in_word)
        if error is not True:
            content["error_mess_1"] = error
            return render(request, 'literalnie/literalnie.html', content)

        in_specific_place = ['_', '_', '_', '_', '_']
        if len(option_3_1.split()) > 0: in_specific_place[0] = option_3_1.split()[0]
        if len(option_3_2.split()) > 0: in_specific_place[1] = option_3_2.split()[0]
        if len(option_3_3.split()) > 0: in_specific_place[2] = option_3_3.split()[0]
        if len(option_3_4.split()) > 0: in_specific_place[3] = option_3_4.split()[0]
        if len(option_3_5.split()) > 0: in_specific_place[4] = option_3_5.split()[0]
        error = in_specific_place_error_check(in_specific_place)
        if error is not True:
            content["error_mess_1"] = error
            return render(request, 'literalnie/literalnie.html', content)

        not_in_specific_place = [[], [], [], [], []]
        not_in_specific_place[0] += option_4_1.split()
        not_in_specific_place[1] += option_4_2.split()
        not_in_specific_place[2] += option_4_3.split()
        not_in_specific_place[3] += option_4_4.split()
        not_in_specific_place[4] += option_4_5.split()
        error = not_in_specific_place_error_check(not_in_specific_place)
        if error is not True:
            content["error_mess_1"] = error
            return render(request, 'literalnie/literalnie.html', content)

        words = literalnie_cheat(not_in_word, somewhere_in_word, in_specific_place, not_in_specific_place)
        tier_list = words_tier_level(words)
        content["words_list"] = tier_list
        return render(request, 'literalnie/literalnie.html', content)

    words = literalnie_cheat([], [], ['_', '_', '_', '_', '_'], [[], [], [], [], []])
    tier_list = words_tier_level(words)
    content = {
        "words_list": tier_list,
        "error_mess_2": request.GET.get("error_mess_add", "")
    }

    return render(request, 'literalnie/literalnie.html', content)


def literalnie_delete_word(request, word):
    if request.method == 'GET':
        FiveLetterWords.objects.filter(word=word).delete()
    return redirect('literalnie')


def literalnie_add_word(request, word=""):
    if request.method == 'GET':
        word = str(word).lower()
        error = add_word_error_check(word)

        if error is not True:
            url = f"{reverse('literalnie')}?error_mess_add={error}"
            return redirect(url)

        print(f"Słowo {word} zostało przyjęte")
        five_letter_word = FiveLetterWords(word=word)
        five_letter_word.save()
    return redirect('literalnie')


def literalnie_instruction(request):
    return render(request, 'literalnie/literalnie_instruction.html')


