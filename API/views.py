from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import parsers

# from django.http import HttpResponse
from API import serializers
from json import loads as json_loads
import APIFunctions
from TutorialUtils import HandleError


base_tags = {
    "Default": "00. Default",
    "Teams": "01: Teams",
    "PlayerProfile": "02: PlayerProfile",
    "Players": "03: Players",
    "Tests": "04: Tests",
    "Monitoring": "05: Monitoring",
    "Periodisation": "06: Planner-periodisation",
    "Conditioning": "06: Planner-conditioning",
    "Health": "06: Planner-health",
    "Wellness": "07: Wellness",
    "Additional": "99 additional",
}


# ############################################################
# # POST - ErrorGen
# ############################################################
# # SWAGGER block - START
# @swagger_auto_schema(
#     method="post",
#     tags=[base_tags["Additional"]],
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         description="",
#         properties={
#             "UserID": openapi.Schema(
#                 type=openapi.TYPE_STRING,
#                 description="User Object ID from Azure AD B2C",
#                 default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#             ),
#             "LangID": openapi.Schema(
#                 type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
#             ),
#             "ErrorCd": openapi.Schema(type=openapi.TYPE_INTEGER, default=0),
#         },
#     ),
#     manual_parameters=[],
#     operation_summary="Search for all player by name",
#     responses={500: serializers.Base500Serializer},
# )
# # SWAGGER block - END
# @api_view(["POST"])
# @parser_classes([parsers.JSONParser])
# def ErrorGen(request) -> Response:
#     data = None
#     try:
#         data = json_loads(request.body)
#         runner = APIFunctions.ErrorGen(cd=data["ErrorCd"])
#         out = runner.run()
#         del runner
#         return Response(data=out)
#     except Exception as e:
#         return Response(status=500, data=HandleError(e=e, input=data))


############################################################
# POST - SearchAllPlayers
############################################################
# SWAGGER block - START
@swagger_auto_schema(
    method="post",
    tags=[base_tags["Default"]],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="",
        properties={
            "UserID": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User Object ID from Azure AD B2C",
                default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ),
            "LangID": openapi.Schema(
                type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
            ),
            "SearchParam": openapi.Schema(type=openapi.TYPE_STRING, description="player name to search for"),
        },
    ),
    manual_parameters=[],
    operation_summary="Search for all player by name",
    responses={500: serializers.Base500Serializer, 200: serializers.SearchPlayersSerializer},
)
# SWAGGER block - END
@api_view(["POST"])
@parser_classes([parsers.JSONParser])
def SearchPlayers(request) -> Response:
    data = None
    try:
        data = json_loads(request.body)
        runner = APIFunctions.SearchPlayer(UserOID=data["UserID"], search_param=data["SearchParam"])
        out = runner.run()
        del runner
        return Response(data=out)
    except Exception as e:
        return Response(status=500, data=HandleError(e=e, input=data))



############################################################
# POST - AddPlayer
############################################################
# SWAGGER block - START
@swagger_auto_schema(
    method="post",
    tags=[base_tags["Default"]],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="",
        properties={
            "UserID": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User Object ID from Azure AD B2C",
                default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ),
            "LangID": openapi.Schema(
                type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
            ),
            "PlayerId": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identification number"),
            "ClubName": openapi.Schema(type=openapi.TYPE_STRING, description="Club name"),
            "TeamId": openapi.Schema(type=openapi.TYPE_INTEGER, description="Team identification number"),
            "TeamShortName": openapi.Schema(type=openapi.TYPE_STRING, description="Short name of team"),
            "Surname": openapi.Schema(type=openapi.TYPE_STRING, description="Family name"),
            "FirstName": openapi.Schema(type=openapi.TYPE_STRING, description="Given name"),
            "Birthdate": openapi.Schema(type=openapi.TYPE_STRING, description="Time of birth"),
            "Alias": openapi.Schema(type=openapi.TYPE_STRING, description="Full name"),
            "TeamLogoUrl": openapi.Schema(type=openapi.TYPE_STRING, description="URL for team logo"),
        },
    ),
    manual_parameters=[],
    operation_summary="Add a player with the input values",
    responses={500: serializers.Base500Serializer, 200: serializers.SearchPlayersSerializer},
)
# SWAGGER block - END
@api_view(["POST"])
@parser_classes([parsers.JSONParser])
def AddPlayer(request) -> Response:
    data = None
    try:
        data = json_loads(request.body)
        # my_information = {'name': 'Dionysia', 'age': 28, 'location': 'Athens'}
        runner = APIFunctions.AddPlayer(UserOID=data["UserID"], add_param_dict={"player_id":data["PlayerId"],"club_name":data["ClubName"],"team_id":data["TeamId"],"team_short_name":data["TeamShortName"],"surname":data["Surname"],"first_name":data["FirstName"],"birthdate":data["Birthdate"],"alias":data["Alias"],"team_logo_url":data["TeamLogoUrl"]})
        out = runner.run()
        del runner
        return Response(data=out)
    except Exception as e:
        return Response(status=500, data=HandleError(e=e, input=data))



############################################################
# POST - RemovePlayer
############################################################
# SWAGGER block - START
@swagger_auto_schema(
    method="post",
    tags=[base_tags["Default"]],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="",
        properties={
            "UserID": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User Object ID from Azure AD B2C",
                default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ),
            "LangID": openapi.Schema(
                type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
            ),
            "FieldName": openapi.Schema(type=openapi.TYPE_STRING, description="Which field are you using for searching"),
            "Value": openapi.Schema(type=openapi.TYPE_STRING, description="The rows where the chosen field has this value will be deleted"),
        },
    ),
    manual_parameters=[],
    operation_summary="Remove players with the input values",
    responses={500: serializers.Base500Serializer, 200: serializers.SearchPlayersSerializer},
)
# SWAGGER block - END
@api_view(["POST"])
@parser_classes([parsers.JSONParser])
def RemovePlayer(request) -> Response:
    data = None
    try:
        data = json_loads(request.body)
        runner = APIFunctions.RemovePlayer(UserOID=data["UserID"], key_param=data["FieldName"], value_param=data["Value"])
        out = runner.run()
        del runner
        return Response(data=out)
    except Exception as e:
        return Response(status=500, data=HandleError(e=e, input=data))



############################################################
# POST - UpdatePlayer
############################################################
# SWAGGER block - START
@swagger_auto_schema(
    method="post",
    tags=[base_tags["Default"]],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="",
        properties={
            "UserID": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User Object ID from Azure AD B2C",
                default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ),
            "LangID": openapi.Schema(
                type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
            ),
            "PlayerID": openapi.Schema(type=openapi.TYPE_INTEGER, description="Player identification number"),
            "FieldName": openapi.Schema(type=openapi.TYPE_STRING, description="Which field are you updating"),
            "Value": openapi.Schema(type=openapi.TYPE_STRING, description="The selected field will beupdated to this value"),
        },
    ),
    manual_parameters=[],
    operation_summary="Update the chosen field of the selected player",
    responses={500: serializers.Base500Serializer, 200: serializers.SearchPlayersSerializer},
)
# SWAGGER block - END
@api_view(["POST"])
@parser_classes([parsers.JSONParser])
def UpdatePlayer(request) -> Response:
    data = None
    try:
        data = json_loads(request.body)
        runner = APIFunctions.UpdatePlayer(UserOID=data["UserID"], playerkey_param=data["PlayerID"], key_param=data["FieldName"], value_param=data["Value"])
        out = runner.run()
        del runner
        return Response(data=out)
    except Exception as e:
        return Response(status=500, data=HandleError(e=e, input=data))



############################################################
# POST - SaveTeamPeriodisation
############################################################
# SWAGGER block - START
@swagger_auto_schema(
    method="post",
    tags=[base_tags["Periodisation"]],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description="",
        properties={
            "UserID": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="User Object ID from Azure AD B2C",
                default="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ),
            "LangID": openapi.Schema(
                type=openapi.TYPE_STRING, description="User language id from Azure AD B2C", default="hu"
            ),
            "values": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="",
                    properties={
                        "value1": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="team_periodisation_id", default=1, x_nullable=True
                        ),
                        "value2": openapi.Schema(type=openapi.TYPE_INTEGER, description="Team", default=5),
                    },
                ),
            ),
        },
    ),
    manual_parameters=[],
    operation_summary="Search for all player by name",
    responses={500: serializers.Base500Serializer, 200: serializers.EmptyReturnSerializer},
)
# SWAGGER block - END
@api_view(["POST"])
@parser_classes([parsers.JSONParser])
def SaveTeamPeriodisation(request) -> Response:
    data = None
    try:
        data = json_loads(request.body)
        return Response(data=data)
    except Exception as e:
        return Response(status=500, data=HandleError(e=e, input=data))
