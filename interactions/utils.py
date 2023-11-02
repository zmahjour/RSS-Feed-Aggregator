from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


def create_interaction_with_generic_relation(
    user,
    object_model,
    object_id,
    interaction_model,
    failure_message,
    success_message,
    is_method=None,
    **kwargs
):
    content_type = ContentType.objects.get_for_model(object_model)
    object = get_object_or_404(object_model, pk=object_id)

    if is_method and is_method(user, content_type, object_id):
        return Response(
            data={"message": failure_message}, status=status.HTTP_400_BAD_REQUEST
        )

    interaction_model.objects.create(user=user, content_object=object, **kwargs)

    return Response(data={"message": success_message}, status=status.HTTP_201_CREATED)


def delete_interaction_with_generic_relation(
    user,
    object_model,
    object_id,
    interaction_model,
    failure_message,
    success_message,
    is_method=None,
):
    content_type = ContentType.objects.get_for_model(object_model)

    if is_method and not is_method(
        user=user, content_type=content_type, object_id=object_id
    ):
        return Response(
            data={"message": failure_message}, status=status.HTTP_400_BAD_REQUEST
        )

    interaction_model.objects.get(
        user=user, content_type=content_type, object_id=object_id
    ).delete()

    return Response(data={"message": success_message}, status=status.HTTP_200_OK)
