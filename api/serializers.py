from rest_framework import serializers
from .models import Position

class PositionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ('id', )



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
        
