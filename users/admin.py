from django.contrib import admin
from .models import *
from django.db import models
admin.site.register( UserProfile )
admin.site.register( BookStatus )
admin.site.register( TenantStatus )
admin.site.register( Book )
admin.site.register( ComplainType )
admin.site.register( Complain )
admin.site.register( Comment )
admin.site.register( Shop )
admin.site.register( ProductStatus )
admin.site.register( Product )