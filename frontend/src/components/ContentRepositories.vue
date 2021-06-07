<template>
  <div>
    <v-container v-if="content_type=='repository'" fluid fill-width>
      <v-flex xs12>
        <select-list
          :model="itemlist"
          :title="model.repository.title"
          @select="function (index, name) { $emit('repository_list_all', name) }"
          @clone="show_dialog_clone"
          @create="show_dialog_create"
          @push="repository_push"
          @rename="show_dialog_rename"
          @delete="function (index, name) { $emit('repository_delete', name) }"
        />
      </v-flex>
    </v-container>
    <dialog-create
      :model="dialog.create"
      @save="$emit('repository_create', dialog.create.name); dialog.create.visible = false"
    />
    <dialog-clone
      :model="dialog.clone"
      @save="$emit('repository_clone', dialog.clone.name, dialog.clone.url); dialog.clone.visible = false"
    />
    <dialog-rename
      :model="dialog.rename"
      @save="$emit('repository_rename', dialog.rename.old_name, dialog.rename.new_name); dialog.rename.visible = false"
    />
  </div>
</template>

<script>
import SelectList from '@/components/SelectList.vue'
import DialogCreate from '@/components/DialogCreate.vue'
import DialogClone from '@/components/DialogClone.vue'
import DialogRename from '@/components/DialogRename.vue'
export default {
  name: 'content-repositories',
  components: {
    SelectList,
    DialogCreate,
    DialogClone,
    DialogRename
  },
  props: ['model', 'content_type'],
  data: function () {
    return {
      itemlist: {
        selected_index: undefined,
        selected_name: undefined,
        show_push_button: true,
        show_clone_button: true,
        items: []
      },
      dialog: {
        create: {
          title: 'Repository',
          visible: false,
          name: ''
        },
        rename: {
          title: 'Repository',
          visible: false,
          oldName: '',
          newName: ''
        },
        clone: {
          title: 'Clone a Repository',
          visible: false,
          name: '',
          url: ''
        }
      }
    }
  },
  methods: {
    set_model: function (m) {
      this.model = m
    },
    update: function () {
      // refresh the itemlist
      var repos = this.model.repository.list
      var i
      this.itemlist.items = []
      for (i = 0; i < repos.length; ++i) {
        var item = {}
        item.name = repos[i]
        item.color = 'grey'
        this.itemlist.items.push(item)
      }

      // highlight the selected item
      var name = this.model.repository.name
      if (name !== undefined) {
        var x
        for (x = 0; x < this.itemlist.items.length; ++x) {
          if (this.itemlist.items[x].name === name) {
            this.itemlist.items[x].color = 'blue'
            break
          }
        }
      }
    },
    show_dialog_create: function (ctype) {
      this.dialog.create.name = ''
      this.dialog.create.visible = true
    },
    show_dialog_clone: function (ctype) {
      this.dialog.clone.name = ''
      this.dialog.clone.visible = true
    },
    show_dialog_rename: function (index, oldName) {
      this.dialog.rename.old_name = oldName
      this.dialog.rename.new_name = ''
      this.dialog.rename.visible = true
    }
  }
}
</script>

<style>

</style>
