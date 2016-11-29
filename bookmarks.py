from flask import Flask, request, redirect, render_template
from mongo import save_catalog, get_catalogs, save_links, get_links, delete_bookmark, delete_catalogs

app = Flask(__name__)


@app.route('/')
def index():
    docs = get_catalogs()
    links_list = []
    for doc in docs:
        links = get_links(doc['name'])
        item = {'ca': doc['name'], 'caid': doc['_id'], 'links': links}
        links_list.append(item)
    print links_list

    return render_template('index.html', cas=docs, links=links_list)


@app.route('/newcatalog', methods=['POST'])
def new_catalog():
    if request.form['catalog']:
        print request.form['catalog']
        doc = {'name': request.form['catalog'], 'owner': ''}
        save_catalog(doc)
    return redirect('/')


@app.route('/newbookmark', methods=['POST'])
def new_bookmark():
    catalog_select = request.form['catalogselect']
    markname = request.form['markname']
    linkadd = request.form['linkadd']

    if catalog_select and markname and linkadd:
        doc = {'name': markname, 'catalog': catalog_select, 'link': linkadd, 'owner': ''}
        save_links(doc)
    return redirect('/')


@app.route('/delbookmark/<objid>')
def del_bookmark(objid):
    delete_bookmark(objid)
    return redirect('/')


@app.route('/delcatalog/<ca>')
def del_catalog(ca):
    print ca
    delete_bookmark(None, ca)
    delete_catalogs(ca)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
