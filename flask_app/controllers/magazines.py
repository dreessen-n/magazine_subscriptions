# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt

# Import models class
from flask_app.models import user, magazine

# CRUD CREATE ROUTES
@app.route('/magazine/create', methods=['POST'])
def create_new_magazine():
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not magazine.Magazine.validate_form(request.form):
        # Redirect back to new magazine page
        return redirect('/magazine/new')
    # Create data dict based on request form
    # the keys must match exactly to the var in the query set
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['id']
    }
    magazine.Magazine.create_magazine(data)
    return redirect('/dashboard')

@app.route('/magazine/subscribe', methods=['POST'])
def add_subscribe_magazine():
    magazine.Magazine.subscribe(request.form)
    return redirect('/dashboard')

@app.route('/magazine/new')
def magazine_new():
    """Display the form to create a new magazine"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on user in session
    # the keys must match exactly to the var in the query set
    data = { 'id': session['id'] }
    # Call classmethod in models
    return render_template('new.html', user=user.User.get_user_by_id(data))

# CRUD READ ROUTES
@app.route('/magazine/show/<int:magazine_id>')
def magazine_show_one(magazine_id):
    """Show the magazine on a page"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on magazine_id
    # The keys must match exactly to the var in the query set
    data = { 'id': magazine_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('show.html', one_magazine=magazine.Magazine.get_one_magazine(data), user=user.User.get_user_by_id(data_user))


# CRUD UPDATE ROUTES
@app.route('/magazine/edit/<int:magazine_id>')
def edit_magazine(magazine_id):
    """Edit the magazine"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on magazine_id
    # The keys must match exactly to the var in the query set
    data = { 'id': magazine_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('edit.html', one_magazine=magazine.Magazine.get_one_magazine(data), user=user.User.get_user_by_id(data_user))

@app.route('/magazine/update', methods=['POST'])
def update_magazine():
    """Update magazine after editing"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not magazine.Magazine.validate_form(request.form):
        # Redirect back to new magazine page
        id = int(request.form['id'])
        return redirect(f'/magazine/edit/{id}')
    # Create data dict based on magazine_id
    # The keys must match exactly to the var in the query set
    data = {
        'id': int(request.form['id']),
        'title': request.form['title'],
        'description': request.form['description'],
    }
    # Call classmethod in models
    magazine.Magazine.update_magazine(data)
    # Redirect to dashboard after update
    return redirect('/dashboard')

# CRUD DELETE ROUTES
@app.route('/magazine/delete/<int:magazine_id>', methods=['POST'])
def delete_magazine(magazine_id):
    """Delete magazine if session user created"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on magazine_id
    # The keys must match exactly to the var in the query set
    data = { 'id': magazine_id }
    # Call classmethod in models
    magazine.Magazine.delete_magazine(data)
    # Redirect back to dashboard after deletion
    return redirect('/dashboard')

@app.route('/magazine/unsubscribe', methods=['POST'])
def un_subscribe_magazine():
    magazine.Magazine.unsubscribe(request.form)
    return redirect('/dashboard')

