# Lost & Found Bot

<img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-22.jpg" width=300>

- Using robust bot framework provided by Telegram
- Locate lost items easily by simply texting the bot
- Only requires a device capable of running Telegram app [Android, iPhone, Mac, Windows, Linux]
- Easy Admin management features backed right into the bot

## Easy for users
<img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-25.jpg" width=250> | <img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-27.jpg" width=250> | <img  src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-32.jpg?raw=true" width=250>

- Simply text and see if your item is there with the Lost & Found department. 
The bot can also send the image of the items so you can be sure it belongs to you only.

- Users can report their lost items to the  Lost & Found department via the bot.
If their item is found, admin can easily message and notify the user that their item is found!

## Easy for admins
<img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-23-54.jpg?raw=true" width=250>

<img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-29.jpg?raw=true" width=250> | 
<img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-06-36.jpg?raw=true" width=250> | <img src="https://github.com/ashvnv/Lost-And-Found-Bot/blob/main/pics/photo_2021-07-09_15-25-23.jpg?raw=true" width=250>
- Admins can easily add or remove items from the database by simply texting the bot. 
No need to use a separate computer for database management.
Multiple admins can be authorised.


# Database management
- For Admins</br>
The bot stores admin information in admin.txt file. This file is automatically made if the file does not exist in program's root folder. The information about admin is stored in JSON format. It includes 'from' information which is sent by the bot.
Multiple admins can be authorised and are stored in the following manner:
> {"123456789": {"id": 123456789, "is_bot": false, "first_name": "Ashwin", "username": "abcd", "language_code": "en"}}

- For lost items list</br>
Lost items list is stored in JSON format in items_data_raw.txt. This file is made automatically by the program if the file does not exist in root folder. Information is stored in following JSON format along with the admin info who added the item.
> {"umbrella": [{"name": "umbrella", "img": "ADDED"}, {"id": 123456789, "is_bot": false, "first_name": "Ashwin", "username": "abcd", "language_code": "en"}]}

Once an item is added the bot marks "img" key as "NA". When the same admin sends an image file next time, the bot reads the JSON data and sees for which item the "img" key is "NA" and saves the image file in .png format in program's root directory with the file name same as the item name sent before ( in "name" key). Once the image is stored locally the JSON details of that item is modified with "img" key made ADDED.
Next time when someone taps on that item name from user panel the same image is forwarded!
