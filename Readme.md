Special remind:
- Only working with google mail, password used is the app password (search google to find how to get app password)
- Sample of file spreadsheet: https://docs.google.com/spreadsheets/d/1sKRQDGanb-EhVrtN2mqUgSC2zMjEsK2TWGfbWYTykdU/
- File spreadsheet must turn on share to allow code view data.
- Signature can using html structure for beauty. Set in Summary sheet
- Mail structure are harshed code that started with: "Dear {Fullname},". The body in file spreadsheet is the text after the Dear ... line.
- Body text allow using html tag like <b></b>...
- File in mail template not yet using in code (update later)
- Using fullname, name, pronoun, key in body mail must write with first letter capitalized and placed inside {}. Eg: {Fullname} 
- Fullname and name always capitalized the first letter of every word.
- Pronoun and key to capitalized first letter based on position in body, place C before it. Like this: {CPronoun}, {CKey}
- Script doesn't auto update time send and status. Want to update then do it manually.

List of setup for environment to run:
- python
- python package: pandas, requests, python-dotenv, cryptography

Setup:
1. Installing python and it package it to run. If already has then skip this step.
2. Create a google spreadsheet file to store data following example: https://docs.google.com/spreadsheets/d/1sKRQDGanb-EhVrtN2mqUgSC2zMjEsK2TWGfbWYTykdU/
3. Open CMD (if using Window)/Open termux (using Android) then 'cd' to moving forward to the folder
4. Type then enter: python main.py 
5. Enter module number 2 to setup gmail and password
6. Enter 3 to setup the link sheet and gid to sheet
7. Run module 1 and choose which to run
