from rest_framework import serializers

from apps.my_auth.models import CustomUser
from tools.ids_encoder import encode_id

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Friend
        fields = '__all__'

    def create(self, validated_data):
        return Friend.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timeRequested = validated_data.get('timeRequested',
                                                    instance.timeRequested)
        instance.timeRespondedTo = validated_data.get('timeRespondedTo',
                                                      instance.timeRespondedTo)
        instance.friendOne = validated_data.get('friendOne',
                                                instance.friendOne)
        instance.friendTwo = validated_data.get('friendTwo',
                                                instance.friendTwo)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance

    def to_representation(self, instance):
        """
        Changes the id to hashed id before it sends it out
        """
        ret = super().to_representation(instance)

        if ret['id'] is not None:
            ret['id'] = encode_id(ret['id'])

        # Changes the friend id's to their usernames
        friendId = ret['friendOne']
        ret['friendOne'] = CustomUser.objects.get(id=friendId).username
        friendId = ret['friendTwo']
        ret['friendTwo'] = CustomUser.objects.get(id=friendId).username
        return ret