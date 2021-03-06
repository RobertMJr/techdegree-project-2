import os
import string
from ciphers import Cipher
from caesar import Caesar
from keywords import Keyword
from affine import Affine
from atbash import Atbash


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_keys():
    """
    Ensures user chooses correct alpha and magnitude keys.
    Returns a tuple containing the alpha key and the magnitude.
    """
    coprime = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    alpha_key = 0.1
    while alpha_key not in coprime:
        alpha_key = input('Choose the first key. Must be a coprime'
                          ' of 26.  \n')
        try:
            alpha_key = int(alpha_key)
        except ValueError:
            print('This only works with integers. \n')
    while True:
        magnitude = input('Chose the magnitude key, must be a number. \n')
        try:
            magnitude = int(magnitude)
            break
        except ValueError:
            print('This only works with integers. \n')
    return alpha_key, magnitude


def get_keyword():
    """
    Ensures user chooses a valid keyword - contains alphabetic characters only.
    Returns the keyword so long as it is made of alphabetic characters only.
    """
    while True:
        keyword_choice = input("Type in your keyword (letters only): \n")
        if keyword_choice.isalpha():
            return keyword_choice


def yes_or_no():
    """
    Used for encryption.
    Returns user input once it ensures it is an Yes or a No
    """
    while True:
        user_choice = input('Do you want the output to be displayed in blocks of 5? (Y/N) \n')
        if user_choice.upper() == 'Y':
            return user_choice.upper()
        elif user_choice.upper() == 'N':
            return user_choice.upper()


def y_o_n():
    """
    Used for decryption.
    Returns user input once it ensures it is an Yes or a No
    """
    while True:
        user_choice = input('Was your cipher text returned in blocks of 5? (Y/N) \n')
        if user_choice.upper() == 'Y':
            return user_choice.upper()
        elif user_choice.upper() == 'N':
            return user_choice.upper()


def repeat():
    """
    Checks user input to see if he wants to repeat an action.
    If user input is equal to 'Y', exits and repeats the action.
    If user input is equal to 'N', stops everything and exits the program completely.
    """
    while True:
        x_val = input('Do you want to encrypt or decrypt again? (Y/N) \n')
        if x_val.upper() == 'Y':
            print('')
            x = True
            break
        elif x_val.upper() == 'N':
            x = False
            break
    if not x:
        exit()


def play():
    """
    Asks the user what cipher he wants to use,
    in order to encrypt or decrypt a text message.
    Gives user the option to return the cipher text in 5 characters blocks.
    Asks user for different input based on cipher selection.
    Adds a onetime pad as an additional security layer.
    If encrypting:
    Returns cipher text encrypted with the chosen cipher and onetime pad.
    If decrypting:
    Returns text decrypted with the chosen cipher and onetime pad.
    """
    working = True
    cipher_choice = True
    enc_dec = True
    letters = string.ascii_uppercase
    while working:
        clear_screen()
        print("This is the Secret Messages project for the Treehouse Techdegree. \n"
              "These are the current available ciphers: \n"
              "- Affine \n"
              "- Atbash \n" 
              "- Caesar \n"
              "- Keyword \n"
              "- Type (Q) to quit. \n")
        while cipher_choice:
            choice = input("Type the name of the cipher would you like to use? \n")
            if choice.upper() == 'Q':
                exit()
            elif choice.upper() == 'AFFINE':
                cipher = Affine()
                break
            elif choice.upper() == 'ATBASH':
                cipher = Atbash()
                break
            elif choice.upper() == 'CAESAR':
                cipher = Caesar()
                break
            elif choice.upper() == 'KEYWORD':
                cipher = Keyword()
                break
            else:
                print('Type the name of any available cipher. \n')

        user_text = input('What is your message?(Letters only) \n')

        while enc_dec:
            e_or_d = input('Are we going to encrypt or decrypt? \n')
            if e_or_d.upper() == 'ENCRYPT' and isinstance(cipher, Affine):
                alpha, beta = get_keys()
                ot_pad  = input('Type your one time pad. \n')
                ot_val = cipher.one_time_pad(user_text, ot_pad)
                value = cipher.encrypt(ot_val,alpha, beta)
                block_choice = yes_or_no()
                if block_choice.upper() == 'Y':
                    value = cipher.add_padding(value)
                    print(value + '\n')
                    repeat()
                    break
                else:
                    print(value + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'DECRYPT' and isinstance(cipher, Affine):
                alpha, beta = get_keys()
                ot_pad  = input('Type your one time pad, must be the same used for encrypting. \n')
                block_choice = y_o_n()
                if block_choice.upper() == 'Y':
                    no_block = cipher.remove_padding(user_text)
                    value = cipher.decrypt(no_block, alpha, beta)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
                else:
                    value = cipher.decrypt(user_text, alpha, beta)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'ENCRYPT' and isinstance(cipher, Atbash):
                ot_pad = input('Type your one time pad. \n')
                ot_val = cipher.one_time_pad(user_text, ot_pad)
                value = cipher.encrypt(ot_val)
                block_choice = yes_or_no()
                if block_choice.upper() == 'Y':
                    value = cipher.add_padding(value)
                    print(value + '\n')
                    repeat()
                    break
                else:
                    print(value + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'DECRYPT' and isinstance(cipher, Atbash):
                ot_pad = input('Type your one time pad, must be the same used for encrypting. \n')
                block_choice = y_o_n()
                if block_choice.upper() == 'Y':
                    no_block = cipher.remove_padding(user_text)
                    value = cipher.decrypt(no_block)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
                else:
                    value = cipher.decrypt(user_text)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'ENCRYPT' and isinstance(cipher, Caesar):
                ot_pad = input('Type your one time pad. \n')
                ot_val = cipher.one_time_pad(user_text, ot_pad)
                value = cipher.encrypt(ot_val)
                block_choice = yes_or_no()
                if block_choice.upper() == 'Y':
                    value = cipher.add_padding(value)
                    print(value + '\n')
                    repeat()
                    break
                else:
                    print(value + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'DECRYPT' and isinstance(cipher, Caesar):
                ot_pad = input('Type your one time pad, must be the same used for encrypting. \n')
                block_choice = y_o_n()
                if block_choice.upper() == 'Y':
                    no_block = cipher.remove_padding(user_text)
                    value = cipher.decrypt(no_block)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
                else:
                    value = cipher.decrypt(user_text)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'ENCRYPT' and isinstance(cipher, Keyword):
                ot_pad = input('Type your one time pad. \n')
                keyword_choice = get_keyword()
                ot_val = cipher.one_time_pad(user_text, ot_pad)
                value = cipher.encrypt(ot_val, keyword_choice)
                block_choice = yes_or_no()
                if block_choice.upper() == 'Y':
                    value = cipher.add_padding(value)
                    print(value + '\n')
                    repeat()
                    break
                else:
                    print(value + '\n')
                    repeat()
                    break
            elif e_or_d.upper() == 'DECRYPT' and isinstance(cipher, Keyword):
                ot_pad = input('Type your one time pad, must be the same used for encrypting. \n')
                block_choice = y_o_n()
                keyword_choice = get_keyword()
                if block_choice.upper() == 'Y':
                    no_block = cipher.remove_padding(user_text)
                    value = cipher.decrypt(no_block, keyword_choice)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break
                else:
                    value = cipher.decrypt(user_text, keyword_choice)
                    ot_val = cipher.one_time_pad(value, ot_pad, encrypt=False)
                    print(ot_val + '\n')
                    repeat()
                    break


if __name__ == '__main__':
    play()