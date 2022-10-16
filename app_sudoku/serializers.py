from rest_framework import serializers


class SudokuSerializer(serializers.Serializer):
    level = serializers.CharField(max_length=15)
    play_square = serializers.JSONField()
    full_square = serializers.JSONField()

    def create(self, validated_data):
        pass
