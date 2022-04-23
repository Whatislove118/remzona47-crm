from rest_framework import serializers

from django.contrib.auth import get_user_model



User = get_user_model



# class MasterSerializer(serializers.ModelSerializer):
#     position = PositionSerializer(many=False)
    
#     class Meta:
#         model = Master
#         fields = '__all__'
#         read_only_fields = ('id', 'user', 'salary')
    
#     def create(self, validated_data):
#         position_data = validated_data.pop("position")
#         master = super().create(validated_data)
#         Position.objects.create(master=master, **position_data)
#         return master
        
