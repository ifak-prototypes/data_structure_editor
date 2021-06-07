<template>
  <div>
    <app-menu
      :visible="menuVisible"
      :items="menuItems"
      @action="on_app_menu_action"
    />
    <app-tool-bar
      title="ifak Data Structure and Equipment Interface Editor"
      @toggle_menu_visibility="menuVisible = !menuVisible"
    />
    <v-content>
      <login :model="content['login']" @save="on_login" />
      <template v-if="login">

        <content-empty
          :model="content[ctype]"
        />
        <content-repositories
          ref = "repositories"
          :content_type = "content_type"
          :model = "content[ctype]"
          @repository_list_all = "repository_list_all"
          @repository_create = "repository_create"
          @repository_clone = "repository_clone"
          @repository_rename = "repository_rename"
          @repository_delete = "repository_delete"
        />
        <content-files
          ref="files"
          :content_type = "content_type"
          :model="content[ctype]"
          @file_list_all = "file_list_all"
          @file_create = "file_create"
          @file_create_ed = "file_create"
          @file_rename = "file_rename"
          @file_delete = "file_delete"
        />
        <content-entries
          ref="entries"
          :content_type = "content_type"
          :model = "content[ctype]"
          @entry_list_all = "entry_list_all"
          @file_write = "file_write"
        />

        <content-block-instance-entries
          ref="bi_entries"
          :content_type = "content_type"
          :model = "content[ctype]"
          @entry_list_all = "entry_list_all"
          @file_write = "file_write"
        />

        <content-blocks
          ref="blocks"
          :content_type = "content_type"
          :model = "content[ctype]"
          @block_list_all = "block_list_all"
          @file_write = "file_write"
        />

      </template>
    </v-content>
  </div>
</template>

<script>
// @ is an alias to /src
import AppMenu from '@/components/AppMenu.vue'
import AppToolBar from '@/components/AppToolBar.vue'
import Login from '@/components/Login.vue'
import ContentEmpty from '@/components/ContentEmpty.vue'
import ContentRepositories from '@/components/ContentRepositories.vue'
import ContentFiles from '@/components/ContentFiles.vue'
import ContentEntries from '@/components/ContentEntries.vue'
import ContentBlockInstanceEntries from '@/components/ContentBlockInstanceEntries.vue'
import ContentBlocks from '@/components/ContentBlocks.vue'

export default {
  name: 'dse',
  components: {
    AppMenu,
    AppToolBar,
    Login,
    ContentEmpty,
    ContentRepositories,
    ContentFiles,
    ContentEntries,
    ContentBlockInstanceEntries,
    ContentBlocks
  },
  data: function () {
    return {
      login: false,
      userRights: [],
      ctype: 'empty',
      content_type: undefined,
      menuVisible: true,
      menuItems: [
        {
          icon: 'settings_input_component',
          'icon-alt': 'settings_input_component',
          text: 'Data Structure and Block Libraries',
          model: false,
          ctype: 'empty',
          subMenuItems: [
            { text: ' ... Library Folders', ctype: 'data_structures', content_type: 'repository' },
            { text: ' ... Libraries', ctype: 'data_structures', content_type: 'file' },
            { text: ' ... Data Structure Definitions', ctype: 'data_structures', content_type: 'entry' },
            { text: ' ... Data Block Definitions', ctype: 'data_structures', content_type: 'block' }
          ]
        },
        {
          icon: 'account_balance',
          'icon-alt': 'account_balance',
          text: 'Equipment Type Interfaces',
          model: false,
          ctype: 'empty',
          subMenuItems: [
            { text: ' ... Repositories', ctype: 'equipment_interfaces', content_type: 'repository' },
            { text: ' ... Equipment Interface Descriptions', ctype: 'equipment_interfaces', content_type: 'file' },
            { text: ' ... Data Block Instances', ctype: 'equipment_interfaces', content_type: 'entry' }
          ]
        },
        { icon: 'supervisor_account', text: 'User Management', ctype: 'c3' },
        { icon: 'settings_applications', text: 'Configuration', ctype: 'c4' },
        { icon: 'account_circle', text: 'Logout', ctype: 'c5' }
      ],
      content: {
        login: {
          id: 'loginDialog',
          title: 'Please Login',
          data: {
            name: 'admin',
            password: '$if@73gd'
          },
          visible: true
        },
        empty: {
          content_type: 'empty'
        },
        data_structures: {
          ctype: 'data_structures',
          repository: {
            title: 'Data Structure and Block Library Folders',
            name: undefined,
            list: []
          },
          file: {
            title: 'Data Structure and Block Libraries',
            name: undefined,
            list: [],
            content: {}
          },
          entry: {
            title: 'Data Structure Definitions',
            name: undefined
          },
          block: {
            title: 'Data Block Definitions',
            name: undefined
          }
        },
        equipment_interfaces: {
          ctype: 'equipment_interfaces',
          title: 'Equipment Interface',
          repository: {
            title: 'Equipment Description Folders',
            name: undefined,
            list: []
          },
          file: {
            title: 'Equipment Description Files',
            name: undefined,
            list: [],
            content: undefined
          },
          entry: {
            title: 'Data Block Instances',
            name: undefined,
            list: [],
            content: undefined
          }
        }
      }
    }
  },
  methods: {
    on_app_menu_action: function (ctype, contentType) {
      var init = false
      if (this.ctype !== ctype) {
        this.ctype = ctype
        init = true
      }
      this.content_type = contentType
      if (this.content_type === 'repository') {
        if (init === true) {
          this.content[ctype].repository.name = undefined
          this.content[ctype].repository.list = []
        }
        this.$refs.repositories.set_model(this.content[ctype])
        this.repository_list_all(this.content[ctype].repository.name)
      } else if (this.content_type === 'file') {
        if (init === true) {
          this.content[ctype].file.name = undefined
          this.content[ctype].file.list = []
          this.content[ctype].file.content = {}
        }
        if (this.content[ctype].repository.name !== undefined) {
          this.$refs.files.set_model(this.content[ctype])
          this.$refs.files.update()
          this.file_list_all(this.content[ctype].file.name)
        } else {
          alert('First please select a repository!')
          this.on_app_menu_action(ctype, 'repository')
        }
      } else if (this.content_type === 'entry' && this.ctype === 'data_structures') {
        if (init === true) {
          this.content[ctype].entry.name = undefined
        }
        if (this.content[ctype].repository.name !== undefined) {
          if (this.content[ctype].file.name !== undefined) {
            this.$refs.entries.set_model(this.content[ctype])
            this.$refs.entries.update()
          } else {
            alert('First please select a library!')
            this.on_app_menu_action(ctype, 'file')
          }
        } else {
          alert('First please select a repository!')
          this.on_app_menu_action(ctype, 'repository')
        }
      } else if (this.content_type === 'entry' && this.ctype === 'equipment_interfaces') {
        if (init === true) {
          this.content[ctype].entry.name = undefined
          this.content[ctype].entry.list = []
          this.content[ctype].entry.content = {}
        }
        if (this.content[ctype].repository.name !== undefined) {
          if (this.content[ctype].file.name !== undefined) {
            this.$refs.entries.set_model(this.content[ctype])
            this.$refs.bi_entries.update()
          } else {
            alert('First please select an equipment interface description!')
            this.on_app_menu_action(ctype, 'file')
          }
        } else {
          alert('First please select a repository!')
          this.on_app_menu_action(ctype, 'repository')
        }
      } else if (this.content_type === 'block') {
        if (this.content[ctype].repository.name !== undefined) {
          if (this.content[ctype].file.name !== undefined) {
            this.$refs.blocks.set_model(this.content[ctype])
            this.$refs.blocks.update()
          } else {
            alert('First please select a library!')
            this.on_app_menu_action(ctype, 'file')
          }
        } else {
          alert('First please select a repository!')
          this.on_app_menu_action(ctype, 'repository')
        }
      }
      if (ctype === 'c3') {
        alert('User management is not implemented.')
      } else if (ctype === 'c4') {
        alert('Configuration support is not implemented.')
      }
    },
    on_login: function (mymodel) {
      this.$http
        .post('http://localhost:8081/dse/api/v1/session', {
          name: this.content.login.data.name,
          password: this.content.login.data.password
        })
        .then((response) => {
          this.login = true
          this.content.login.visible = false
          this.userRights = response.data.value
        })
    },
    repository_list_all: function (name) {
      var ctype = this.ctype
      if (name === undefined || name !== this.content[ctype].repository.name) {
        this.$http
          .get('http://localhost:8081/dse/api/v1/repository/list_all/' + ctype)
          .then((response) => {
            this.content[ctype].repository.list = response.data.value
            this.content[ctype].repository.name = name
            this.$refs.repositories.update()

            // clean up dependent data
            this.content[ctype].file.name = undefined
            this.content[ctype].file.list = []
            this.content[ctype].file.content = undefined
            this.content[ctype].entry.name = undefined
            this.content[ctype].entry.list = []
            this.content[ctype].entry.content = undefined
          })
          .catch((e) => {
            alert(e)
          })
      }
    },
    repository_clone: function (name, url) {
      this.$http
        .post('http://localhost:8081/dse/api/v1/repository/clone/' + this.ctype, {
          name: name,
          url: url
        })
        .then((response) => {
          this.repository_list_all(name)
        })
        .catch((e) => {
          alert(e)
        })
    },
    repository_create: function (name) {
      this.$http
        .post('http://localhost:8081/dse/api/v1/repository/create/' + this.ctype + '/' + name)
        .then((response) => {
          this.repository_list_all(name)
        })
        .catch((e) => {
          alert(e)
        })
    },
    repository_push: function () {
      // POST /repository/push/<name>
      alert('Pushing to the source repository is planned, but currently not implemented')
    },
    repository_rename: function (oldName, newName) {
      this.$http
        .post('http://localhost:8081/dse/api/v1/repository/rename/' + this.ctype + '/' + oldName + '/' + newName)
        .then((response) => {
          this.repository_list_all(newName)
        })
        .catch((e) => {
          alert(e)
        })
    },
    repository_delete: function (name) {
      this.$http
        .delete('http://localhost:8081/dse/api/v1/repository/delete/' + this.ctype + '/' + name)
        .then((response) => {
          this.repository_list_all(undefined)
        })
        .catch((e) => {
          alert(e)
        })
    },
    file_list_all: function (fileName) {
      var ctype = this.ctype
      var repo = this.content[ctype].repository.name
      if (fileName === undefined || fileName !== this.content[ctype].file.name) {
        this.$http
          .get('http://localhost:8081/dse/api/v1/file/list_all/' + ctype + '/' + repo)
          .then((response) => {
            this.content[ctype].file.list = response.data.value
            this.content[ctype].file.name = fileName
            this.$refs.files.update()

            // clean up dependent data
            this.content[ctype].entry.name = undefined
            this.content[ctype].entry.list = []
            this.content[ctype].entry.content = undefined
          })
          .then(() => {
            if (fileName !== undefined) {
              this.entry_list_all(undefined)
            }
          })
          .catch((e) => {
            alert(e)
          })
      }
    },
    file_create: function (name, data) {
      var ctype = this.ctype
      var repo = this.content[ctype].repository.name
      this.$http
        .post('http://localhost:8081/dse/api/v1/file/write/' + ctype + '/' + repo + '/' + name, data)
        .then((response) => {
          this.file_list_all(name)
        })
        .catch((e) => {
          alert(e)
        })
    },
    file_rename: function (oldName, newName, data) {
      var ctype = this.ctype
      var repo = this.content[ctype].repository.name
      this.$http
        .post('http://localhost:8081/dse/api/v1/file/rename/' + ctype + '/' + repo + '/' + oldName + '/' + newName, data)
        .then((response) => {
          this.file_list_all(newName)
        })
        .catch((e) => {
          alert(e)
        })
    },
    file_write: function (name, callback) {
      var ctype = this.ctype
      var model = this.content[ctype]
      var repo = model.repository.name
      var content = model.file.content
      this.$http
        .post('http://localhost:8081/dse/api/v1/file/write/' + ctype + '/' + repo + '/' + name, content)
        .then((response) => {
          this.file_read(name, model, undefined)
        })
        .then(() => {
          if (callback !== undefined) {
            callback()
          }
        })
        .catch((e) => {
          alert(e)
        })
    },
    file_delete: function (name) {
      var ctype = this.ctype
      var repo = this.content[ctype].repository.name
      this.$http
        .delete('http://localhost:8081/dse/api/v1/file/delete/' + ctype + '/' + repo + '/' + name)
        .then((response) => {
          this.file_list_all(undefined)
        })
        .catch((e) => {
          alert(e)
        })
    },
    entry_list_all: function (name) {
      var ctype = this.ctype
      var model = this.content[ctype]
      model.entry.name = name
      this.file_read(model.file.name, model, () => {
        if (this.ctype === 'data_structures') {
          this.$refs.entries.update()
        } else if (this.ctype === 'equipment_interfaces') {
          this.$refs.bi_entries.update()
        }
      })
    },
    block_list_all: function (name) {
      var ctype = this.ctype
      var model = this.content[ctype]
      model.entry.name = name
      this.file_read(model.file.name, model, () => {
        this.$refs.blocks.update()
      })
    }
  }
}
</script>
