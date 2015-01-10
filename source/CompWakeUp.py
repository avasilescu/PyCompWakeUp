#CompWakeUp
#Alex Vasilescu
#Python Script to wake up desktop using the RaspberryPi

import imaplib;
import ConfigParser;
import subprocess;
import os;

def ImportConf(filename):
	config=ConfigParser.ConfigParser();	
	print('Reading file: ' + filename);	
	config.read(filename);
	
	gmail_server=config.get('IMAP Server', 'gmail_server');
	imap_port=config.get('IMAP Server','imap_port');
	username=config.get('IMAP Server','username');
	password=config.get('IMAP Server','password');

	Subject=config.get('General','Subjects').split('\n');	
	Comps=config.get('General','Computers').split('\n');
	MAC=config.get('General','MAC').split('\n');
	Broadcast=config.get('General','Broadcast').split('\n');	

	print(Comps); #for debugging to see it read in correctly

	return(gmail_server,imap_port,username,password,Subject,Comps,MAC,Broadcast);
'''	
Theory of operation

In the config file, the order of the Subjects, Broadcast, Computers and MAC addresses are respective of the computer.
Thus it will be:

Subject =   Comp 1
            Comp 2
Computers = Comp 1
            Comp 2
            
Software can then check for each computer listed.
'''
 
def EmailChecker(server,port,user,pw,subject):
	#Log into email server using IMAP over SSL
    mail = imaplib.IMAP4_SSL(server,port);
	mail.login(user, pw);

    #For Gmail, mail.select can select "inbox" or a label such as "WOL Comp". Can rely on Gmail filters instead of developing custom from scratch.
	mail.select(subject); 
	
	typ, data = mail.search(None, '(UNSEEN)'); #search for unread emails
	NewEmailFlag=False;	#initializes flag to false
	
    for num in data[0].split():
		typ, data = mail.fetch(num, '(RFC822)') #RFC822 is a parser for email headers; downloading any new email that matches "subject" specified above. 
		if num > 0: NewEmailFlag=True; #if new email, set flag

	mail.close(); #close currently selected mailbox
	mail.logout(); #shutdown connection to server
	print('New Email - ' + str(NewEmailFlag)); #useful for debugging and testing
	return NewEmailFlag;

def WOL(ADDR,MAC):
	print MAC;	#debugging only
    #for the following command to work, "wakeonlan" needs to be installed. for RPi (assuming raspian distro), run command "sudo apt-get install "wakeonlan"
	subprocess.call(['wakeonlan','-i', ADDR,MAC]);
    
gmail_server,imap_port,username,password,Subjects,Comps,MAC,Broadcast=ImportConf('CompWakeUp.conf');

#goes through each "subject" and checks email to see if any new emails. sends WOL packet if so.
for idx,val in enumerate(Subjects):
    print('Array Index - ' + str(idx));
    print('Subject - ' + val);
    CompFlag=EmailChecker(gmail_server,imap_port,username,password,Subjects[idx]);
    if CompFlag:
        print('Waking up - ' + Comps[idx]);
        WOL(Broadcast[idx],MAC[idx]);

    
