import pytest

from core.serializers import RetrieveUpdateSerializer


@pytest.mark.django_db
def test_user_profile(client, get_credentials, user):
	"""Тест просмотра профиля"""
	response = client.get(
		path='/core/profile',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == RetrieveUpdateSerializer(user).data
