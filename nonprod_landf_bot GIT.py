"""
MIT License

Copyright (c) 2021 Ashwin Vallaban

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#Lost & Found Telegram Bot
#This project was mode for FCRIT HACK-X-TRONICS 2021
#3 July 2021
#
#This program is not ready for production use
#
#Telegram Bot Token was removed for security reasons
#For authorising a user as an admin send a text:
#                                               Auth <code>
#                                               Auth 123
#                                               Auth code for now is 123. It can be changed from this function: admin_auth_add()


import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import json
import re
import os

#----------------------------------------------------------------------


###########################
#var names
#Menu words are specified here

userpanelback_msg = '⬅ Back [user]'
adminpanelback_msg = '⬅ Back [admin]'
main_menuback_msg = '⬅ Back'

DEPT_CONTACT_INFO = 'Department contact number <>'

msg1 = 'Lost something? click here!\n💁🏽'
msg2 = 'Admin Panel\n🗿'
msg3 = 'Contact the department 📞'

msg4 = 'Get a list of all lost items with the department\n📒'
msg5 = 'Search for an item'
msg6 = 'Report a lost item\n🖊️'

msg7 = 'Add an item\n📝'
msg8 = 'Delete an item\n❌'
msg9 = 'Send a message to the user\n✉️'


###########################


#Telegram Bot Token-------------------------------------
TOKEN = "<>" #Token Removed for security reasons
#-------------------------------------------------------

#func reads the txt file and returns it's contents
#filename should be with extension
def file_read(filename, filemode):
    print('file_read()')
    # Open a file: file
    file = open(filename,mode=filemode)
 
    # read all lines at once
    itemdata = file.read()
 
    # close the file
    file.close()

    print('File Read')

    return itemdata


#=============================================== Main Menu ==========================================================
def main_menu(chat_id):
    print('main_menu()')
    bot.sendMessage(chat_id, 'Main Menu',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            #msg: 1,2,3
                            [KeyboardButton(text=msg1),KeyboardButton(text=msg2),KeyboardButton(text=msg3)]
                            ]
                        )
                    )
    print('Executed custom keyboard')
    


#=============================================== User Panel =========================================================

def user_panel(chat_id):
    print('user_panel()')
    bot.sendMessage(chat_id, 'Don\'t worry! We will help you.',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            #msg: 4,5,6,3
                            [KeyboardButton(text=msg4)],
                            #[KeyboardButton(text=msg5)],
                            [KeyboardButton(text=msg6)],
                            [KeyboardButton(text=main_menuback_msg)]
                            ]
                        )
                    )
    print('Executed custom keyboard')

    
def all_items(chat_id):
    print('all_items()')

    itemdata = file_read('items_data_raw.txt','r') #read the current data

    json_dictionary = json.loads(itemdata)

    temp = ''
    temp += '[KeyboardButton(text=userpanelback_msg), KeyboardButton(text=msg3)]' #add back and contact dept texts

    for j in json_dictionary.items():
        temp +=',[KeyboardButton(text="' + str(j[1][0]['name']) + '")]' #add items name in dictionary
        


#create custom keyboard in telegram
    temp_exec_string = '''
def all_items_display():
    bot.sendMessage(''' + str(chat_id) + ''', 'Click on an item to see image',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            ''' + temp + '''
                            ]
                        )
                    )
all_items_display()
'''
    exec(temp_exec_string) #execute the string temp_exec_string. the string was made for constructing dynamic keyboard with items in database (item_data_raw.txt)
    print('Executed custom keyboard')


#this func send the image of the item which user clicked
def all_items_img(chat_id, item_search):
    print('all_items_img()')
    
    itemdata = file_read('items_data_raw.txt','r')

    json_dictionary = json.loads(itemdata)

    for j in json_dictionary.items():
        if item_search == str(j[1][0]['name']):
            bot.sendMessage(chat_id, 'Sending image of ' + str(item_search) + '. Please wait...')
            try:
                bot.sendPhoto(chat_id, photo=open(item_search + '.png', 'rb'))
            except:
                bot.sendMessage(chat_id, 'Image not found <error>')
            return True
    return False

 

#=============================================== Admin Panel ==================================================

#the func returns True if the user is authorised as an admin and False otherwise
#this func is called inside Root section of the program by admin privileged codes
def admin_auth(chat_id,admininfo):
    print('admin_auth()')
    
    itemdata = file_read('admin.txt','r')

    json_dictionary = json.loads(itemdata)

    for k in json_dictionary:
        if str(chat_id) == k:
            bot.sendMessage(chat_id, 'Welcome admin ' + admininfo['first_name'] + '!')
            print('admin authorised')
            return True

    bot.sendMessage(chat_id, 'You are not authorised. Send auth code first in following syntax: \n\n Auth<space><admincode>\n\ne.g.,\nAuth 123')
    print('unauthorised access')
    return False


#this func adds the user as admin after verifying the code sent by that user
def admin_auth_add(chat_id, admininfo, code):
    print('admin_auth_add()')

    if (code == '123') == False:
        bot.sendMessage(chat_id, 'Wrong auth code!')
        print('wrong auth code')
        return
    
    itemdata = file_read('admin.txt','r')

    json_dictionary = json.loads(itemdata)

    itemdata_new = """
{
  \"""" + str(chat_id) + """\":{

}
}
"""
    #below codes adds the user to admin.txt json file
    json_dictionary_new = json.loads(itemdata_new)

    json_dictionary_new[str(chat_id)].update(admininfo)

    json_dictionary.update(json_dictionary_new)

    # Open a file: file
    with open('admin.txt','w') as file:
        file.write(json.dumps(json_dictionary))
 
    # close the file
    file.close()

    bot.sendMessage(chat_id, 'You have been authorised as an admin!')

    print('user added as an admin')


#this func sends a list of all items in the database with prefix 'Delete:'. Clicking on an item will then delete it from the database by item_delete()
def delete_item_list(chat_id):
    print('delete_item_list()')
    itemdata = file_read('items_data_raw.txt','r')

    json_dictionary = json.loads(itemdata)

    temp = ''
    temp += '[KeyboardButton(text=adminpanelback_msg)]'

    for j in json_dictionary.items():
        temp +=',[KeyboardButton(text="Delete: ' + str(j[1][0]['name']) + '")]'
        



    temp_exec_string = '''
def all_items_display():
    bot.sendMessage(''' + str(chat_id) + ''', 'Click on an item to delete',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            ''' + temp + '''
                            ]
                        )
                    )
all_items_display()
'''
    exec(temp_exec_string)
    print('Executed custom keyboard')



def admin_panel(chat_id):
    print('admin_panel()')
    bot.sendMessage(chat_id, 'Admin Panel',
                    reply_markup=ReplyKeyboardMarkup(
                        keyboard=[
                            #msg: 7,8
                            [KeyboardButton(text=msg7),KeyboardButton(text=msg8)],
                            [KeyboardButton(text=msg9)],
                            [KeyboardButton(text=main_menuback_msg)]
                            ]
                        )
                    )
    print('Executed custom keyboard')

#this func deletes the item
def item_delete(chat_id, name):
    print('item_delete()')
    
    itemdata = file_read('items_data_raw.txt','r')

    json_dictionary = json.loads(itemdata)

    del json_dictionary[name]
        
    # Open a file: file
    with open('items_data_raw.txt','w') as file:
        file.write(json.dumps(json_dictionary))
 
    # close the file
    file.close()

    #delete photo from local folder
    os.remove(name + '.png')

    bot.sendMessage(chat_id, 'Item deleted')

    print('Item deleted')

    delete_item_list(chat_id) #send a new list to the admin

    return


#this func adds a new item
def item_add(chat_id, admininfo, name):
    print('item_add()')
    
    itemdata = file_read('items_data_raw.txt','r')

    json_dictionary = json.loads(itemdata)

    itemdata_new = """
{
  \"""" + name + """\": [
    {
      "name": \"""" + name + """\",
      "img": "NA"
    }
  ]
}
"""

    #codes below will add the item to the existing database
    #added item needs an image which shall only be sent by the person who added the item
    #the json structure "img" is made "NA" which allows photo_add() to see on which item the image shall be added
    #once the image is added the "img" is made "ADDED" inside photo_add()
    json_dictionary_new = json.loads(itemdata_new)

    json_dictionary_new[name].append(admininfo)

    json_dictionary.update(json_dictionary_new)

    
    # Open a file: file
    with open('items_data_raw.txt','w') as file:
        file.write(json.dumps(json_dictionary))
 
    # close the file
    file.close()

    bot.sendMessage(chat_id, 'Item added. Send an image!')

    print('item added')

    return


#this func adds a photo  to the item
#added item needs an image which shall only be sent by the person who added the item
def photo_add(chat_id,msg):
    print('photo_add()')
    
    itemdata = file_read('items_data_raw.txt','r')

    json_dictionary = json.loads(itemdata)

    for k,v in json_dictionary.items():
        if v[0]['img'] == 'NA':
            if v[1]['id'] == chat_id:
                #download image and save with the same filename
                bot.download_file(msg['photo'][-1]['file_id'], './' + str(k) + '.png')
                bot.sendMessage(chat_id, 'Image added to Item: ' + str(k))
                v[0]['img'] = 'ADDED'

                # Open a file: file
                with open('items_data_raw.txt','w') as file:
                    file.write(json.dumps(json_dictionary))
 
                # close the file
                file.close()

                print('Image added')

                return
            
    bot.sendMessage(chat_id, 'Add a new item before sending an image')
    print('Image not added')


#this func allows user to send message to the admin
def report_admin(chat_id, userinfo, msg):
    print('report_admin()')

    itemdata = file_read('admin.txt','r')

    json_dictionary = json.loads(itemdata)

    for k,v in json_dictionary.items():
        bot.sendMessage(k, 'Lost item report:\n\n' + msg + '\n\n Message sent by:\n' + str(userinfo))
        print('reported')

    bot.sendMessage(chat_id, 'We will notify you once your item is found')
    print('Received a report')
    
    

#this is where the messages sent to the bot are analyzed the appropriate func is called accordingly
################################ ROOT #####################################
def on_chat_message(msg):
    print('\non_chat_message() msg received')
    
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':

        if msg['text'] == msg1 or msg['text'] == userpanelback_msg:
            user_panel(chat_id)
            
        elif msg['text'] == msg2 or msg['text'] == adminpanelback_msg:
            #admin auth
            if admin_auth(chat_id,msg['from']):
                admin_panel(chat_id)

        elif msg['text'] == msg3:
            bot.sendMessage(chat_id, DEPT_CONTACT_INFO)

        #==================== User panel ==========================
        
        elif msg['text'] == msg4:
            all_items(chat_id)


        elif msg['text'] == msg5:
            print('search an item, not added yet!')
            
        elif msg['text'] == msg6:
            print('Report a lost item')
            bot.sendMessage(chat_id, 'Send details in following syntax\n\nSyntax\nReport<space><details>\n\ne.g.,\nReport i lost my yellow wallet in cafeteria')

        elif re.search("^Report.+",msg['text']):
            report_admin(chat_id, msg['from'], re.findall(" .+", msg['text'])[0].strip())

        #==================== Admin panel =========================

        
        elif msg['text'] == msg7:
            print('Add an item')
            bot.sendMessage(chat_id, 'To add an item send the name in following syntax:\n\n Add<space><name of item>\n\ne.g.,\nAdd red umbrella')

        elif re.search("^Add.+",msg['text']):
            #admin auth
            if admin_auth(chat_id,msg['from']):
                print('found add item')
                item_add(chat_id, msg['from'], re.findall(" .+", msg['text'])[0].strip())

        
        elif msg['text'] == msg8:
            #admin auth
            if admin_auth(chat_id,msg['from']):
                print('Delete an item')
                delete_item_list(chat_id)
            

        elif re.search("^Delete:.+",msg['text']):
            #admin auth
            if admin_auth(chat_id,msg['from']):
                print('found delete item')
                item_delete(chat_id, re.findall(" .+", msg['text'])[0].strip())

        elif re.search("^Auth.+",msg['text']):
            print('found auth code')
            admin_auth_add(chat_id, msg['from'], re.findall(" .+", msg['text'])[0].strip())

        elif msg['text'] == msg9:
            if admin_auth(chat_id,msg['from']):
                print('send message to user')
                bot.sendMessage(chat_id, 'To send a message to the user follow this syntax:\nUser<space><id><space><message>\nwhere id can be found in the Lost item report text\n\ne.g.\nUser 12345678 You wallet has been found! Collect it from the L&F department')

        elif re.search("^User.+",msg['text']):
            if admin_auth(chat_id,msg['from']):
                bot.sendMessage(re.findall(" [0-9]+", msg['text'])[0].strip(),re.findall(" [A-z].+", msg['text'])[0].strip() + '\n\nSent by L&F dept. admin ' + msg['from']['first_name'])
                bot.sendMessage(chat_id, 'Message sent')
                print('message sent to the user')
            
        #=====================
        elif all_items_img(chat_id, msg['text']): #send the image of the item
            print('Img sent')
            
        else:
            main_menu(chat_id)
            print('show main menu')
            
    elif content_type == 'photo':
        print('photo sent by user')
        bot.sendMessage(chat_id, 'uploading image... wait sometime')
        photo_add(chat_id,msg)

    else:
        bot.sendMessage(chat_id, 'Error!')
        print('Invalid file sent')
        

bot = telepot.Bot(TOKEN)
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)
