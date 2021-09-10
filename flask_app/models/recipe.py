from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.made_on = data["made_on"]
        self.under_30 = data["under_30"]
        self.created_on = data["created_on"]
        self.updated_on = data["updated_on"]
        self.user_id = data["user_id"]

    #query methods

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL("recipes").query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        if len(results) < 1:
            return False
        else:
            return cls(results[0])

    @classmethod
    def create_recipe(cls, data):
        for row in data:
            print(row, data[row])
        query = "INSERT INTO recipes (name, description, instructions, made_on, under_30, created_on, updated_on, recipes.user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(made_on)s, %(under_30)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        for key in data:
            print(key, ":", data[key])
        query = "UPDATE recipes.recipes SET recipes.name=%(name)s, recipes.instructions=%(instructions)s, recipes.description=%(description)s, recipes.under_30=%(under_30)s, recipes.made_on=%(made_on)s, recipes.updated_on=NOW() WHERE recipes.id = %(id)s;"
        connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"
        connectToMySQL("recipes").query_db(query, data)


    #Validations
    @staticmethod
    def validate_recipe(recipe_info):
        valid_recipe = True
        if not 3 <= len(recipe_info["name"]) <= 255:
            valid_recipe = False
            flash("Name must be between 3 and 255 characters", "name")
        if not 20 <= len(recipe_info["description"]) <= 255:
            valid_recipe = False
            flash("Description must be between 20 and 255 characters", "description")
        if not 20 <= len(recipe_info["instructions"]) <= 255:
            valid_recipe = False
            flash("Instructions must be between 20 and 255 characters", "instructions")
        if recipe_info["made_on"] == None or recipe_info["made_on"] == "" or "made_on" not in recipe_info:
            valid_recipe = False
            flash("please pick a date", "date")
        return valid_recipe

