# ******************************************************************************
# Author:           Proxima-L3
# Date:             April 29, 2022
# Project Name:     Anagram Alias Assistant Program (AAAP) v2.0
# Update Summary:	Added a GUI via Tkinter framework. Code had to be practically
# 					rebuilt; multiple functions were added, while others were changed
# 					and the main function was drastically overhauled with most of
# 					the program's gui/widget code. Several relatively minor
# 					changes to code's organization to more accurately implement
# 					python standard practices.
# Description:      A program that uses web scraping to make lists of names
#                   from websites and uses them to help the user create anagrams.
# Goal/purpose:     Learn how to use web scraping, practice searching for and
#                   using random libraries/modules/functions that solve a problem
#                   in my algorithm, refresh my programming skills after being
#                   away from it for over a year, create a tool that has potential
#                   use in the future, learn how to make GUIs for programs, learn
# 					how to use version control directly through IDE via git/github,
# 					exercise resourcefulness via ability to reference/read
# 					documentation efficiently, try out the practice of making
# 					wireframes, gain better understanding of how to organize my
# 					program file,
# Sources:          (https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures)
#                   (https://www.anagrammer.com/)
#                   (https://www.coolgenerator.com/anagram-name-generator)
#
#                   (https://www.askpython.com/python/string/remove-character-from-string-python)
#                   (https://www.tutorialspoint.com/python-inserting-item-in-sorted-list-maintaining-order)
#                   (https://www.w3schools.com/python/python_tuples_unpack.asp)
#                   (https://www.educative.io/edpresso/how-to-find-the-length-of-a-string-in-python)
# 					(https://tkdocs.com/tutorial/onepage.html)
#                   (https://www.pythonpool.com/python-check-if-string-is-integer/)
#                   (Minimal review from one of my Udemy courses)
# 					(https://softwareengineering.stackexchange.com/questions/3199/what-version-naming-convention-do-you-use?newreg=986f6d522b3d47478c0bef9677b24198)
# 					(https://tkdocs.com/tutorial/onepage.html)
# 					(https://www.tutorialspoint.com/python/tk_frame.htm)
# 					(https://www.youtube.com/watch?v=dBMHuIWbF_k)
# 					(https://www.youtube.com/watch?v=RGOj5yH7evk)
# 					(https://www.youtube.com/watch?v=KdoOm3xo8X0&t=547s)
# 					(https://stackoverflow.com/questions/2307464/what-is-the-difference-between-root-destroy-and-root-quit)
# 					(https://www.youtube.com/watch?v=LTVvHObxc4E)
# 					(https://www.youtube.com/watch?v=_auZ8TTkojQ)
# 					(https://stackoverflow.com/questions/48494695/how-to-set-the-color-of-the-circle-and-the-selection-dot-of-a-radio-button)
# 					(https://www.javatpoint.com/python-tkinter-text)
# 					(https://docs.python.org/3.7/library/tkinter.scrolledtext.html#tkinter.scrolledtext.ScrolledText)
# 					(https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/)
# 					(https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter)
# 					(https://stackoverflow.com/questions/36293437/tkinter-run-function-after-frame-is-displayed)
# 					(https://stackoverflow.com/questions/40684739/why-do-tkinters-radio-buttons-all-start-selected-when-using-stringvar-but-not-i)
# ******************************************************************************


import requests
import bs4
import lxml
import bisect
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time


# This function initializes the root window of the program and customizes it accordingly with methods
def initialize_main_window(win_name):
    win_name.title("AAAP")
    win_name.geometry('850x550')
    win_name.resizable(False, False)
    win_name.configure(background="#282828")
    win_name.iconbitmap('project_assets/escaping_sideways_YAl_icon.ico')


# This function switches to a new frame and changes the window/executes different code depending on which frame is next
def change_screen(current_screen_name, next_screen_name, win_name, anagram_entered, rbutton_choice,
                  common_letters_amount):
    current_screen_name.pack_forget()
    next_screen_name.pack()

    screen_packed = f'{next_screen_name}'

    if screen_packed == '.!frame2':
        # clear user input and resize root window
        anagram_entered.delete(0, 'end')
        anagram_entered.focus()
        rbutton_choice.set('null')
        common_letters_amount.delete(0, 'end')
        win_name.geometry('850x550')
    elif screen_packed == '.!frame5':
        # resize root window and quit the program after 2 seconds
        win_name.geometry('650x450')
        next_screen_name.update()
        time.sleep(2)
        win_name.quit()
    else:
        win_name.geometry('850x550')


# Temporary function that will be replaced with a file call. The external file will essentially be a database of all the collected names/figures/etc that have been scraped from websites
def temp_wiki_scrape_list_func():
    url_used = "https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures"

    # assigning the html page to a variable via get request
    wiki_request1 = requests.get(url_used)

    # using beautiful soup to make raw html code organized
    wiki_soup = bs4.BeautifulSoup(wiki_request1.text, 'lxml')

    # making a list of all a tags in the html document
    raw_atag_list = wiki_soup.select('a')

    keyword_gibberish_list = ['', ' ', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h',
                              'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', "'", '`', '~', '!', '@', '#', '$', '%',
                              '^', '&', '*', '(', ')', '-', '=', '_', '+', '[', ']', '{', '}', '|', ';', ':', '"', ',',
                              '.', '/', '<', '>', '?']
    filtered_atag_list = []
    int_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    has_int = False

    # for loop with several if statements that filter out the unwanted things in my code, specifically names with ints, single letters, and repeats of names
    for item in raw_atag_list:
        item = item.getText()

        for num in int_list:
            if str(num) in item:
                has_int = True
                break
            else:
                has_int = False

        if has_int:
            continue
        elif item.lower() in keyword_gibberish_list:
            continue
        elif item in filtered_atag_list:
            continue
        else:
            bisect.insort(filtered_atag_list, item)

    return url_used, filtered_atag_list


# # will use this when .grid is replaced with .place ... function turns radio button choice for adv ops into a dropdown
# def adv_ops_toggle(label_name, entry_name):
#     if
#     label_name.grid_forget()
#     entry_name.grid_forget()


# This function takes in list of names, the pre_anagram, and the variables representing the choices made by the user in the advanced options section and uses that information to generate a list of possible anagrams/aliases
def anagram_generator(name_list, preanagram, common_letters_amount):
    number_of_common_letters_list = []
    perfect_anagram_list = []
    adv_op0_anagram_list = []

    # for loop used as outer layer of nested for loop to iterate through list_of_names list and create another list that holds the number of letters that the pre_anagram and each name in list_of_names have in common. (the index location of each item in list_of_names and each item in number_of_common_letters_list should be the same... although, in the future, we may want to figure out how to use a dictionary to do this whole process)
    for name in name_list:

        name_for_iterating = name.replace(' ', '').lower()
        pre_anagram_for_iterating = preanagram.replace(' ', '').lower()
        letter_counter = 0

        # nested for loop used for checking how many letters pre_anagram and the current name (from list of names) have in common
        for letter in pre_anagram_for_iterating:
            if letter in name_for_iterating:
                pre_anagram_for_iterating = pre_anagram_for_iterating.replace(letter, '', 1)
                letter_counter += 1
                name_for_iterating = name_for_iterating.replace(letter, '', 1)
            else:
                pass

        # this line adds how many common letters there are into a list that will be used later to find/index names (from the list_of_names list) that meet certain guidelines to be put into another list that will be shown to the user as possible viable anagrams/aliases
        number_of_common_letters_list.append(letter_counter)

        # this line takes the current "name string" being iterated through, gets rid of its spaces, and compares its remaining length to the remaining length of preanagram. if they are the same, it adds the current name being iterated through to a perfect anagram list
        if name_for_iterating == '' and pre_anagram_for_iterating == '':
            perfect_anagram_list.append(name)
        else:
            pass

    # (actual code that makes and returns the list of anagrams/aliases) - conditional statement that checks if user wanted perfect anagrams only and if they didn't, a new list of all the names with the number of common letters or more is created then returned
    if common_letters_amount.isdigit():

        index_counter = 0

        for item in number_of_common_letters_list:
            if item >= int(common_letters_amount):
                adv_op0_anagram_list.append(name_list[index_counter])
            else:
                pass
            index_counter += 1

        return adv_op0_anagram_list

    else:
        return perfect_anagram_list


# This function checks to see if user input was entered correctly, runs the anagram generator, and changes the relevant information on the results screen
def check_user_input_and_results_generator(anagram_entered, radio_button_choice, common_letters_widget,
                                           current_screen_name, next_screen_name, win_name, pre_anagram_result_text,
                                           common_letters_amount_result_text, num_of_anagrams_text, results_box,
                                           name_list):
    # checks to see if anagram box is filled with any letters and displays error message if it isn't
    if anagram_entered.get().strip() == '':
        print('user must enter some text in anagram box')
    # checks to see if no advanced options were chosen and continues the program accordingly
    elif radio_button_choice.get() != 'y':
        # inserts user's pre-anagram on gui widget
        pre_anagram_result_text.set(f'Word/Phrase: {anagram_entered.get()}')
        # inserts blank spot because common letters option was not chosen
        common_letters_amount_result_text.set('')
        # anagram generator
        anagram_list = anagram_generator(name_list, anagram_entered.get(), common_letters_widget.get())
        # inserts number of anagrams found on gui widget
        num_of_anagrams_text.set(f'Anagrams Found: {len(anagram_list)}')
        # code that clears and makes the text box read only
        results_box.configure(state='normal')
        results_box.delete('1.0', 'end')
        # for loop that iterates through the anagram list and adds each anagram result to the text box
        for item in anagram_list:
            results_box.insert('end', item + '\n')
        results_box.configure(state='disabled')
        # change to results screen
        win_name.geometry('850x700')
        current_screen_name.pack_forget()
        next_screen_name.pack()
    else:
        if radio_button_choice.get() == 'y':
            # inserts user's pre-anagram on gui widget
            pre_anagram_result_text.set(f'Word/Phrase: {anagram_entered.get()}')
            # inserts number of common letters chosen by user
            common_letters_amount_result_text.set(f'Common Letters: {common_letters_widget.get()}')
            # anagram generator
            anagram_list = anagram_generator(name_list, anagram_entered.get(), common_letters_widget.get())
            # inserts number of anagrams found on gui widget
            num_of_anagrams_text.set(f'Anagrams Found: {len(anagram_list)}')
            # code that clears and makes the text box read only
            results_box.configure(state='normal')
            results_box.delete('1.0', 'end')
            # for loop that iterates through the anagram list and adds each anagram result to the text box
            for item in anagram_list:
                results_box.insert('end', item + '\n')
            results_box.configure(state='disabled')
            # change to results screen
            win_name.geometry('850x700')
            current_screen_name.pack_forget()
            next_screen_name.pack()
        else:
            # might add this print statement as an on-screen message if I ever decide to convert all the .grid methods to .place
            print('user must enter an integer in common letters option')


# This function ties all other functions together to make one coherent program
def main():
    url_used, list_of_names = temp_wiki_scrape_list_func()
    # might need this in future when more options are added: adv_op_list = []

    # GUI SETUP AND LAYOUT

    # INITIALIZE ROOT WINDOW
    root = Tk()
    initialize_main_window(root)

    # TITLE SCREEN FRAME LAYOUT
    title_screen_frame = Frame(root, bg='#282828')
    Label(title_screen_frame,
          text="Anagram Alias Assistant\nProgram\n(AAAP)",
          font=('ubuntu bold', 35),
          bg='#282828',
          fg='#33ff33',
          anchor=CENTER).grid(row=0, column=0, ipady=90)
    title_screen_continue = Button(title_screen_frame,
                                   text="press here to continue...",
                                   font=('ubuntu', 15),
                                   bg='#404040',
                                   fg='#33ff33',
                                   activebackground='#696969',
                                   activeforeground='#33ff33',
                                   anchor=CENTER,
                                   command=lambda: change_screen(title_screen_frame, main_menu_screen_frame, root,
                                                                 anagram_entry, user_input_rbuttons1,
                                                                 common_letters_entry))
    title_screen_continue.grid(row=1, column=0)

    # MAIN MENU SCREEN FRAME LAYOUT
    main_menu_screen_frame = Frame(root, bg='#282828')
    # spacer between rest of program widgets and edge of program window
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          padx=10,
          pady=15).grid(column=0, row=0)
    # vertical spacer between heading and buttons
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          pady=20).grid(column=0, row=2)
    # vertical spacer between buttons
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          pady=5).grid(column=0, row=4)
    # make anagram option button
    Button(main_menu_screen_frame,
           text="Make an Anagram!",
           font=('ubuntu', 20),
           bg='#404040',
           fg='#33ff33',
           height=1,
           width=16,
           activebackground='#696969',
           activeforeground='#33ff33',
           command=lambda: change_screen(main_menu_screen_frame, user_input_screen_frame, root, anagram_entry,
                                         user_input_rbuttons1, common_letters_entry)).grid(column=1, row=3)
    # quit button
    Button(main_menu_screen_frame,
           text="Quit",
           font=('ubuntu', 20),
           bg='#404040',
           fg='#33ff33',
           height=1,
           width=16,
           activebackground='#696969',
           activeforeground='#33ff33',
           command=lambda: change_screen(main_menu_screen_frame, exit_screen_frame, root, anagram_entry,
                                         user_input_rbuttons1, common_letters_entry)).grid(column=1, row=5)
    # spacer between main menu heading and menu option buttons
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          padx=90).grid(column=2, row=0)
    # main menu heading at top right corner
    Label(main_menu_screen_frame,
          text="MAIN MENU",
          font=('ubuntu bold', 35),
          bg='#282828',
          fg='#33ff33').grid(column=3, row=1)
    # horizontal end zone spacer
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          padx=200).grid(column=20, row=0)
    # vertical end zone spacer
    Label(main_menu_screen_frame,
          text="",
          bg='#282828',
          pady=200).grid(column=0, row=20)

    # USER INPUT SCREEN FRAME LAYOUT
    user_input_screen_frame = Frame(root, bg='#282828')
    # spacer between rest of program widgets and edge of program window
    Label(user_input_screen_frame,
          text="",
          bg='#282828',
          padx=25,
          pady=15).grid(column=0, row=0)
    # spacer between adv ops and menu button
    Label(user_input_screen_frame,
          text="",
          bg='#282828',
          pady=130).grid(column=0, row=5)
    # user entry anagram box subtitle
    Label(user_input_screen_frame,
          text="Enter word or phrase to be anagrammed:",
          font=('ubuntu', 20),
          bg='#282828',
          fg='#33ff33').grid(column=1, row=1, columnspan=4, pady=(0, 15))
    # main menu button
    Button(user_input_screen_frame,
           text="<Main Menu",
           font=('ubuntu', 15),
           bg='#404040',
           fg='#33ff33',
           activebackground='#696969',
           activeforeground='#33ff33',
           height=1,
           width=12,
           command=lambda: change_screen(user_input_screen_frame, main_menu_screen_frame, root, anagram_entry,
                                         user_input_rbuttons1, common_letters_entry)).grid(column=1, row=6,
                                                                                           columnspan=2, sticky='W')
    # advanced options choice subtitle
    Label(user_input_screen_frame,
          text="Advanced Options?",
          font=('ubuntu', 15),
          bg='#282828',
          fg='#33ff33').grid(column=2, row=2, columnspan=2, rowspan=2, sticky='W')
    # user entry adv op 1 box subtitle
    common_letters_label = Label(user_input_screen_frame,
                                 text="Common Letters:",
                                 font=('ubuntu', 10),
                                 bg='#282828',
                                 fg='#33ff33')
    common_letters_label.grid(column=2, row=4, pady=(25, 5))
    # user entry adv op 1 box
    common_letters_entry = Entry(user_input_screen_frame,
                                 width=4,
                                 font=('ubuntu', 10),
                                 bg='#696969',
                                 fg='#33ff33',
                                 insertbackground='#33ff33')
    common_letters_entry.grid(column=3, row=4, sticky='W', pady=(25, 5))
    # advanced options choice radio buttons
    user_input_rbuttons1 = StringVar(value='null')
    yes_rbutton = Radiobutton(user_input_screen_frame,
                              text="Yes",
                              font=('ubuntu', 8),
                              bg='#282828',
                              fg='#33ff33',
                              activebackground='#696969',
                              activeforeground='#33ff33',
                              selectcolor='#696969',
                              variable=user_input_rbuttons1,
                              value='y')
    yes_rbutton.grid(column=3, row=2, sticky='NW')
    no_rbutton = Radiobutton(user_input_screen_frame,
                             text="No",
                             font=('ubuntu', 8),
                             bg='#282828',
                             fg='#33ff33',
                             activebackground='#696969',
                             activeforeground='#33ff33',
                             selectcolor='#696969',
                             variable=user_input_rbuttons1,
                             value='n')
    # code snippet for when I decide to implement advanced options toggle feature:
    # command=adv_ops_toggle(user_input_rbuttons1, common_letters_label, common_letters_entry)
    no_rbutton.grid(column=3, row=3, sticky='SW')
    # user entry anagram box
    anagram_entry = Entry(user_input_screen_frame,
                          width=18,
                          font=('ubuntu', 15),
                          bg='#696969',
                          fg='#33ff33',
                          insertbackground='#33ff33')
    anagram_entry.grid(column=5, row=1, padx=5, pady=(0, 15), sticky='W')
    # results button
    Button(user_input_screen_frame,
           text="Results>",
           font=('ubuntu', 15),
           bg='#404040',
           fg='#33ff33',
           activebackground='#696969',
           activeforeground='#33ff33',
           height=1,
           width=12,
           command=lambda: check_user_input_and_results_generator(anagram_entry, user_input_rbuttons1,
                                                                  common_letters_entry, user_input_screen_frame,
                                                                  results_screen_frame, root, pre_anagram,
                                                                  common_letters_amount, anagrams_found,
                                                                  results_list_box, list_of_names)).grid(column=5,
                                                                                                         row=6,
                                                                                                         padx=(120, 0),
                                                                                                         sticky='E')
    # horizontal end zone spacer
    Label(user_input_screen_frame,
          text="",
          bg='#282828',
          padx=200).grid(column=20, row=0)
    # vertical end zone spacer
    Label(user_input_screen_frame,
          text="",
          bg='#282828',
          pady=200).grid(column=0, row=20)

    # RESULTS SCREEN FRAME LAYOUT
    results_screen_frame = Frame(root, bg='#282828', width=850, height=700)
    # results screen labels for upper left corner
    Label(results_screen_frame,
          text="Results",
          font=('ubuntu bold', 25),
          bg='#282828',
          fg='#33ff33').place(x=30, y=20)
    pre_anagram = StringVar()
    Label(results_screen_frame,
          textvariable=pre_anagram,
          font=('ubuntu', 12),
          bg='#282828',
          fg='#33ff33').place(x=45, y=70)
    common_letters_amount = IntVar()
    # might need this code snippet when more menu options are created: adv_op_list.append(common_letters_amount)
    Label(results_screen_frame,
          textvariable=common_letters_amount,
          font=('ubuntu', 12),
          bg='#282828',
          fg='#33ff33').place(x=45, y=90)
    Label(results_screen_frame,
          text=f"Database Used: ({url_used})",
          font=('ubuntu', 12),
          bg='#282828',
          fg='#33ff33').place(x=45, y=110)
    # anagrams found label
    anagrams_found = StringVar()
    Label(results_screen_frame,
          textvariable=anagrams_found,
          font=('ubuntu', 12),
          bg='#282828',
          fg='#33ff33').place(x=30, y=175)
    # anagram results list text box
    results_list_box = ScrolledText(results_screen_frame,
                                    font=('ubuntu', 12),
                                    bg='#323232',
                                    fg='#33ff33',
                                    insertbackground='#33ff33',
                                    bd=1,
                                    height=23,
                                    width=86)
    results_list_box.place(x=25, y=210)
    results_list_box.configure(state='disabled')
    # main menu button
    Button(results_screen_frame,
           text="<Main Menu",
           font=('ubuntu', 15),
           bg='#404040',
           fg='#33ff33',
           activebackground='#696969',
           activeforeground='#33ff33',
           height=1,
           width=12,
           command=lambda: change_screen(results_screen_frame, main_menu_screen_frame, root, anagram_entry,
                                         user_input_rbuttons1, common_letters_entry)).place(x=15, y=645)
    # quit button
    Button(results_screen_frame,
           text="Quit>",
           font=('ubuntu', 15),
           bg='#404040',
           fg='#33ff33',
           activebackground='#696969',
           activeforeground='#33ff33',
           height=1,
           width=12,
           command=lambda: change_screen(results_screen_frame, exit_screen_frame, root, anagram_entry,
                                         user_input_rbuttons1, common_letters_entry)).place(x=695, y=645)

    # EXIT SCREEN FRAME LAYOUT
    exit_screen_frame = Frame(root, bg='#282828', width=850, height=550)
    # goodbye message label
    Label(exit_screen_frame,
          text="Thank you for using\nAAAP",
          font=('ubuntu bold', 35),
          bg='#282828',
          fg='#33ff33').place(x=325, y=180, anchor='center')
    # ending program label 650x450
    Label(exit_screen_frame,
          text="ending program ...",
          font=('ubuntu', 12),
          bg='#282828',
          fg='#33ff33').place(x=325, y=350, anchor='center')

    # will insure program window opens and opens on the title screen when program is run
    title_screen_frame.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
