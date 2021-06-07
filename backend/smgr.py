
# TODO:
#   - make more in-line comments
#   - write a README.md
#   - evaluate session time out data (provided to the SessionManager constructor)

import exc
import hashlib
import json
import os
import time
import uuid

roles = ['admin', 'user']
admin_pwhash = 'de8a76f07ca3714fad8ae7487d264f859decfd938c89f18028e07beef063e1c8'  # $if@73gd  - DANGER: you should change it!!!
path_of_this_script = os.path.dirname(os.path.realpath(__file__))

os.chdir(path_of_this_script)


class SessionManager(object):
    def __init__(self):
        self.conf_dir = "conf"
        self.users_file_name = "users.json"
        self.users = {'admin': {'pwhash': admin_pwhash, 'role': 'admin'}}  # users = {name: {pwhash:, role: }}
        self.load_users()
        self.roles = {'admin': ['admin', 'user'],  # you can define special rights for users
                      'user':  ['user']}
        self.sessions = {}  # sessions = {id: {user:, session_object:, created:, used:}

    # Private methods

    def load_users(self):
        d = os.path.join(path_of_this_script, self.conf_dir)
        if not os.path.isdir(d):
            os.makedirs(d)
        fn = os.path.join(d, self.users_file_name)
        if os.path.isfile(fn):
            with open(fn, 'r') as f:
                self.users = json.load(f)

    def save_users(self):
        d = os.path.join(path_of_this_script, self.conf_dir)
        fn = os.path.join(d, self.users_file_name)
        with open(fn, 'w') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def check(self, id, right):
        if id in self.sessions.keys():
            user = self.sessions[str(id)]['user']
            role = self.users[user]['role']
            if right in self.roles[role]:
                return True
            else:
                raise exc.Error(403, "User {u} is not authorized to perform {r}!".format(u=user, r=right))
        else:
            raise exc.Error(401, "The session timed out or you are not logged in. Please log in again.")

    # session API: data = {name:, password:}

    def post_session(self, data, session_object):
        """login"""
        def account_is_valid(name, password):
            if name in self.users.keys():
                hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if hash == self.users[name]['pwhash']:
                    return True
                else:
                    raise exc.Error(401, "The provided password for user '{name}' is not correct.".format(name=name))
            else:
                raise exc.Error(401, "User '{name}' is unknown.".format(name=name))

        if account_is_valid(data['name'], data['password']):
            sid = str(uuid.uuid4())
            now = time.time()
            self.sessions[sid] = {'user': data['name'], 'session_object': session_object, 'created': now, 'used': now}
            role = self.users[data['name']]['role']
            rights = self.roles[role]
            return (sid, rights)

    def get_sessions(self, sid):
        if self.check(sid, 'admin'):
            retval = {}
            for k in self.sessions.keys():
                v = self.sessions[k]
                retval[k] = {'user': v['user'], 'created': v['created'], 'used': v['used']}
            return retval

    def delete_other_session(self, sid, other_sid):
        if self.check(sid, 'admin'):
            if sid != other_sid:
                s = self.sessions.pop(other_sid)
                return {'user': s['user'], 'created': s['created'], 'used': s['used']}
            else:
                raise exc.Error(403, "You can not explicitely delete your own session.")

    def delete_own_session(self, sid):
        """logout"""
        if self.check(sid, 'user'):
            s = self.sessions.pop(sid)
            return {'user': s['user'], 'created': s['created'], 'used': s['used']}

    # user API: data = {name:, password:, role: }

    def post_user(self, sid, data):
        if self.check(sid, 'admin'):
            if not data['role'] in self.roles.keys():
                raise exc.Error(500, "Role '{role}' is not a valid role in scope of this application.".format(role=data['role']))
            hash = hashlib.sha256(data['password']).hexdigest()
            user_data = {}
            user_data['pwhash'] = hash
            user_data['role'] = data['role']
            self.users[data['name']] = user_data
            self.save_users()
            return data

    def get_users(self, sid):
        if self.check(sid, 'admin'):
            return self.users

    def delete_user(self, sid, name):
        if self.check(sid, 'admin'):
            if name == 'admin':
                raise exc.Error(403, "You can't delete yourself as 'admin' user")
            self.users.pop(name, None)
