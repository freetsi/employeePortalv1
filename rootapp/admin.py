from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User

from rootapp.models import Profile, Department, Report


class Employee(User):
	class Meta:
		proxy = True


class ProfileInline(admin.StackedInline):
	model = Profile
	fields = ['birth_date', 'phone', 'mobile', 'address', 'postcode', 'title', 'father_name', 'department', 'gender']
	readonly_fields = ['id']
	can_delete = False


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'department')
	search_fields = ('user',)

	def get_queryset(self, request):
		query = super(ProfileAdmin, self).get_queryset(request)
		filtered_query = query.filter(user__is_staff=False)
		return filtered_query


class EmployeeAdmin(admin.ModelAdmin):
	list_display = ['id','username', 'first_name', 'last_name', 'is_active', 'is_staff']
	list_display_links = ('username', 'first_name', 'last_name', )
	list_filter = ['is_active']
	search_fields = ('username', 'first_name', 'last_name',)
	# The negative sign indicate descending order
	ordering = ('username', )

	fields = ('id','username', 'is_active', 'is_staff', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', )
	readonly_fields = ('id', 'date_joined', 'last_login', )

	inlines = [ProfileInline]

	# class Media:
	# 	css = {
	# 		'all': ('css/admin_console.css',)
	# 	}

	# Overload the add permission check to disable creation of new entries for all
	# def has_add_permission(self, request, obj=None):
	# 	return False

	# Overload the delete permission check to disable deletions of entries for all
	def has_delete_permission(self, request, obj=None):
		return False

	# def get_sync_date(self, obj):
	# 	return obj.profile.sync_date

	def get_queryset(self, request):
		query = super(EmployeeAdmin, self).get_queryset(request)
		filtered_query = query.filter(is_staff=False)
		return filtered_query


class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('id','name',)
	search_fields = ('name',)
	list_display_links = ('name', )


class ReportAdmin(admin.ModelAdmin):
	list_display = ('user','title','priority')
	search_fields = ('name','priority')
	list_display_links = ('title', )


class LogEntryAdmin(admin.ModelAdmin):
	list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change')
	list_display_links = (None)
	date_hierarchy = 'action_time'

	def change(self, obj):
		return obj

	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False


admin.site.site_header = 'Employees Portal'
admin.site.index_title = 'Resource Administration'
admin.site.site_title = 'Employees Portal'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Employee, EmployeeAdmin)