from django.conf import settings
from post.models.post_models import Article
from rest_framework import serializers

class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "body", "image", "image_credit", "date_published", "date_created", "date_updated", "status", "read_time" ]
    
    def to_representation(self, instance):
        representation = super(ArticleSerializers, self).to_representation(instance)
        # Check the request is listview or DetailView
        # is_list_view = isinstance(self.instance, list)
        custom_response = []
        for dataObj in self.instance:
            custom_response.append(
                {
                    "object_id":dataObj.id,
                    "article":{
                        "title":dataObj.title,
                        "body":dataObj.body
                    },
                    "image_information":{
                        "image":dataObj.image,
                        "image_credit":dataObj.image_credit
                    },
                    "status":dataObj.status,
                    "read_time":dataObj.read_time+" min"
                }
            )
        representation.update(custom_response)
        return representation

