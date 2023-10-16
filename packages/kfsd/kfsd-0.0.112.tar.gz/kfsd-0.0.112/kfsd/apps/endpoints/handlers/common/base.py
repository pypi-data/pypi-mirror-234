from kfsd.apps.core.utils.dict import DictUtils

from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404


class BaseHandler:
    ARG_NAME_IDENTIFIER = "identifier"
    ARG_NAME_SERIALIZER = "serializer"
    ARG_NAME_MODELCLASS = "modelClass"
    ARG_NAME_ISDBFETCH = "isDBFetch"

    def __init__(self, **kwargs):
        self.__modelSerializer = DictUtils.get(kwargs, self.ARG_NAME_SERIALIZER)
        self.__modelClass = DictUtils.get(kwargs, self.ARG_NAME_MODELCLASS)
        self.__identifier = DictUtils.get(kwargs, self.ARG_NAME_IDENTIFIER)
        isDBFetch = DictUtils.get(kwargs, self.ARG_NAME_ISDBFETCH)
        self.__modelQS = self.getQS(self.__identifier) if isDBFetch else None
        self.__modelQSData = self.getModelQSDataFromDB() if isDBFetch else None

    def dbFetch(self):
        self.__modelQS = self.getQS(self.__identifier)
        self.__modelQSData = self.getModelQSDataFromDB()

    def getModelClass(self):
        return self.__modelClass

    def getQS(self, objIdentifier):
        return get_object_or_404(self.getModelClass(), identifier=objIdentifier)

    def exists(self):
        if self.getModelClass().objects.filter(identifier=self.__identifier).exists():
            return True
        return False

    def create(self, **kwargs):
        self.__modelQS = self.getModelClass().objects.create(**kwargs)
        self.__modelQSData = self.getModelQSDataFromDB()

    def update(self, kwargs):
        serializer = self.getModelSerializer()(
            self.getModelQS(), data=kwargs, partial=True
        )
        if serializer.is_valid():
            return serializer.save()
        raise ValidationError(serializer.errors, "bad_request")

    def delete(self):
        if self.exists():
            self.getModelQS().delete()

    def getModelQSData(self):
        return self.__modelQSData

    def setModelQSData(self, data):
        self.__modelQSData = data

    def setModelQS(self, instance):
        self.__modelQS = instance

    def getModelQS(self, refresh=False):
        if refresh:
            self.__modelQS = self.getQS(self.__identifier)
        return self.__modelQS

    def refreshModelQSData(self):
        self.__modelQSData = self.getModelQSDataFromDB()

    def getModelSerializer(self):
        return self.__modelSerializer

    def getIdentifier(self):
        return self.__identifier

    def getModelQSDataFromDB(self):
        serializedData = self.getModelSerializer()(self.getModelQS())
        return serializedData.data

    def getQStoSerializerMany(self, qs):
        serializedData = self.getModelSerializer()(qs, many=True)
        return serializedData

    def getIdentifiersQS(self, identifiers):
        query = Q(identifier__in=identifiers)
        return self.getModelClass().objects.distinct().filter(query)

    def getFilterQS(self, queries):
        return self.getModelClass().objects.distinct().filter(queries)

    def search(self, modelClass, queries):
        return modelClass.objects.distinct().filter(queries)
