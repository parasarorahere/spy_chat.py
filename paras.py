#Import statements allows us to use pre-defined variables and functions from other files.
from spy_detail import spy, Spy,ChatMessage,friends
from steganography.steganography import Steganography
from datetime import datetime

#list which has some default status
STATUS_MESSAGES = ['Hey there! i am using spy chat(*_*)', 'Available','Busy','In college','Sleeping','At the work','DND']

#print few strings using single quotes and double quotes
print 'Hello!'
print"what's up"
print'Let\'s  get started'

#String Concatenation. We will use the '+' sybmol to join strings together.
question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? \n"
existing = raw_input(question)


#function to update the new status
def add_status():
    updated_status_message=None
    if spy.current_status_message != None:
        print "Your current status message is " + spy.current_status_message + "\n"
    else:
        print 'You don\'t have any status message currently \n'
     #condition to select or not to select from the older status
    default = raw_input("Do you want to select from the older status (y/n)?\n ")
    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set?\n")
        if len(new_status_message)> 0:
            #add new values to the end of the list using the pre-defined function append
            STATUS_MESSAGES.append(new_status_message)
            updated_status_message = new_status_message
    elif default.upper() == "Y":
        item_position = 1
        #for loop to print all the previously set statuses.
        for message in STATUS_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1
        message_selection = int(raw_input("Choose one from the above messages\n "))
        #We have to check if the number entered by the user is valid, i.e. it is less than or equal to the length of the STATUS_MESSAGES list. len function returns the number of elements in the list.
        if len(STATUS_MESSAGES) >= message_selection:
             updated_status_message = STATUS_MESSAGES[message_selection - 1]
    else:
        print 'The option you chose is not valid! Press either y or n.'

    if updated_status_message:
        print 'Your updated status message is: %s' % (updated_status_message)
    else:
         print 'You current don' \
               '\'t have a status update'
    return updated_status_message


#function to add a friend
def add_friend():
    new_friend=Spy('','',0,0.0)
    new_friend.name = raw_input("Please add your friend's name:\n")
    new_friend.salutation= raw_input("Are they Mr. or Ms.? \n")
    new_friend.name = new_friend.salutation + " " + new_friend.name
    new_friend.age = raw_input("Age?\n")
    new_friend.rating = raw_input("Spy rating?\n")
    #int() method, it converts strings into integers.
    new_friend.age =int(new_friend.age)
    #float() method ,it convert strings into floats
    new_friend.rating =float(new_friend.rating)
    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:
        friends.append(new_friend)
        print 'Friend Added!'

    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'
    return len(friends)


#function to select a friend
def select_friend():
    item_number = 0


    for friend in friends:
        #String formatting using placeholders
        print '%d %s aged %d with rating %.2f is online'%(item_number+1, friend.name,friend.age,friend.rating)
        item_number=item_number+1


    friend_choice = raw_input("Choose from your friends\n")
    friend_choice_position = int(friend_choice) - 1

    return friend_choice_position


#function to send a message
def send_message():

    #to choose friend to which i want to send_message using select_friend function
    friend_choice = select_friend()

    original_image = raw_input("What is the name of the image?")
    output_path = "output.jpg"
    text = raw_input("What do you want to say? ")
    # handle for case when image doesn't contain any secret message
    if len(text) > 0:
        #The encode function takes the secret message, the image, and the output path as input and creates the image with the hidden secret message at the output path.
        Steganography.encode(original_image, output_path, text)

        new_chat = ChatMessage(text,True)

        friends[friend_choice].chats.append(new_chat)

        print "Your secret message image is ready!"
        # Delete a spy from your list of spies if they are speaking too much. (More than 100 words)
        length = len(text.split())
        if length > 100:
            friends.pop(friend_choice)
    else:
        print"please enter a valid message"

#function to read a message
def read_message():

    #get the position of the friend whose chat we need to read, using the select_friend() function.
    sender = select_friend()

    output_path = raw_input("What is the name of the file?")

    #The decode fucntion takes the image with the hidden secret message as input and returns the secret text.
    secret_text = Steganography.decode(output_path)
    #To save the secret message that we decoded in the read_message() function along with the current timestamp.
    new_chat = ChatMessage(secret_text,False)

    friends[sender].chats.append(new_chat)

    print "Your secret message has been saved!"
    print  secret_text


#function to read chat history
def read_chat_history():

    read_for = select_friend()

    print '\n'

    for chat in friends[read_for].Chats:
        #we check if the chat was sent by the active user or some other spy. We are also using the strftime() function to format the timestamp associated with each chat message.
        if chat.sent_by_me:
            print '[%s] %s: %s' % (chat.time.strftime("%d %B %Y"), 'You said:', chat.message)
        else:
            print '[%s] %s said: %s' % (chat.time.strftime("%d %B %Y"), friends[read_for].name, chat.message)


#function to start chat
def start_chat(spy):
    current_status_message =None
    spy.name = spy.salutation + " " + spy.name
    if spy.age > 12 and spy.age < 50:
        #printing a welcome message with all the details about the spy:
        print "Authentication complete.""\nWelcome " + spy.name + " \nage: " + str(spy.age) + " \nAnd rating of: " + str(spy.rating) + '\n"Proud to have you onboard"'
        show_menu = True
        #To print a menu multiple times, we can enclose it in a while loop
        while show_menu:
            #set of options of the possible actions that can be performed in the application to choose from.
            menu_choices = "What do you want to do.please choose any one option from here? \n 1.Add a status update\n 2.Add a friend\n 3.select a friend\n 4.Send a secret message\n 5.Read a secret message\n 6.Read Chats from a user\n 7.Close Application\n"
            menu_choice = raw_input(menu_choices)
            if len(menu_choice)> 0:
                 menu_choice = int(menu_choice)
                 if menu_choice==1:
                     print 'You chose to update the status'
                     spy.current_status_message=add_status()
                 elif menu_choice==2:
                     print"you choose to add a friend"
                     number_of_friends = add_friend()
                     print 'You have %d friends' % (number_of_friends)
                 elif menu_choice==3:
                     index = select_friend()
                     print "friend choice position %d"%(index)
                 elif menu_choice==4:
                     send_message()
                 elif menu_choice==5:
                     read_message()
                 elif menu_choice==6:
                     read_chat_history()
                 else:
                     show_menu = False

#condition to check that continue as default user or not
if existing.upper() == "Y":
    #calling of function start_chat
    start_chat(spy)
elif existing.upper()=="N":
    spy=Spy('','',0,0.0)
    spy.name=raw_input("what is your name?")
    if len(spy.name)>0:
        print 'Welcome ' + spy.name + " .glad(*_*) to have you with us"
        spy.salutation=raw_input("what should we call you?(mr. or ms.)\n")
        if len(spy.salutation)>0:
            spy.name=spy.salutation + " " + spy.name
            print "alright"+spy.name+".i'd like to know about more before we proceed"
            spy.age=raw_input("what is your age?\n")
            # type() method tells you the type of your information or data.
            print type(spy.age)
            spy.age=int(spy.age)
            print type(spy.age)
            #hi
            #condition to check age to be a spy
            if spy.age<50 and spy.age>12:

               spy.rating=raw_input("what is your spy_rating\n")
               spy_rating=float(spy.rating)
               if(spy.rating>4.5):
                   print"you are good ace"
               elif spy.rating>3.5 and spy.rating<=4.5:
                   print"you are one of the good one"
               elif spy.rating >= 2.5 and spy.rating<= 3.5:
                   print 'You can always do better'
               start_chat(spy)
            else:
                print'Sorry you are not of the correct age to be a spy'
        else:
             print "please enter salutation. it is mandatory"

    else:
        print "plz enter valid spy name"

