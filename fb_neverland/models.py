from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User( models.Model ):
	fb_id = models.CharField(u'fb_id', max_length = 100)
	first_name = models.CharField(u'first_name', max_length = 100)
	last_name = models.CharField(u'last_name', max_length = 100)
	nick_name = models.CharField(u'nick_name', max_length = 100)
	profile_pic = models.CharField(u'profile_pic', max_length = 100)
	age = models.IntegerField(u'first_name', )
	local = models.CharField(u'first_name', max_length = 100)
	gender = models.IntegerField(u'first_name')
	relation_id = models.IntegerField(u'first_name')
	preferred_age_above = models.IntegerField(u'first_name')
	preferred_age_below = models.IntegerField(u'first_name')
	preferred_gender = models.IntegerField(u'first_name')	


class Relation( models.Model ):
	relation_id = models.IntegerField(u'relation_id')
	uid1 = models.IntegerField(u'uid1')

