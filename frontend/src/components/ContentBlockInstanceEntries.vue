<template>
  <div>
    <v-container v-if="content_type=='entry' && model.ctype === 'equipment_interfaces'" fluid fill-width>
      <v-flex xs12>
        <select-list
          :model="itemlist"
          :title="model.entry.title"
          @create="show_dialog_create"
          @rename="show_dialog_edit"
          @select="struct_select"
          @delete="struct_delete"
        />
      </v-flex>
    </v-container>
    <dialog-create-or-edit-block-instance
      ref="entries_create"
      :model="dialog.create"
      @save="block_instance_create_or_edit"
    />
  </div>
</template>

<script>
import SelectList from '@/components/SelectList.vue'
import DialogCreateOrEditBlockInstance from '@/components/DialogCreateOrEditBlockInstance.vue'
export default {
  name: 'content-block-instance-entries',
  components: {
    SelectList,
    DialogCreateOrEditBlockInstance
  },
  props: ['model', 'content_type'],
  data: function () {
    return {
      itemlist: {
        selected_index: undefined,
        selected_name: undefined,
        items: []
      },
      dialog: {
        create: {
          action_type: '',
          dialog_title: '',
          label_name_title: 'Block Instance Name',
          button_save_title: '',
          visible: false,
          data: {}
        }
      }
    }
  },
  methods: {
    set_model: function (m) {
      this.model = m
    },
    update: function () {
      // initialize a container for data block elements
      if (this.model.file.content.EquipmentDescription[0].BlockInstance === undefined) {
        this.model.file.content.EquipmentDescription[0].BlockInstance = []
      }

      // refresh the itemlist
      var entries = this.model.file.content.EquipmentDescription[0].BlockInstance
      var i
      this.itemlist.items = []
      for (i = 0; i < entries.length; ++i) {
        var item = {}
        item.name = entries[i]._Name
        item.color = 'grey'
        this.itemlist.items.push(item)
      }

      // highlight the selected item
      var name = this.model.entry.name
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
    struct_select: function (index, name) {
      this.itemlist.selected_index = index
      this.itemlist.selected_name = name
      this.$emit('entry_list_all', this.itemlist.selected_name)
    },
    show_dialog_create: function () {
      this.dialog.create.action_type = 'create'
      this.dialog.create.data = {
        _Name: '',
        _ID: this.uuid(),
        _Comment: '',
        _Description: '',
        _LibraryID: '',
        _LibraryVersion: '',
        _LibraryName: '',
        _BlockID: '',
        _BlockName: ''
      }
      this.dialog.create.dialog_title = 'Create Block Instance'
      this.dialog.create.button_save_title = 'Create Block Instance'
      this.$refs.entries_create.reset()
      this.$refs.entries_create.update()
      this.dialog.create.visible = true
    },
    show_dialog_edit: function (index, name) {
      this.itemlist.selected_name = name
      var x = 0
      for (x = 0; x < this.itemlist.items.length; ++x) {
        if (this.itemlist.items[x].name === name) {
          this.itemlist.selected_index = x
          this.itemlist.selected_name = this.itemlist.items[x].name
          this.model.entry.name = name
          break
        }
      }
      this.dialog.create.action_type = 'edit'
      this.dialog.create.data = JSON.parse(JSON.stringify(this.model.file.content.EquipmentDescription[0].BlockInstance[this.itemlist.selected_index]))
      this.dialog.create.dialog_title = 'Edit Block Instance'
      this.dialog.create.button_save_title = 'Save Block Instance'
      this.$refs.entries_create.update()
      this.dialog.create.visible = true
      this.$emit('entry_list_all', this.itemlist.selected_name)
    },
    block_instance_create_or_edit: function () {
      if (this.model.ctype === 'equipment_interfaces') {
        if (this.dialog.create.action_type === 'create') {
          if (!('BlockInstance' in this.model.file.content.EquipmentDescription[0])) {
            this.model.file.content.EquipmentDescription[0]['BlockInstance'] = []
          }
          this.model.file.content.EquipmentDescription[0].BlockInstance.push(JSON.parse(JSON.stringify(this.dialog.create.data)))
        } else {
          this.model.file.content.EquipmentDescription[0].BlockInstance[this.itemlist.selected_index] = JSON.parse(JSON.stringify(this.dialog.create.data))
        }
        this.$emit('file_write', this.model.file.name, () => {
          this.model.entry.name = this.dialog.create.data._Name
          this.update()
        })
      }
    },
    struct_delete: function (index, name) {
      var structs = this.model.file.content.EquipmentDescription[0].BlockInstance
      var i
      for (i = 0; i < structs.length; ++i) {
        var struct = structs[i]
        if (name === struct._Name) {
          this.model.file.content.EquipmentDescription[0].BlockInstance.splice(i, 1)
          break
        }
      }
      this.$emit('file_write', this.model.file.name, () => {
        this.update()
      })
    }
  }
}
</script>

<style>

</style>
