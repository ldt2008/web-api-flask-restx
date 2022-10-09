import uuid
import datetime

from app.main import db
from app.main.model.category import Category
from typing import Dict, Tuple


def save_new_category(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    category = Category.query.filter_by(name=data['name']).first()
    if not category:
        new_category = Category(
            public_id=str(uuid.uuid4()),
            name=data['name']
        )
        save_changes(new_category)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Category': new_category.public_id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Category already exists.',
        }
        return response_object, 409

def update_a_category(public_id, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    category = Category.query.filter_by(public_id=public_id).first()
    if category:
        category.name = data['name']
        save_changes(category)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Category not exists.',
        }
        return response_object, 409

def delete_a_category(public_id) -> Tuple[Dict[str, str], int]:
    category = Category.query.filter_by(public_id=public_id).first()
    if category:
        delete_category(category)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Category not exists.',
        }
        return response_object, 409


def get_all_category():
    return Category.query.all()

def get_a_category(public_id):
    return Category.query.filter_by(public_id=public_id).first()

def save_changes(data: Category) -> None:
    db.session.add(data)
    db.session.commit()

def delete_category(data: Category) -> None:
    db.session.delete(data)
    db.session.commit()

