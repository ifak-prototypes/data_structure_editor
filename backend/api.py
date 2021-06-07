import app
import bottle
import exc
import generator
import json
import os
import shutil
import smgr
import time
import traceback
import zipfile

# Global variables
# ---------------------------------------------------------------
# URI path element of the root of our application
base_path = '/dse/api/v1/'

# Object reference to the business logic and session management
# ---------------------------------------------------------------
sm = smgr.SessionManager()
bl = app.WebApplication(sm)


# Utility functions
# ---------------------------------------------------------------
def success(value):
    """ Returns a JSON based success message around the given value. """
    return json.dumps({"type": "SUCCESS", "value": value})

def error(exception):
    """ Provides an error message and sets the HTTP response (error) code.
    The default error code for exceptions is 500. """
    traceback.print_exc()
    if isinstance(exception, exc.Error):
        bottle.response.content_type = 'application/plain; charset=utf-8'
        bottle.response.status = exception.code
        return "ERROR: " + exception.message + "\n\n" + traceback.format_exc()
    else:
        raise exception

def sid():
    """ Returns the session id according to a bottle request. """
    return bottle.request.get_cookie("sid")


# Cross-Origin Resource Sharing (CORS)
# ---------------------------------------------------------------
# In bottle We create a hook, which adds all necessary headers for CORS.
# If CORS is wanted, then the following hook should be commented out.
@bottle.error(405)
def method_not_allowed(res):
    if bottle.request.method == 'OPTIONS' or bottle.request.method == 'POST':
        new_res = bottle.HTTPResponse()
        new_res.set_header('Access-Control-Allow-Origin', '*')
        return new_res
    res.headers['Allow'] += ', OPTIONS, POST'
    return bottle.request.app.default_error_handler(res)

@bottle.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    bottle.response.headers['Access-Control-Expose-Headers'] = 'Access-Control-Allow-Origin'

    # here instead of * you should use a URL like 'https://www.securai.de' in order to minize risks.
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'

    # this one can then access the following services.
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


# API for cookie-based session management
# ---------------------------------------------------------------
@bottle.post(base_path + 'session')
def post_session():
    """ This is the login function. """
    try:
        data = json.loads(bottle.request.body.read())  # {name, password}
        bottle.response.content_type = 'application/json; charset=utf-8'
        business_logic = app.WebApplication(sm)
        sid, rights = sm.post_session(data, business_logic)
        bottle.response.set_cookie("sid", sid)
        return success(rights)
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'sessions')
def get_sessions():
    """ Lists all active sessions."""
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.get_sessions(sid()))
    except Exception as e:
        return error(e)

@bottle.delete(base_path + 'session')
def delete_own_session():
    """ This is the logout function."""
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.delete_own_session(sid()))
    except Exception as e:
        return error(e)

@bottle.delete(base_path + 'session/<other_sid>')
def delete_other_session(other_sid):
    """ Deletion of sessions of other users."""
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.delete_other_session(sid(), other_sid))
    except Exception as e:
        return error(e)


# API for user management 
# ---------------------------------------------------------------
@bottle.post(base_path + 'user')
def post_user():
    try:
        data = json.loads(bottle.request.body.read())  # {name, password, role}
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.post_user(sid(), data))
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'users')
def get_users():
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.get_users(sid()))
    except Exception as e:
        return error(e)

@bottle.delete(base_path + 'user/<name>')
def delete_user(name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(sm.delete_user(sid(), name))
    except Exception as e:
        return error(e)


# API for repository handling 
# ---------------------------------------------------------------
@bottle.get(base_path + 'repository/list_all/<ctype>')
def repository_list_all(ctype):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.repository_list_all(sid(), ctype))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'repository/clone/<ctype>')
def repository_clone(ctype):
    try:
        data = json.loads(bottle.request.body.read())
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.repository_clone(sid(), ctype, data['name'], data['url']))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'repository/create/<ctype>/<name>')
def repository_create(ctype, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.repository_create(sid(), ctype, name))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'repository/rename/<ctype>/<old_name>/<new_name>')
def repository_rename(ctype, old_name, new_name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.repository_rename(sid(), ctype, old_name, new_name))
    except Exception as e:
        return error(e)

@bottle.delete(base_path + 'repository/delete/<ctype>/<name>')
def repository_delete(ctype, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.repository_delete(sid(), ctype, name))
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'repository/list_all_structs/<ctype>')
def struct_list_all(ctype):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.struct_list_all(sid(), ctype))
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'repository/list_all_blocks/<ctype>')
def block_list_all(ctype):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.block_list_all(sid(), ctype))
    except Exception as e:
        return error(e)


# API for XML file handling 
# ---------------------------------------------------------------
@bottle.get(base_path + 'file/list_all/<ctype>/<repo>')
def file_list_all(ctype, repo):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.file_list_all(sid(), ctype, repo))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'file/create/<ctype>/<repo>/<name>')
def file_create(ctype, repo, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.file_create(sid(), ctype, repo, name))
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'file/read/<ctype>/<repo>/<name>')
def file_read(ctype, repo, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.file_read(sid(), ctype, repo, name))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'file/write/<ctype>/<repo>/<name>')
def file_write(ctype, repo, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        data = bottle.request.body.read()
        return success(bl.file_write(sid(), ctype, repo, name, data))
    except Exception as e:
        return error(e)

@bottle.get(base_path + 'file/read_template/<ctype>')
def file_read_template(ctype):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.file_read_template(sid(), ctype))
    except Exception as e:
        return error(e)

@bottle.post(base_path + 'file/rename/<ctype>/<repo>/<old_name>/<new_name>')
def file_rename(ctype, repo, old_name, new_name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        data = bottle.request.body.read()
        return success(bl.file_rename(sid(), ctype, repo, old_name, new_name, data))
    except Exception as e:
        return error(e)

@bottle.delete(base_path + 'file/delete/<ctype>/<repo>/<name>')
def file_delete(ctype, repo, name):
    try:
        bottle.response.content_type = 'application/json; charset=utf-8'
        return success(bl.file_delete(sid(), ctype, repo, name))
    except Exception as e:
        return error(e)


# Download the generated file
# ---------------------------------------------------------------

@bottle.get('/download/<repo_name>/<equipment_description>')
def generate(repo_name, equipment_description):
    """ CAUTION: this is an unsafe operation not secured by the session token
        During implementation the session key was None, which obviously is a bug.
    """

    app_root = './data/application_framework/'
    if os.path.isdir(app_root):
        shutil.rmtree(app_root)

    app_dir = app_root + equipment_description
    os.makedirs(app_dir)

    orig_zip_file = './data/generic_application.zip'
    with zipfile.ZipFile(orig_zip_file, 'r') as zip_ref:
        zip_ref.extractall(app_dir)

    target_dir = './data/generated'
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)

    generated_file = './data/GenericEquipmentInterface.java'
    if os.path.isfile(generated_file):
        os.remove(generated_file)
    generator.generate(repo_name, equipment_description)
    shutil.copyfile(generated_file, os.path.join(app_dir, 'src', 'main', 'java', 'ai', 'aitia', 'demo', 'car_provider', 'controller', 'GenericEquipmentInterface.java'))

    generated_zip = './generated_application.zip'
    if os.path.isfile(os.path.join('data', generated_zip)):
        os.remove(os.path.join('data', generated_zip))
    cmd = 'cd ./data && zip -q -r {0} ./application_framework'.format(generated_zip)
    os.system(cmd)

    target_file = str(int(1000 * time.time())) + '.zip'
    shutil.copyfile('./data/generated_application.zip', target_dir + '/' + target_file)
    return bottle.static_file(target_file, root=target_dir)

# Static Routes
# ---------------------------------------------------------------

@bottle.get('/')
def index():
    return bottle.static_file("index.html", root='../frontend/dist')

@bottle.get('/favicon.ico')
def favicon():
    return bottle.static_file("favicon.ico", root='../frontend/dist')

@bottle.get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return bottle.static_file(filepath, root="../frontend/dist/css")

@bottle.get("/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return bottle.static_file(filepath, root="../frontend/dist/fonts")

@bottle.get("/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return bottle.static_file(filepath, root="../frontend/dist/img")

@bottle.get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return bottle.static_file(filepath, root="../frontend/dist/js")


# Start the bottle application
# ---------------------------------------------------------------

if __name__ == "__main__":
    bottle.run(host='localhost', port=8081, debug=True)  # developer test version
    # bottle.run(host='0.0.0.0', port=8081, debug=True)  # for deployment
