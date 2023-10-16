from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.filters import ListFilter


ModelAdmin.change_list_template = "admin/m_change_list.html"
ListFilter.template = "admin/m_filter.html"
