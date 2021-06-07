<template>
  <div>
    <v-container v-if="content_type=='file'" fluid fill-width>
      <v-flex xs12>
        <select-list
          :model="itemlist"
          :title="model.file.title"
          @select="function (index, name) { $emit('file_list_all', name) }"
          @create="show_dialog_create"
          @rename="show_dialog_rename"
          @delete="function (index, name) { $emit('file_delete', name) }"
          @download="download"
        />
      </v-flex>
    </v-container>
    <dialog-create-structure-library
      :model="dialog.create"
      @save="$emit('file_create', dialog.create.name, dialog.create.data); dialog.create.visible = false"
    />
    <dialog-create-equipment-description
      :model="dialog.create_ed"
      @save="$emit('file_create_ed', dialog.create_ed.name, dialog.create_ed.data); dialog.create_ed.visible = false"
    />
    <dialog-rename-structure-library
      :model="dialog.rename"
      @save="$emit('file_rename', dialog.rename.old_name, dialog.rename.name, dialog.rename.data); dialog.rename.visible = false"
    />
    <dialog-rename-equipment-description
      :model="dialog.rename_ed"
      @save="$emit('file_rename', dialog.rename_ed.old_name, dialog.rename_ed.name, dialog.rename_ed.data); dialog.rename_ed.visible = false"
    />
  </div>
</template>

<script>
import SelectList from '@/components/SelectList.vue'
import DialogCreateStructureLibrary from '@/components/DialogCreateStructureLibrary.vue'
import DialogCreateEquipmentDescription from '@/components/DialogCreateEquipmentDescription.vue'
import DialogRenameStructureLibrary from '@/components/DialogRenameStructureLibrary.vue'
import DialogRenameEquipmentDescription from '@/components/DialogRenameEquipmentDescription.vue'
export default {
  name: 'content-files',
  components: {
    SelectList,
    DialogCreateStructureLibrary,
    DialogCreateEquipmentDescription,
    DialogRenameStructureLibrary,
    DialogRenameEquipmentDescription
  },
  props: ['model', 'content_type'],
  data: function () {
    return {
      url: 'https://78.media.tumblr.com/tumblr_m39nv7PcCU1r326q7o1_500.png',
      itemlist: {
        selected_index: undefined,
        selected_name: undefined,
        items: []
      },
      dialog: {
        create: {
          title: 'Structure File',
          visible: false,
          name: '',
          data: undefined
        },
        create_ed: {
          title: 'Equipment Description',
          visible: false,
          name: '',
          data: undefined
        },
        rename: {
          title: 'Structure File',
          visible: false,
          name: '',
          data: undefined,
          old_name: ''
        },
        rename_ed: {
          title: 'Equipment Description',
          visible: false,
          name: '',
          data: undefined,
          old_name: ''
        }
      }
    }
  },
  methods: {
    set_model: function (m) {
      this.model = m
    },
    update: function () {
      // add source code downloader
      if (this.model.ctype === 'equipment_interfaces') {
        this.itemlist.show_download_button = true
      }

      // refresh the itemlist
      var files = this.model.file.list
      var i
      this.itemlist.items = []
      for (i = 0; i < files.length; ++i) {
        var item = {}
        item.name = files[i]
        item.color = 'grey'
        this.itemlist.items.push(item)
      }
      // highlight the selected item
      var name = this.model.file.name
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
    show_dialog_create: function () {
      this.$http
        .get('http://localhost:8081/dse/api/v1/file/read_template/' + this.model.ctype)
        .then((response) => {
          if (this.model.ctype === 'data_structures') {
            this.dialog.create.data = JSON.parse(response.data.value)
            this.dialog.create.name = ''
            this.dialog.create.visible = true
          } else if (this.model.ctype === 'equipment_interfaces') {
            this.dialog.create_ed.data = JSON.parse(response.data.value)
            this.dialog.create_ed.name = ''
            this.dialog.create_ed.visible = true
          }
        })
        .catch((e) => {
          alert(e)
        })
    },
    show_dialog_rename: function (index, oldName) {
      if (this.model.ctype === 'data_structures') {
        this.dialog.rename.old_name = oldName
        this.dialog.rename.name = oldName
        this.file_read(oldName, this.model, () => {
          this.dialog.rename.data = this.model.file.content
          this.dialog.rename.visible = true
        })
      } else if (this.model.ctype === 'equipment_interfaces') {
        this.dialog.rename_ed.old_name = oldName
        this.dialog.rename_ed.name = oldName
        this.file_read(oldName, this.model, () => {
          this.dialog.rename_ed.data = this.model.file.content
          this.dialog.rename_ed.visible = true
        })
      }
    },
    download: function (index, name) {
      this.$http({
        method: 'get',
        url: 'http://localhost:8081/download/' + this.model.repository.name + '/' + name,
        responseType: 'arraybuffer',
        withCredentials: true
      })
        .then(response => {
          this.forceFileDownload(response) // provide the fileName parameter which replaces file.png in forceFileDownload
        })
        .catch(() => console.log('error occured'))
    },
    forceFileDownload: function (response) {
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'generic_application.zip')
      document.body.appendChild(link)
      link.click()
    }
  }
}
</script>

<style>

</style>
