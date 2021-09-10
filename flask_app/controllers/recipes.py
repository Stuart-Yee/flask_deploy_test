from flask import Flask, render_template, redirect, session, flash, request
from flask_app import app
from flask_app.models.recipe import Recipe

@app.route("/dashboard")
def dashboard():
    if session["logged_in"]:
        recipes = Recipe.get_all()
        return render_template("dashboard.html", recipes = recipes)
    else:
        return redirect("/")

@app.route("/recipes/new", methods=["POST", "GET"])
def create_recipe():
    if session["logged_in"] == False | session["logged_in"] == None:
        return redirect("/")
    if request.method == "GET":
        edit = False
        return render_template("save_recipe.html", edit=edit)
    elif request.method == "POST":
        if not Recipe.validate_recipe(request.form):
            return redirect("/recipes/new")
        else:
            data = {}
            for key in request.form:
                data[key] = request.form[key]
            data["user_id"] = session["user_id"]
            print(data["user_id"])
            print(session["user_id"])
            if data["under_30"] == "True":
                data["under_30"] = True
            else:
                data["under_30"] = False
            new_id = Recipe.create_recipe(data)
            return redirect(f"/recipes/{new_id}")
    else:
        return "I'm sorry, that request method isn't allowed."


@app.route("/recipes/<int:recipe_id>")
def show_recipe(recipe_id):
    #todo show recipe
    data = {"id": recipe_id}
    recipe = Recipe.find_by_id(data)
    return render_template("show_recipe.html", recipe=recipe)

@app.route("/recipes/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    id_data = {"id": recipe_id}
    recipe = Recipe.find_by_id(id_data)
    if session["user_id"] != recipe.user_id:
        return redirect("/logout")
    if request.method == "GET":
        edit = True
        data = {"id" : recipe_id}
        recipe = Recipe.find_by_id(data)
        return render_template("save_recipe.html", edit=edit, recipe=recipe)
    elif request.method == "POST":
        data = {}
        for key in request.form:
            data[key] = request.form[key]
        data["id"] = recipe_id
        if data["under_30"] == "True":
            data["under_30"] = True
        else:
            data["under_30"] = False
            if Recipe.validate_recipe(data):
                Recipe.update_recipe(data)
                return redirect(f"/recipes/{recipe_id}")
            else:
                return redirect(f"/recipes/edit/{recipe_id}")
    else:
        return "I'm sorry, that request method isn't allowed"

@app.route("/recipes/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    id_data = {"id": recipe_id}
    recipe = Recipe.find_by_id(id_data)
    if session["user_id"] != recipe.user_id:
        return redirect("/logout")
    else:
        Recipe.delete_recipe(id_data)
    return redirect("/dashboard")