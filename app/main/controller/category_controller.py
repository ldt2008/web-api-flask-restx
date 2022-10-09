from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required, admin_token_required
from ..util.dto import CategoryDto
from ..service.category_service import save_new_category, update_a_category, get_all_category, get_a_category, delete_a_category
from typing import Dict, Tuple

api = CategoryDto.api
_category = CategoryDto.category


@api.route('/')
class CategoryList(Resource):
    @api.doc('list_of_category')
    @api.marshal_list_with(_category, envelope='data')
    def get(self):
        """List all category"""
        return get_all_category()

    @admin_token_required
    @api.expect(_category, validate=True)
    @api.response(201, 'Category successfully created.')
    @api.doc('create a new category')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Category """
        data = request.json
        return save_new_category(data=data)

    
@api.route('/<public_id>')
@api.param('public_id', 'The Category identifier')
@api.response(404, 'Category not found.')
class Category(Resource):
    @api.doc('get a category')
    @api.marshal_with(_category)
    def get(self, public_id):
        """get a category given its identifier"""
        category = get_a_category(public_id)
        if not category:
            api.abort(404)
        else:
            return category
    
    @admin_token_required
    @api.expect(_category, validate=True)
    @api.response(201, 'Category successfully updated.')
    @api.doc('update a category')
    def put(self, public_id) -> Tuple[Dict[str, str], int]:
        """Update a Category """
        data = request.json
        return update_a_category(public_id,data=data)

    @admin_token_required
    @api.response(201, 'Category successfully deleted.')
    @api.doc('delete a category')
    def delete(self, public_id) -> Tuple[Dict[str, str], int]:
        """Delete a Category """
        return delete_a_category(public_id)




