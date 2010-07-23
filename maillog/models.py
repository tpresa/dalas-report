from django.db import models

MSG_HUMAN_STATE = (
    ('0', 'N/A'),
    ('1', 'Queue active'),
    ('2', 'Sent'),
    ('3', 'Removed from queue'),
)

class Queue(models.Model):
	ident = models.CharField(max_length=250,default=' ')
	label = models.CharField(max_length=250,default=u'',blank=True)
	done = models.BooleanField()

	def __unicode__(self):
		return self.ident
		
class Event(models.Model):
	"""
	POG approach to log events
	"""
	label = models.CharField(max_length=250,blank=True)
	raw_month = models.CharField(max_length=250,blank=True)
	raw_day = models.CharField(max_length=250,blank=True)
	raw_time = models.CharField(max_length=250,blank=True)
	raw_hostname = models.CharField(max_length=250,blank=True)
	raw_actor =models.CharField(max_length=250,blank=True)
	raw_actor_cmd =models.CharField(max_length=250,blank=True)
	raw_pid =models.CharField(max_length=250,blank=True)
	raw_line =models.CharField(max_length=1024,blank=True)
	queue = models.ManyToManyField(Queue,blank=True)
	checkin = models.DateTimeField(auto_now_add=True,editable=False)
	
	def __unicode__(self):
		return self.label	

class Msg(models.Model):
	From = models.CharField(max_length=250,blank=True)
	subject = models.CharField(max_length=250,blank=True)
	start = models.DateTimeField(auto_now=True)
	end = models.DateTimeField(null=True,blank=True)
	average = models.DateTimeField(null=True,blank=True)
	size= models.IntegerField(null=True,blank=True)
	checkin = models.DateTimeField(auto_now_add=True,editable=False)
	done = models.BooleanField()
	
	def __unicode__(self):
		return self.subject

class MsgId(models.Model):
	label = models.CharField(max_length=250,default=u'',blank=True)
	msgid = models.CharField(max_length=250)
	msg = models.ForeignKey(Msg,blank=True)
	queue = models.ManyToManyField(Queue,blank=True)
	checkin = models.DateTimeField(auto_now_add=True,editable=False)	
	
	def __unicode__(self):
		return "%s [ %s ]" % (self.ident,self.label)

class Recipient(models.Model):
	label = models.CharField(max_length=250,default=u'',blank=True)
	email_to =models.CharField(max_length=250,default=u'',blank=True)
	orig_to =models.CharField(max_length=250,default=u'',blank=True)
	relay_info =models.CharField(max_length=250,default=u'',blank=True)
	delays= models.CharField(max_length=250,default=u'',blank=True)
	dsn= models.CharField(max_length=250,default=u'',blank=True)
	status =  models.CharField(max_length=1)
	queue = models.ForeignKey(Queue,null=True,blank=True)
	checkin = models.DateTimeField(auto_now_add=True,editable=False)

	def __unicode__(self):
		return "%s [ %s ]" % (self.queue,self.label)
	
class Reject(models.Model):
	label = models.CharField(max_length=250,default=u'',blank=True)
	ident = models.ManyToManyField(MsgId,blank=True)
	checkin = models.DateTimeField(auto_now_add=True,editable=False)
	
