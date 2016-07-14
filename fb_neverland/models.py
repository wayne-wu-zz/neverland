from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class User( models.Model ):

    GENDER_ALL = 0
    GENDER_MALE = 1
    GENDER_FEMAILE = 2

    uid = models.CharField(u'uid', max_length = 100, default="")
    first_name = models.CharField(u'first_name', max_length = 100, default="")
    last_name = models.CharField(u'last_name', max_length = 100, default="")
    nick_name = models.CharField(u'nick_name', max_length = 100, default="")
    age = models.IntegerField(u'first_name', default=20)
    location = models.CharField(u'location', max_length = 100, default="taiwan")
    gender = models.IntegerField(u'gender', default=GENDER_ALL)
    relation_id = models.IntegerField(u'relation_id', default=-1)
    preferred_age_above = models.IntegerField(u'preferred_age_above' , default = 15)
    preferred_age_below = models.IntegerField(u'preferred_age_below' , default = 25)
    preferred_gender = models.IntegerField(u'preferred_gender', default=GENDER_ALL)  
    flag = models.BooleanField(u'flag', default=False)
    current_relation_id = models.IntegerField(u'current_relation_id',default=-1)
    temp = models.CharField( u'temp', max_length= 100, default="null" )
    state = models.CharField( u'state', max_length = 100, default="" )
    profile_pic = models.CharField( u'profile_pic' , max_length=300, default="" )

class Relation( models.Model ):
    uid1 = models.CharField(u'uid1', max_length=100, default = "")
    uid2 = models.CharField(u'uid2', max_length=100, default = "")
    msg12 = models.CharField( u'msg12', max_length = 100, default = "" )
    msg21 = models.CharField( u'msg21', max_length = 100, default = "" )
    img12 = models.CharField( u'img12', max_length = 300, default = "" )
    img21 = models.CharField( u'img21', max_length = 300, default = "" )    
    status1 = models.IntegerField( u'status1' , default = 0 )
    status2 = models.IntegerField( u'status2' , default = 0)

class Handler:
    def __init__ ( self ):
        self.relation = Relation.objects
        self.user = User.objects

    def update_relation( self, rid, relation ):
        try:
            result = self.relation.get( id = rid )
        except ObjectDoesNotExist:
            return { 'success': False, 'msg': 'id not exists' }

        for k, v in relation.iteritems():
            setattr( result, k , v )

        result.save()
        return { 'success': True }


    def get_relation( self , rid ):
        try:
            result = self.relation.get( id = rid )
        except ObjectDoesNotExist:
            return None
        
        return result

    def create_relation( self, uid1, uid2 ):
        relation = Relation( uid1 = uid1, uid2 = uid2 
            , img12 = self.get_user( uid1 ).profile_pic
            , img21 = self.get_user( uid2 ).profile_pic
        )
        relation.save()
        return relation.id

    def has_relation( self, uid1, uid2 ):
        if uid1 == uid2 or not self.get_user(uid1).flag or not self.get_user(uid2).flag:
            return -1
        if len( self.relation.all() ) == 0:
            return 0
        try:
            tmp = self.relation.filter( uid1 = uid1 ).filter( uid2 = uid2 )
        except ObjectDoesNotExist:
            tmp = []

        try:
            tmp2 = self.relation.filter( uid2 = uid1 ).filter( uid1 = uid2 )
        except ObjectDoesNotExist:
            tmp2 = []

        if len(tmp) > 0:
            if tmp.status1 == 2 or tmp.status2 == 2:
                return -1
            if tmp.status1 == tmp.status2 and tmp.status1 == 1   
                return -1

        if len(tmp2) > 0:
            if tmp2.status1 == 2 or tmp2.status2 == 2:
                return -1
            if tmp2.status1 == tmp2.status2 and tmp2.status1 == 1   
                return -1



        if len(tmp) == 0 and len(tmp2) == 0:
            return 0 


        if len(tmp) :
            return tmp[0].id

        if len(tmp2):
            return tmp2[0].id
            
        return -1

    def get_user( self, uid ):
        #try:
        result = self.user.get( uid = uid )
        #except ObjectDoesNotExist:
        #    user = User( uid = uid )
        #    user.save()
        #    return user

        return result

    def is_exists( self, uid ):
        try:
            result = self.user.get( uid = uid )
            return True
        except ObjectDoesNotExist:
            return False

    def create_user( self, uid ):
        user = User( uid = uid )
        user.save()
        return { 'success': True }

    def check_user( self, uid ):
        try:
            result = self.user.get( uid = uid )
        except ObjectDoesNotExist:
            self.create_user( uid ) 
            return { 'success': True, 'flag': False }

        return { 'success': True, 'flag': result.flag }

    def get_user_current_rid( self, uid ):
        try:
            result = self.user.get( uid = uid )
        except ObjectDoesNotExist:
            return False

        return result.current_relation_id 
    
    def update_user( self, uid , info ):
        try:
            result = self.user.get( uid = uid )
        except ObjectDoesNotExist:
            return { 'success': False, 'msg': 'User not exists' }

        for k, v in info.iteritems():
            setattr( result, k, v )

        result.save()   
        return { 'success': True }

    def delete_user( self, uid ):
        try:
            result = self.user.get( uid = uid )
        except ObjectDoesNotExist:
            return { 'success': False, 'msg': 'User not exists' }

        result.delete()
        return { 'success': True }

    def get_random_user( self ):
        return self.user.order_by('?').first()


    def get_next_relation( self, uid ):
        nuid = self.get_random_user().uid
        round = 0
        while round < 10 and self.has_relation( uid, nuid ) == -1:
            nuid = self.get_random_user().uid
            round += 1

        if round >= 10:
            return None

        rel = self.has_relation( uid, nuid )
        if rel is 0:
            rel = self.create_relation( uid, nuid )

        try:
            result = self.user.get( uid = uid )
        except ObjectDoesNotExist:
            return None

        setattr( result, 'current_relation_id' , rel )
        result.save()
        
        return rel

