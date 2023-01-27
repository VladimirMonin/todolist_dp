import pytest

from goals.serializers import GoalSerializer
from tests.factories import GoalFactory


@pytest.mark.django_db
def test_goal_create(client, get_credentials, user, goal_category):
	"""Создание цели"""
	data = {
		'title': 'title',
		'description': 'description',
		'user': user.id,
		'category': goal_category.id,
		'status': 2,
		'priority': 3,
		'due_date': '2022-11-15',
	}

	response = client.post(
		path='/goals/goal/create',
		HTTP_AUTHORIZATION=get_credentials,
		data=data,
		content_type='application/json'
	)

	assert response.status_code == 201
	assert response.data['title'] == data['title']
	assert response.data['description'] == data['description']
	assert response.data['category'] == data['category']
	assert response.data['status'] == data['status']
	assert response.data['priority'] == data['priority']
	assert response.data['due_date'] == data['due_date']


@pytest.mark.django_db
def test_goal_list(client, get_credentials, board_participant, goal_category):
	"""Список целей"""
	goals = GoalFactory.create_batch(10, user=board_participant.user, category=goal_category)

	response = client.get(
		path='/goals/goal/list',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == GoalSerializer(goals, many=True).data


@pytest.mark.django_db
def test_goal_retrieve(client, get_credentials, goal, user, board_participant):
	"""Просмотр цели"""
	response = client.get(
		path=f'/goals/goal/{goal.id}',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_goal_update(client, get_credentials, goal, board_participant):
	"""Обновление цели"""
	new_title = 'updated_title'

	response = client.patch(
		path=f'/goals/goal/{goal.id}',
		HTTP_AUTHORIZATION=get_credentials,
		data={'title': new_title},
		content_type='application/json'
	)

	assert response.status_code == 200
	assert response.data.get('title') == new_title


@pytest.mark.django_db
def test_goal_delete(client, get_credentials, goal, board_participant):
	"""Удаление цели"""
	response = client.delete(
		path=f'/goals/goal/{goal.id}',
		HTTP_AUTHORIZATION=get_credentials,
	)

	assert response.status_code == 204
	assert response.data is None
