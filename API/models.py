from django.db import models
from json import JSONDecoder

# from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Base500Model(models.Model):
    ErrorMsg = models.CharField()
    ErrorCd = models.IntegerField()


class EmptyReturnModel(models.Model):
    pass

class InjuryDict(models.Model):
    Active = models.BooleanField(null=False)
    Description = models.CharField(null=True)
    Date_of_injury = models.DateField(null=True)


class SearchPlayerModel(models.Model):
    # custom_dict = models.ForeignKey(CustomDict, on_delete=models.CASCADE)
    # 
    player_id = models.IntegerField()
    club_name = models.CharField(null=True)
    team_id = models.IntegerField(null=True)
    team_short_name = models.CharField(null=True)
    team_logo_url = models.URLField(null=True)
    surname = models.CharField(null=True)
    first_name = models.CharField(null=True)
    birthdate = models.DateField(null=True)
    alias = models.CharField(null=True)
    Injury = InjuryDict()



class SearchPlayersModel(models.Model):
    Players = models.ManyToManyField(SearchPlayerModel)
