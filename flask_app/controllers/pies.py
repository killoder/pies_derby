from flask_app import app
from flask_app.models.user import User
from flask_app.models.pie import Pie
from flask import render_template, redirect, session, request, flash

@app.route('/add/pie')
def addPie():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(data)
        return render_template('addPie.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/pie', methods = ['POST'])
def createPie():
    if 'user_id' in session:
        if not Pie.validate_pie(request.form):
            return redirect(request.referrer)
        data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'user_id': session['user_id']
        }
        Pie.save(data)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/edit/pie/<int:id>')
def editPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        if loggedUser['id'] == pie['user_id']:
            return render_template('editPie.html', loggedUser = loggedUser, pie= pie)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/update/pie/<int:id>', methods = ['POST'])
def updatePie(id):
    if 'user_id' in session:
        data1 = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data1)
        pie = Pie.get_pie_by_id(data1)
        if loggedUser['id'] == pie['user_id']:
            if not Pie.validate_pie(request.form):
                return redirect(request.referrer)
            data = {
                'name': request.form['name'],
                'filling': request.form['filling'],
                'crust': request.form['crust'],
                'pie_id': id
            }
            Pie.update(data)
            return redirect('/dashboard')
        return redirect('/dashboard')
    return redirect('/')

@app.route('/pie/<int:id>')
def viewPie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        votesNum = Pie.get_pie_voters(data)
        loggedUserVotedPie = User.get_user_voted_pies(data)
        return render_template('viewPie.html', loggedUser = loggedUser, pie= pie, votesNum= votesNum,votedPie = loggedUserVotedPie)
    return redirect('/')

@app.route('/delete/pie/<int:id>')
def deletePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        pie = Pie.get_pie_by_id(data)
        if loggedUser['id'] == pie['user_id']:
            Pie.deleteAllVotes(data)
            Pie.delete(data)
            return redirect(request.referrer)
        return redirect('/dashboard')
    return redirect('/')

@app.route('/vote/<int:id>')
def votePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        votedPie = User.get_user_voted_pies(data)
        if id not in votedPie:
            Pie.addVote(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/unvote/<int:id>')
def unvotePie(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        Pie.unVote(data)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/derby')
def derby():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'pie_id': id
        }
        loggedUser = User.get_user_by_id(data)
        allPies = Pie.get_all()
        return render_template('derby.html', allPies=allPies, loggedUser=loggedUser)
    return redirect('/')