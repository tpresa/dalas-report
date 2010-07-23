
from django.contrib import admin


from dalas.maillog.models import *




class AdminQueue(admin.ModelAdmin):
	list_display=('ident','label','done','action')
	search_fields = ['ident','label']
	list_filter = ['label']
	
	def action(self,item):
		return "Delete Queue | Make some..."
admin.site.register(Queue,AdminQueue)

admin.site.register(Reject)



class AdminRecipient(admin.ModelAdmin):
	list_display=('queue','msglist','label','email_to','orig_to','delays','relay_info','status','action')
	search_fields = ['label','email_to','orig_to','delays']
	list_filter = ['status','label','email_to','orig_to','relay_info','dsn']
	
	def msglist(self,item):
		return "..."
	msglist.short_description = "Attached to..."
		
	def action(self,item):
		return "Make some action..."
		
admin.site.register(Recipient,AdminRecipient)




class AdminEvent(admin.ModelAdmin):
	list_display=('msglist','label','raw_month','raw_day','raw_time','raw_hostname','raw_actor','raw_actor_cmd','raw_pid','action')
	filter_horizontal = ['queue']
	search_fields = ['raw_month','raw_day','raw_time','raw_hostname','raw_actor','raw_actor_cmd']
	list_filter = ['label','raw_month','raw_day','raw_hostname','raw_actor','raw_actor_cmd']
	
	
	def msglist(self,item):
		lista = ' '
		for i in item.queue.all():
			lista+=i.ident
			lista+='<br>'
		return lista
		
	msglist.short_description = "Attached to..."
	msglist.allow_tags = True
	
	def action(self,item):
		return "Make some action..."
		
admin.site.register(Event,AdminEvent)




admin.site.register(MsgId)

class AdminMsg(admin.ModelAdmin):
	list_display=['subject','done','resume']
	search_fields = ['subject','start','average','end','done']
	list_filter = ['done']
	
	def resume(self,item):
		return "<p><b>Start: %s</b></p><p><b>Stop: %s</b></p><p><b>Average: %s</b></p>" % (item.start,item.end,item.average)
		
	resume.short_description = "History.."
	resume.allow_tags = True
	
admin.site.register(Msg,AdminMsg)

