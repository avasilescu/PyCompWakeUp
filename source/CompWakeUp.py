#CompWakeUp
#Alex Vasilescu
#Python Script to wake up desktop using the RaspberryPi

import ConfigParser;

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
 


