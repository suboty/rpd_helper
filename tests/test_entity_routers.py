import os
import traceback

import requests
from app.logger import logger


class ErrorWhileTest(Exception):
    ...


def decorator_test(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in test.\n"
                         f"Exception: {e}.\n"
                         f"Traceback: {traceback.format_exc()}")
            raise ErrorWhileTest(f"Error in test. Exception: {e}")

    return wrapper


class CRUDRouter:
    def __init__(self, entity_name: str, entity_examples):
        self.entity_name = entity_name
        self.entity_examples = [x for x in entity_examples]

        # for test behaviour
        self.id_after_created = None

    @decorator_test
    def create(self):
        res = requests.post(
            url=f'http://{os.environ.get("HOST")}:{os.environ.get("PORT")}/{self.entity_name}/',
            json=self.entity_examples[0]
        ).json()
        self.id_after_created = res['id']

    @decorator_test
    def update(self):
        res = requests.patch(
            url=f'http://{os.environ.get("HOST")}:{os.environ.get("PORT")}/{self.entity_name}/{self.id_after_created}',
            json=self.entity_examples[1]
        ).json()

    @decorator_test
    def get(self):
        res = requests.get(
            url=f'http://{os.environ.get("HOST")}:{os.environ.get("PORT")}/{self.entity_name}/{self.id_after_created}'
        ).json()

        for key in self.entity_examples[1].keys():
            assert res[key] == self.entity_examples[1][key], 'Error while get request checking!'


def test_entity_router():
    if not os.environ.get('HOST') or not os.environ.get('PORT'):
        raise ErrorWhileTest('Not identified os variables for testing!')

    # Courses entity
    logger.info('Work with courses')
    courses_entity_router = CRUDRouter(
        entity_name='courses',
        entity_examples=[
            {
                "name": "Test name 1",
                "params": {'test_key': 'test_value'}
            },
            {
                "name": "Test name 2",
                "params": {'test_key': 'test_value'}
            }
        ]
    )

    courses_entity_router.create()
    courses_entity_router.update()
    courses_entity_router.get()

    logger.info(f'Work with courses is finish: {courses_entity_router.id_after_created}')

    # Competencies entity
    logger.info('Work with competencies')
    competencies_entity_router = CRUDRouter(
        entity_name='competencies',
        entity_examples=[
            {
                "courses_id": 1,
                "type": "Test type",
                "competencies": [
                    "competence 1"
                ]
            },
            {
                "courses_id": 1,
                "type": "Test type",
                "competencies": [
                    "competence 2"
                ]
            }
        ]
    )

    competencies_entity_router.create()
    competencies_entity_router.update()
    competencies_entity_router.get()

    # Documents entity
    logger.info('Work with documents')
    documents_entity_router = CRUDRouter(
        entity_name='documents',
        entity_examples=[
            {
                "courses_id": 1,
                "type": "Test type 1"
            },
            {
                "courses_id": 1,
                "type": "Test type 2"
            },
        ]
    )

    documents_entity_router.create()
    documents_entity_router.update()
    documents_entity_router.get()

    # Texts entity
    logger.info('Work with texts')
    texts_entity_router = CRUDRouter(
        entity_name='texts',
        entity_examples=[
            {
                "document_id": 1,
                "competencies_id": 1,
                "text": "Test text 1",
                "type": "Test type 1"
            },
            {
                "document_id": 1,
                "competencies_id": 1,
                "text": "Test text 111",
                "type": "Test type 1"
            }
        ]
    )

    texts_entity_router.create()
    texts_entity_router.update()
    texts_entity_router.get()
