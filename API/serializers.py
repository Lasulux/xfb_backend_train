from rest_framework import serializers
import API.models as APIModels


class Base500Serializer(serializers.ModelSerializer):
    class Meta:
        model = APIModels.Base500Model
        fields = ("ErrorCd", "ErrorMsg")


class EmptyReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIModels.EmptyReturnModel
        exclude = ("id",)

class InjuryDictSerializer(serializers.ModelSerializer):
    class Meta:
        model=APIModels.InjuryDict
        exclude = ("id",)

class SearchPlayerSerializer(serializers.ModelSerializer):
    Injury = InjuryDictSerializer()
    class Meta:
        model = APIModels.SearchPlayerModel
        exclude = ("id",)
        

class SearchPlayersSerializer(serializers.ModelSerializer):
    Players = SearchPlayerSerializer(many=True)

    class Meta:
        model = APIModels.SearchPlayersModel
        exclude = ("id",)
