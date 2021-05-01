# Pihole-404
A nice 404 page for pihole with an acompanying automatic script that can be used to whitelist the domain with the click of a button.

![This is what your 404 page will look like. Of course, you can also customize it.](./Screenshot.png)
_^Above: This is what your 404 page will look like! Of course, feel free to customize it._

## Table of Contents
* [The Problem](#the-problem)
* [The Solution](#the-solution)
* [Step 1](#step-1)
* [Step 2](#step-2)
* [Step 3](#step-3)
* [Known Bugs](#known-issuesbugs)
* [Credits](#credits)

## The Problem:
&emsp; Setting up a Pihole is awesome and pretty easy. But what happens when a page you want to go to is blocked? You get a boring 404 error. And what if you want to go to the webpage? First, you have to go to your pihole's website. Then you have to login. Next, you need to go to whitelist and type in the domain. This is great, but what if you don't know the password or a client has problems?

## The Solution:
&emsp; Pihole-404 to the rescue! This simple script will add a button that lets you email the admin. This email will be read by an automatic python script and the domain will be whitelisted! And on top of all that, it makes the 404 page look very nice!

## Step 1: Install Pihole and Get it Working
Head over to https://github.com/pi-hole/pi-hole

## Step 2: Enable Less Secure App Access and IMAP
If you are using Gmail, you need to enable less secure app access to your google account [here](https://myaccount.google.com/lesssecureapps). You also need to enable IMAP, if it is not already enabled [here](https://mail.google.com/mail/u/0/#settings/fwdandpop). Scroll down to **IMAP Access** and make sure **Status** is set to **Enable IMAP**. I am not sure about other providers as I have not tried them.

## Step 3: Set up the Repo and Install
On the Raspberry Pi, Clone this repository:
#### `git clone https://github.com/BennyThePythonCoder/Pihole-404.git`
Navigate to the project folder:
#### `cd Pihole-404`
or wherever the repo folder was installed if you installed it in a different location.\
Run the installer script:
#### `sudo sh install.sh`
And everything should work!

## Known Issues/Bugs
&emsp; When using SSH to access the Raspberry Pi, the email checker program may be stopped when exitting SSH. If this happens, just log on to the Raspberry Pi through HDMI and a keyboard. Then go to the folder you cloned this repo in using `cd` type:
#### `watch -n 10 python3 EmailChecker.py &`
This will start the program in the background.
Any time you shutdown or restart, you also must run this command.
If the Raspberry Pi updates, you may need to run the installer script again since the file /etc/lighttpd/lighttpd.conf is changed. The installer script should fix this.\
#### _Note: This script sets blocking mode to IP blocking. If you want to change this, just edit /etc/pihole/pihole-FTL.conf and set blocking mode to NULL ._

## Credits:
* Everyone at [pi-hole](https://pi-hole.net) ([Github](https://github.com/pi-hole/pi-hole))
* [This](https://www.reddit.com/r/pihole/comments/a9v7jj/how_to_install_a_custom_block_page_for_websites/) Reddit post which was incredibly useful
* *imap-tools* python package, found [here at pypi](https://pypi.org/project/imap-tools/), used for processing emails
* [Python3](https://python.org), a phonomenal programming language everyone should know
* [The Raspberry Pi Foundation](https://raspberrypi.org) for making awesome little computers
* Wallpaperflare for amazing images ([Astronaut](https://www.wallpaperflare.com/astronaut-clipart-space-monochrome-artwork-copy-space-close-up-wallpaper-ppoyl), [Moon](https://www.wallpaperflare.com/minimalism-space-black-background-artwork-simple-background-wallpaper-pmmgi))
* [Pixlr E](https://pixlr.com/e/) for great online photo editing

# If you find this repo useful, **please star it and share it!** If you have questions, just create an [issue](https://github.com/BennyThePythonCoder/Pihole-404/issues).
