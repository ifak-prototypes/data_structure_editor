<template>
  <div>
  <v-dialog v-model="model.visible" width="800px">

    <v-card>
      <v-card-title class="grey lighten-4 py-4 title">

        {{ model.dialog_title }}

      </v-card-title>
      <v-card-text>
        <v-container>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                :label="model.label_name_title + '*'"
                v-model="model.data._Name"
                required

              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-textarea
                v-model="model.data._Description"
              >
                <template v-slot:label>
                  <div>
                    Description
                  </div>
                </template>
              </v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-textarea
                v-model="model.data._Comment"
              >
                <template v-slot:label>
                  <div>
                    Developer Comment
                  </div>
                </template>
              </v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <select-list
              :hide_select=true
              :model="itemlist"
              title="Data Block  Members"
              @select="struct_entry_select"
              @create="show_dialog_create"
              @rename="show_dialog_edit"
              @delete="struct_entry_delete"
            />
          </v-row>

          <v-row>
            <small>*indicates required field</small>
          </v-row>

        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn flat color="primary"
          @click="$emit('save'); model.visible=false"
          >{{ model.button_save_title }}</v-btn>

        <v-btn flat color="primary"
          @click="model.visible=false"
          >Cancel</v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>

  <dialog-create-or-edit-block-entry
    ref="create_or_edit_block_entry"
    :model="dialog.create"
    @save="block_entry_create_or_edit"
  />

  </div>
</template>

<script>
import SelectList from '@/components/SelectList.vue'
import DialogCreateOrEditBlockEntry from '@/components/DialogCreateOrEditBlockEntry'
export default {
  name: 'dialog-create-or-edit-block',
  components: {
    SelectList,
    DialogCreateOrEditBlockEntry
  },
  props: ['model'],
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
          label_name_title: 'Data Block Member Name',
          button_save_title: '',
          visible: false,
          data: {}
        }
      }
    }
  },
  methods: {
    update: function () {
      // update itemlist of DataEntrys
      this.itemlist.items = []
      if (this.model.data.DataEntry !== undefined) {
        var entries = this.model.data.DataEntry
        var i
        for (i = 0; i < entries.length; ++i) {
          var item = {}
          item.name = entries[i]._Name
          this.itemlist.items.push(item)
        }
        this.highlite_block_entry(-1)
      }
    },
    highlite_block_entry: function (index) {
      var x
      for (x = 0; x < this.itemlist.items.length; ++x) {
        if (x === index) {
          this.itemlist.items[x].color = 'blue'
        } else {
          this.itemlist.items[x].color = 'grey'
        }
      }
    },
    block_entry_select: function (index, name) {
      this.itemlist.selected_index = index
      this.dialog.selected_name = name
      this.highlite_block_entry(index)
    },
    show_dialog_create: function (index, name) {
      this.dialog.create.action_type = 'create'
      this.dialog.create.dialog_title = 'Create Data Block Member'
      this.dialog.create.button_save_title = 'OK'
      this.dialog.create.data = {
        _Name: '',
        _ID: this.uuid(),
        _Comment: '',
        _Description: ''
      }

      this.$refs.create_or_edit_block_entry.update()

      this.dialog.create.visible = true
    },
    show_dialog_edit: function (index, name) {
      this.block_entry_select(index, name)

      this.dialog.create.action_type = 'edit'
      this.dialog.create.dialog_title = 'Edit Data Block Member'
      this.dialog.create.button_save_title = 'OK'
      this.dialog.create.data = JSON.parse(JSON.stringify(this.model.data.DataEntry[this.itemlist.selected_index]))

      this.$refs.create_or_edit_block_entry.update()

      this.dialog.create.visible = true
    },
    block_entry_create_or_edit: function () {
      if (this.dialog.create.action_type === 'create') {
        if (!('DataEntry' in this.model.data)) {
          this.model.data['DataEntry'] = []
        }
        this.model.data.DataEntry.push(JSON.parse(JSON.stringify(this.dialog.create.data)))
        this.update()
        this.block_entry_select(this.itemlist.length, this.dialog.create.data._Name)
      } else {
        this.model.data.DataEntry[this.itemlist.selected_index] = JSON.parse(JSON.stringify(this.dialog.create.data))
        this.update()
        this.block_entry_select(this.itemlist.selected_index, this.itemlist.selected_name)
      }
    },
    block_entry_delete: function (index, name) {
      var blockElements = this.model.data.DataEntry
      var i
      for (i = 0; i < blockElements.length; ++i) {
        var blockElement = blockElements[i]
        if (name === blockElement._Name) {
          this.model.data.DataEntry.splice(i, 1)
          break
        }
      }

      this.update()
      this.block_entry_select(-1, undefined)

      this.$refs.create_or_edit_block_entry.update()

      this.$emit('save')
    }
  }
}
</script>

<style>
</style>
