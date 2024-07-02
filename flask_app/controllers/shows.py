from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash


@app.route("/shows")
def shows():
    """This route displays all shows"""
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    shows = Show.retrieve_info()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_shows.html", shows=shows, user=user)


@app.get("/shows/new")
def new_show():
    """This route displays new show"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("new_show.html", user=user)


@app.get("/shows/<int:show_id>")
def show_details(show_id):
    """This route displays a shows info"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    show = Show.retrieve_by_id_with_user(show_id)
    user = User.find_by_user_id(session["user_id"])
    if show == None:
        return "No show information found"
    return render_template("show_details.html", show=show, user=user)


@app.post("/shows/create")
def create_show():
    """The route that processes the create form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    if not Show.form_is_valid(request.form):
        return redirect("/shows/new")

    print("*******************************")
    print(request.form)
    show_id = Show.create(request.form)
    # print("New Show:" + str(show_id))#
    return redirect("/shows")


@app.get("/shows/<int:show_id>/edit")
def edit_show(show_id):
    """This route displays edit form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    show = Show.retrieve_by_id_with_user(show_id)
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_show.html", show=show, user=user)


@app.post("/shows/update")
def update_show():
    """This route processes the Edit form"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    show_id = request.form["show_id"]

    if not Show.form_is_valid(request.form):
        return redirect(f"/shows/{show_id}/edit")

    Show.update(request.form)
    return redirect(f"/shows/{show_id}")


@app.post("/shows/<int:show_id>/delete")
def delete_show(show_id):
    """Deletes a show"""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")
    Show.delete_by_id(show_id)
    return redirect("/shows")
