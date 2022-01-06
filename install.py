#!/usr/share/python3

# import necessary requirements
import os
import os.path
import time

# Easily clear the screen
def clearScreen(numlines):
    for i in range(0,int(numlines)):
        print("\n")

# Easily rewrite a line in a file
def rewrite(file, line, target_text):
    with open(file, 'r') as FILE:
        data = FILE.readlines()
        data[line-1] = target_text
        FILE.close()
    with open(file,'w') as FILE:
        FILE.writelines(data)
        FILE.close()

# Clear the screen
clearScreen(20)

# Cool splash text
print("""
______   _ _           _               ___ _____    ___
| ___ \ (_) |         | |             /   |  _  |  /   |
| |_/ / | | |__   ___ | | ___ ______ / /| | | | | / /| |
|  __/  | |  _ \ / _ \| |/ _ \______/ /_| | |/| |/ /_| |
| |     | | | | | (_) | |  __/      \___  | |_/ |\___  |
\_|     |_|_| |_|\___/|_|\___|          |_/\____/    |_/

By BennyThePythonCoder

Repo can be found at (https://github.com/BennyThePythonCoder/Pihole-404)
Thanks to pi-hole (pi-hole.net) (https://github.com/pi-hole/pi-hole)
Other credits can be found at (https://github.com/BennyThePythonCoder/Pihole-404#credits)
""")
# Waits 5 seconds, then clears the screen
time.sleep(5)
clearScreen(20)

email_file = "EmailChecker.py"
php_file = "CustomBlockPage.php"

# Checks if the program has been run previously and if there is already a configeration file credentials.txt
file_exists = os.path.exists('credentials.txt')
if file_exists:
    redo_setup = input("""
    Configuration file credentials.txt found.
    Would you like to use previous settings (Y)? Or would you like to redo the setup (n)? (Y/n)
    """)
else:
    redo_setup = "n"
yes_strings = {'YES', 'Yes', 'yes', 'Y', 'y'}
no_strings = {'NO', 'No', 'no', 'N', 'n'}
if file_exists == False or redo_setup in yes_strings:
    # Installs python script dependency imap-tools
    print("[...] Installing Python3 EmailChecker.py dependency imap-tools (for automatically checking email to whitelist domain)")
    os.system('sudo pip3 install imap-tools')
    print("[✓] Installed Python3 EmailChecker.py dependency imap-tools\n\n")

    email = input("Please enter your email for the script: ")
    password = input("Please entery your email password: ")
    provider = input("What email provider do you use? (gmail/outlook/aol/yahoo/other) ")

    if provider == "gmail":
        provider = "imap.gmail.com"
    if provider == "outlook":
        provider = "imap-outlook.com"
    if provider == "aol":
        provider = "imap.aol.com"
    if provider == "yahoo":
        provider = "imap.yahoo.com"
    if provider == "other":
        print("Please look at https://www.systoolsgroup.com/imap/\n\n")
        provider = input("""
        If your provider was listed there, then please input the IMAP address of the provider.
        If it was not there, then use a search engine to find the IMAP address of your provider.
        Please type the IMAP address here (for example imap.gmail.com for Gmail):
        """)

    print(f"Your provider's IMAP address is: {provider}")

    # Adds credentials to the files so they work properly
    print("[...] Adding credentials to files EmailChecker.py and CustomBlockPage.php so the script can work")
    rewrite(php_file, 20, f"      <a href='mailto:{email}?subject=Domain%20Blocked&body=[sub]' onclick='this.href =this.href.replace('[sub]',window.location)' target='_blank' rel=noopener noreferrer><button style='background-color:white; border-color:white'>here</button></a>.<br>\n")
    rewrite(email_file, 9, f"with MailBox('{provider}').login('{email}', '{password}', initial_folder='INBOX') as mailbox:\n")
    print("[✓] Finished adding credentials to files")

    # Create credentials.txt for future setups
    with open('credentials.txt', 'w') as credentials_file:
        credentials_file.write("\n\n\n") # clears the file, avoids errors/problems
        # actually adds updated credentials to the file
        credentials_file.write(f"""
        EMAIL:{email}
        PASSWORD:{password}
        PROVIDER:{provider}
        """)
        credentials_file.close()

    # Copy webpage PHP file to correct location
    os.system('sudo cp CustomBlockPage.php /var/www/html/pihole/CustomBlockPage.php')
    os.system('sudo chmod +x /var/www/html/pihole/CustomBlockPage.php')
    os.system('sudo cp Astronaut1.png /var/www/html/pihole/Astronaut1.png')
    os.system('sudo cp background.jpg /var/www/html/pihole/background.jpg')
    print('[✓] Webpage PHP file is located at /var/www/html/pihole/CustomBlockPage.php  Feel free to edit!')
    # Changes the default 404 page to the custom page found in /var/www/html/pihole/
    os.system('sudo sed -i "s:server.error-handler-404    = "/pihole/index.php":server.error-handler-404    = "/pihole/CustomBlockPage.php":gi" /etc/lighttpd/lighttpd.conf')
    print('[✓] Changed configuration file for lighttpd located at /etc/lighttpd/lighttpd.conf')
    os.system('sudo service lighttpd restart')

    # Changes blocking mode to IP in /etc/pihole/pihole-FTL.conf . This will make the custom 404 page display.
    # More details can be found at https://docs.pi-hole.net/ftldns/blockingmode/
    print('The next part of the installer script will set the Pihole blocking mode to IP. More details can be found at:\n https://docs.pi-hole.net/ftldns/blockingmode/ \n If you do not want to change this, press CTRL + C (you have 10 seconds)')
    time.sleep(10)
    FTL_file = '/etc/pihole/pihole-FTL.conf'
    if os.path.exists(FTL_file):
        # file exists
        with open(FTL_file, 'rw') as ftl_file:
            contents = ftl_file.read()
            if 'BLOCKINGMODE' in contents:
                # if BLOCKINGMODE line is in file
                if '=IP' in contents:
                    # if BLOCKINGMODE is set to IP
                    pass # then the work is done and we do not need to edit the file
                else:
                    # If BLOCKINGMODE line is present but not set to IP
                    os.system(f"sudo sed -i 's/.*BLOCKINGMODE.*/BLOCKINGMODE=IP/' {FTL_file}")
            else:
                # BLOCKINGMODE line is not present at all
                # ftl_file.append('BLOCKINGMODE=IP') could also be used, but I want to make sure it uses superuser permissions in this case (sudo)
                os.system('echo "BLOCKINGMODE=IP" | sudo tee -a $FILE')
    else:
        # the FTL_file does not exist
        os.system(f'sudo touch {FTL_file}')
        os.system(f'echo "BLOCKINGMODE=IP" | sudo tee -a {FTL_file}')

    # Start Email Checker program in background, make it check email every 10 seconds
    os.system('while true; do python3 EmailChecker.py ; sleep 10; done &')

    print("""[✓] Email checker program is running! Everything is setup and ready to go!
    Try going to http://doubleclick.net to test it out!
    If you like this script, please star my repository!
    Thanks :]""")

elif redo_setup in no_strings:
    print("OK. Using previous credentials from credentials.txt")
    with open('credentials.txt', 'r') as credentials_file:
        email = credentials_file.readline()
        password = credentials_file.readline()
        provider = credentials_file.readline()
        credentials_file.close()
    # Adds credentials to the files so they work properly
    print("[...] Adding credentials to files EmailChecker.py and CustomBlockPage.php so the script can work")
    rewrite(php_file, 20, f"      <a href='mailto:{email}?subject=Domain%20Blocked&body=[sub]' onclick='this.href =this.href.replace('[sub]',window.location)' target='_blank' rel=noopener noreferrer><button style='background-color:white; border-color:white'>here</button></a>.<br>\n")
    rewrite(email_file, 9, f"with MailBox('{provider}').login('{email}', '{password}', initial_folder='INBOX') as mailbox:\n")
    print("[✓] Finished adding credentials to files")

    # Start Email Checker program in background, make it check email every 10 seconds
    os.system('while true; do python3 EmailChecker.py ; sleep 10; done &')

    print("""[✓] Email checker program is running! Everything is setup and ready to go!
    Try going to http://doubleclick.net to test it out!
    If you like this script, please star my repository!
    Thanks :""")
