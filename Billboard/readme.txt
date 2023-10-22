iot billboard instructions - ryan wachter
last update: october 13 2023

readme:

-- HOW TO SELECT IMAGES --

every image must be .png

put images in the BillboardManager folder on the Desktop

to select an image for the script, 
type the name WITHOUT the file extension into img.txt

example for img.txt:
flag (correct)
flag.png (incorrect)

make sure there is NOTHING else in img.txt besides the png file name!

-- HOW TO START THE BILLBOARD --

open up a terminal (top left of screen)

type 'sudo su' (without the '')

password is promhub

go to the BillboardManager directory

the directory path is /home/lbc2/Desktop/BillboardManager/

to get there after doing sudo su, type 'cd Desktop'

After you get into the Desktop folder, type 'cd BillboardManager'

once you get in the BillBoardManager folder;

-- TYPE THE FOLLOWING TO START THE SCRIPT --

python3 billboard.py

-- HOW TO CLOSE THE SCRIPT --

go back to the terminal and use CTRL+C
