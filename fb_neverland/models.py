from __future__ import unicode_literals

from django.db import models




# Create your models here.
class User( models.Model ):

	uid = models.CharField(u'uid', max_length = 100, default="")
	first_name = models.CharField(u'first_name', max_length = 100, default="")
	last_name = models.CharField(u'last_name', max_length = 100, default="")
	nick_name = models.CharField(u'nick_name', max_length = 100, default="")
	age = models.IntegerField(u'first_name', default=20)
	location = models.CharField(u'location', max_length = 100, default="taiwan")
	gender = models.IntegerField(u'gender', default=0)
	relation_id = models.IntegerField(u'relation_id', default=-1)
	preferred_age_above = models.IntegerField(u'preferred_age_above' , default = 15)
	preferred_age_below = models.IntegerField(u'preferred_age_below' , default = 25)
	preferred_gender = models.IntegerField(u'preferred_gender', default=0)	
	flag = models.BooleanField(u'flag', default=False)
	current_relation_id = models.IntegerField(u'current_relation_id',default=-1)

class Profile_Pic( models.Model ):
	uid = models.CharField( u'uid', max_length = 100 )
	url = models.CharField( u'url', max_length = 100 )


class Relation( models.Model ):



	#rid = models.AutoField(u'rid', primary_key=True)
	uid1 = models.CharField(u'uid1', max_length=100, default = "")
	uid2 = models.CharField(u'uid2', max_length=100, default = "")
	msg12 = models.CharField( u'msg12', max_length = 100, default = "" )
	msg21 = models.CharField( u'msg21', max_length = 100, default = "" )
	img12 = models.CharField( u'img12', max_length = 200, default = "" )
	img21 = models.CharField( u'img21', max_length = 200, default = "" )	
	status1 = models.IntegerField( u'status1' , default = 0 )
	status2 = models.IntegerField( u'status2' , default = 0)
	#STATUS_NONE = 0
	#STATUS_YES  = 1
	#STATUS_NO   = 2
	#STATUS_GMM  = 3



class Handler:
	def __init__ ( self ):
		self.relation = Relation.objects
		self.user = User.objects
		self.profile_pic = Profile_Pic.objects

	def update_relation( self, relation ):
		rid = relation['rid']
		try:
			result = self.relation.get( rid = rid )
		except ObjectDoesNotExist:
			return { 'success': False, 'msg': 'rid not exists' }

		for k, v in relation.iteritems():
			if k not in result:
				return { 'success': False, 'msg': 'Contain invalid key ' + k }
			result[k] = v

		ret = result.save()
		if ret == 1:
			return { 'success': True }
		else:
			return { 'success': False, 'msg': 'update operation failed' }   


	def get_relation( self , rid ):
		result = self.relation.get( rid = rid )
		if result is None:
			return { 'success': False, 'msg': 'rid not exists' }
		ret = { 'success': True }
		ret['payload'] = result
		return ret

	def create_relation( self, uid1, uid2 ):
		relation = Relation( uid1 = uid1, uid2 = uid2 )
		relation.save()
		return relation.id

	def has_relation( self, uid1, uid2 ):
		if len( self.relation.all() ) == 0:
			return 0

		tmp = self.relation.filter( uid1 = uid1 ).filter( uid2 = uid2 )
		tmp2 = self.relation.filter( uid2 = uid1 ).filter( uid1 = uid2 )

		if tmp and tmp[0]['status1'] is None:
			return tmp[0]['rid']

		if tmp2 and tmp2[0]['status2'] is None:
			return tmp2[0]['rid']

		if tmp is None and tmp2 is None:
			return 0
		else:
			return -1

	def create_user( self, uid ):
		user = User( uid = uid )
		user.save()
		return { 'success': True }

	def check_user( self, uid ):
		result = self.user.get( uid = uid )
		if result is None:
			return { 'success': False, 'msg': 'User not exists' }
		return { 'success': True, 'flag': result.flag }

	def get_user_current_rid( self, uid ):
		result = self.user.get( uid = uid )
		if result is None:
			return { 'success': False, 'msg': 'User not exists' }
		return { 'success': True, 'rid': result[current_relation_id] }
	
	def update_user( self, uid , info ):
		result = self.user.get( uid = uid )
		if result is None:
			return { 'success': False, 'msg': 'User not exists' }

		for k, v in info.iteritems():
			#if k not in result:
			#	return { 'success': False, 'msg': 'Contain invalid field' + k }
			setattr( result, k, v )

		result.save()	
		return { 'success': True }

	def delete_user( self, uid ):
		result = self.user.get( uid = uid )
		if result is None:
			return { 'success': False, 'msg': 'User not exists' }

		result.delete()
		return { 'success': True }

	def get_random_user( self ):
		return self.user.order_by('?').first()



	def get_next_relation( self, uid ):
		nuid = get_random_user()['uid']
		round = 0
		while round < 5 and has_relation( uid, nuid ) == -1:
			nuid = get_random_user()['uid']
			round += 1

		if round >= 5:
			return { 'success': False, 'msg': 'No more match can be found' }

		rel = has_relation( uid, nuid )
		if rel is 0:
			rel = create_relation( uid, nuid )

		self.user[ uid ].current_relation_id = rel
		return rel



