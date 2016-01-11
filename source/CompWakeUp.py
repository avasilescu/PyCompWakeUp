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

	Comps=config.get('General','Computers').split('\n');
	MAC=config.get('General','MAC').split('\n');
	Broadcast=config.get('General','Broadcast').split('\n');	
	comp_user=config.get('General','comp_user').split('\n');
	comp_pw=config.get('General','comp_pw').split('\n');
    
    #for debugging to see it read in correctly
	print("Comps: ");
	print(Comps); 

	return(gmail_server,imap_port,username,password,Comps,MAC,Broadcast,comp_user,comp_pw);
'''	
Theory of operation

In the config file, the order of the Subjects, Broadcast, Computers and MAC addresses are respective of the computer.
Thus it will be:

Subject =	Comp 1
			Comp 2
Computers =	Comp 1
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

def rmtshutdown(ADDR,MAC,comp_user,comp_pw):
	print ADDR;
	print MAC;
	subprocess.call(['net rpc shutdown','-I',ADDR,'-U',comp_user,comp_pw]);

def CreateSubjectArray(Computers,wol_subject,shutdown_subject):
	Subjects=[];
	print("Subjects:");
	print(Subjects);
	for i, Comp in enumerate(Computers):
		print("i= " + str(i));
		print("Comp= " + Comp);
		print("WOL Subject= " + wol_subject);
		Subjects.append(wol_subject + Comp);
	
	print("Subjects:");
	print(Subjects);

	SubjectLength = len(Subjects);
	for i, Comp in enumerate(Computers):
		print("i= " + str(i));
		print("Comp= " + Comp);
		print("Shutdown Subject= " + shutdown_subject);
		Subjects.append(shutdown_subject + Comp);

	print("Subjects:");
	print(Subjects);

	return(Subjects);

def CreateSubjectArray2(Computers, ImportSubject):
	ExportSubjects=[];

	for subj in enumerate(ImportSubject):
		for i, Comp in enumerate(Computers):
			print("i= " + str(i));
			print("Comp= " + Comp);
			ExportSubjects.append(subj + Comp);

	print("ExportSubjects:");
	print(ExportSubjects);

	return(ExportSubjects);

#Subject names used for searching; remember space after subject
wol_subject = "WOL "
shutdown_subject = "Shutdown "

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)));

#for debugging absolute location
print __location__;
print(os.path.join(__location__,'CompWakeUp.conf'))

gmail_server,imap_port,username,password,Comps,MAC,Broadcast,comp_user,comp_pw=ImportConf(os.path.join(__location__,'CompWakeUp.conf'));

#Creates subject arrary
SubjectArray = CreateSubjectArray(Comps, wol_subject, shutdown_subject);
print("SubjectArray:");
print(SubjectArray);

#goes through each "subject" and checks email to see if any new emails. sends WOL packet if so.
for idx,Subject in enumerate(SubjectArray):
	print('Array Index - ' + str(idx));
	print('Subject - ' + Subject);
	CompFlag=EmailChecker(gmail_server,imap_port,username,password,Subject);
	if CompFlag and str.find(Subject, wol_subject):
		print('Waking up - ' + Comps[idx]);
		WOL(Broadcast[idx],MAC[idx]);
	if CompFlag and str.find(Subject, shutdown_subject):
		print('Shutting down - ' + Comps[idx]);
		rmtshutdown(Broadcast,MAC,comp_user,comp_pw);