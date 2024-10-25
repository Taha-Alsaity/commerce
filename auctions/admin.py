from django.contrib import admin
from.models import User,CreateList,Category,AddBidd,Comments
# Register your models here.





admin.site.register(User)
admin.site.register(Category)
admin.site.register(CreateList)

admin.site.register(Comments)
admin.site.register(AddBidd)