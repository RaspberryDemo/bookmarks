from flask import Flask, flash, request, redirect, render_template
from flask_bootstrap import Bootstrap
from datastore import *
from userdb import *
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

app = Flask(__name__)
Bootstrap(app)

lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'login'

lm.init_app(app)

app.secret_key = 'hard to guess'


@lm.user_loader
def load_user(user_id):
    user = User(user_id)
    return user


@app.route('/')
@login_required
def index():
    owner = current_user.username
    docs = get_catalogs(owner)
    links_list = []
    for doc in docs:
        links = get_links(doc['name'], owner)
        item = {'ca': doc['name'], 'caid': doc['_id'], 'links': links}
        links_list.append(item)

    return render_template('index.html', cas=docs, links=links_list)


@app.route('/ca/<caname>')
@login_required
def filter_ca(caname):
    owner = current_user.username
    alldoc = get_catalogs(owner)
    docs = get_catalogs_by_ca(caname, owner)
    links_list = []
    for doc in docs:
        links = get_links(doc['name'], owner)
        item = {'ca': doc['name'], 'caid': doc['_id'], 'links': links}
        links_list.append(item)

    return render_template('index.html', cas=alldoc, links=links_list)


@app.route('/search', methods=['POST'])
@login_required
def search_wildcard_links():
    key = request.form['searchkey']
    owner = current_user.username
    allcas = get_catalogs(owner)
    alllinks = get_links_wildcard(key, owner)
    alllinks = list(alllinks)
    cas = []
    for doc in alllinks:
        if doc['catalog'] not in cas:
            cas.append(doc['catalog'])
    links_list = []
    for ca in cas:
        links = [link for link in alllinks if ca == link['catalog']]
        item = {'ca': ca, 'caid': 'unknown', 'links': links}
        links_list.append(item)
    return render_template('index.html', cas=allcas, links=links_list)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logout')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if check_password(username, password):
            user = User(username)
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    rform = RegisterForm()
    if rform.validate_on_submit():
        r = add_user(rform.username.data, rform.password.data)
        if not r:
            flash('Username is token by others')
        else:
            flash('Register success')
    return render_template('register.html', form=rform)


@app.route('/newcatalog', methods=['POST'])
@login_required
def new_catalog():
    if request.form['catalog']:
        owner = current_user.username
        doc = {'name': request.form['catalog'], 'owner': owner}
        save_catalog(doc)
    return redirect('/')


@app.route('/newbookmark', methods=['POST'])
@login_required
def new_bookmark():
    catalog_select = request.form['catalogselect']
    markname = request.form['markname']
    linkadd = request.form['linkadd']
    owner = current_user.username

    if catalog_select and markname and linkadd:
        doc = {'name': markname, 'catalog': catalog_select,
               'link': linkadd, 'owner': owner, 'comments': ''}
        save_links(doc)
    return redirect('/')


@app.route('/delbookmark/<objid>')
@login_required
def del_bookmark(objid):
    delete_bookmark(objid)
    return redirect('/')


@app.route('/editbookmark/<objid>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(objid):
    owner = current_user.username
    docs = get_catalogs(owner)
    link = get_link_by_id(objid)

    from forms import EditBookmarkForm
    eform = EditBookmarkForm(catalogs_choice=link['catalog'], alias=link['name'],
                             link=link['link'], comments=link['comments'])
    eform.catalogs_choice.choices = [(d['name'], d['name']) for d in docs]

    action = '/editbookmark/%s' % (objid)

    if eform.validate_on_submit():
        update_bookmark(objid, eform.catalogs_choice.data, eform.alias.data, eform.link.data, eform.comments.data)
        return redirect('/')

    return render_template('editbookmark.html', form=eform, action=action)


@app.route('/delcatalog/<ca>')
@login_required
def del_catalog(ca):
    owner = current_user.username
    delete_bookmark(None, ca, owner)
    delete_catalogs(ca, owner)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
