import sys
sys.path.append('.')
import django
from django.core.management import setup_environ
import settings
setup_environ(settings)
from dalas.maillog.models import *
from parser import DalasParser
import time


		


		
class EventManager():
	"""
	Just small class to manage 4 typical Postfix Actions, and them track 
	"""

	def __init__(self):
		self.QueueList = { }
		self.QueueRawData = { }
		self.Queuestatus = { }
		self.actor_cmd = None
		self.cmd = {'nqmgr':self.Nqmgr,'qmgr':self.Qmgr,'smtp':self.Smtp,'cleanup':self.CleanUp,'pickup':self.PickUp}
		
		
	
	def HandleEvent(self,data):
		
		queue = Queue.objects.filter(ident=data['unique'])
		if not queue:
			queue = Queue.objects.create(ident=data['unique'])
			
			queue.save()
		else:
			queue = queue[0]
		
		event = Event.objects.create()
		event.label = data['label']
		event.raw_month = data['month']
		event.raw_day = data['day']
		event.raw_time = data['time']
		event.raw_hostname =data['hostname']
		event.raw_actor = data['process']
		event.raw_actor_cmd  = data['childprocess']
		event.raw_pid = data['pid']
		event.raw_line = str(data)
		
		event.queue.add(queue)
		event.save()
		
		
		
			
			
					
		
		

		
		
		
		
		#Check if has actor... and execute...
		
		if data and self.cmd.has_key(data['childprocess']) :
			self.cmd[data['childprocess']](data,queue)
		else:
			#FIX-ME: Create handle to exceptions:
			#need regex to cover
			return False

						
		
	def Qmgr(self,data,queue):
		
		print "QMGR", data
		

	
	def Nqmgr(self,data,queue):
		print data
	
	def Smtp(self,data,queue):
		# FIX-ME: 
		recipients = Recipient.objects.create()
		recipients.label ='send to: %s' % data['output']['to']
		recipients.email_to =data['output']['to']
		recipients.orig_to =data['output']['orig_to']
		recipients.relay_info = data['output']['relay']
		recipients.delays =  data['output']['delays']
		recipients.dsn = data['output']['dsn']
		recipients.status = data['output']['status']
		recipients.queue = queue
		recipients.save()
		

		
		
		

	def CleanUp(self,data,queue):
		#Create Unique MSG ID
		
		msg = Msg.objects.filter(msgid__msgid=data['unique'])
		
		if not msg:
			print data
			msg = Msg.objects.create()
			msg.save()
		else:
			msg = msg[0]
			
		print msg
		
	
			
			
					
		
		#'email_to','orig_to','delays'
		#{'queueId': '2244E61201', 'hostname': 'debian-base', 'childprocess': 'cleanup', 'time': '16:00:08', 'process': 'postfix', 'output': {'message-id': '20100722190008.2244E61201@debian-base.pop-es.rnp.br'}, 'unique': '2244E61201', 'pid': '21339', 'day': '22', 'month': 'Jul'}

		


	def PickUp(self,data,queue):
		print data
		
			
		










a = DalasParser('/tmp/simple.log')
#fix-ME
#if msglist > 1000, refuse input...
manager = EventManager()


for l in a.parse():	
	manager.HandleEvent(l)
	print manager.QueueList
	
	
	


