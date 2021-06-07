<template>
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
            <v-combobox
              :items="library_items"
              v-model = library_value
              label="Library Name"
              @change="function (item) { lnchanged(item) }"
            />
          </v-row>

          <v-row>
            <v-combobox
              :items="struct_items"
              v-model = struct_value
              label="Block Type"
              @change="function (item) { sichanged(item) }"
            />
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
            <small>*indicates required field</small>
          </v-row>

        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn flat color="primary"
          @click="save(); model.visible=false"
          >{{ model.button_save_title }}</v-btn>

        <v-btn flat color="primary"
          @click="model.visible=false"
          >Cancel</v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'dialog-create-or-edit-block-instance',
  components: {
  },
  props: ['model'],
  data: function () {
    return {
      library_items: [],
      struct_items: [],
      library_value: undefined,
      library_version: undefined,
      struct_value: undefined,
      structList: []
    }
  },
  methods: {
    updateStructList: function (listOfStructs) {
      this.structList = listOfStructs

      // update this.library_items
      this.library_items = []
      var repo, i
      var lib, k
      var str, l
      for (i = 0; i < this.structList.length; ++i) {
        repo = this.structList[i]
        for (k = 0; k < repo.Libraries.length; ++k) {
          lib = repo.Libraries[k]
          var libraryItem = {}
          libraryItem.text = repo.RepoName + '::' + lib.LibraryName
          libraryItem.value = {}
          libraryItem.value.id = lib.LibraryID
          libraryItem.value.version = lib.LibraryVersion
          libraryItem.value.name = lib.LibraryName
          libraryItem.value.struct_items = []
          for (l = 0; l < lib.Blocks.length; ++l) {
            str = lib.Blocks[l]
            var structItem = {}
            structItem.text = str.Name
            structItem.value = {}
            structItem.value.id = str.ID
            structItem.value.name = str.Name
            libraryItem.value.struct_items.push(structItem)
          }
          if (lib.Blocks.length > 0) {
            this.library_items.push(libraryItem)
          }
        }
      }

      // update the library and block fields
      var libIndex, blockIndex
      if (this.model.data._LibraryID !== undefined) {
        for (libIndex = 0; libIndex < this.library_items.length; ++libIndex) {
          var item = this.library_items[libIndex]
          if (item.value.id === this.model.data._LibraryID) {
            for (blockIndex = 0; blockIndex < item.value.struct_items.length; ++blockIndex) {
              var blockItem = item.value.struct_items[blockIndex]
              if (blockItem.value.id === this.model.data._BlockID) {
                this.library_value = item
                this.struct_items = item.value.struct_items
                this.struct_value = blockItem
              }
            }
          }
        }
      }
    },
    reset: function () {
      this.library_items = []
      this.struct_items = []
      this.library_value = undefined
      this.library_version = undefined
      this.struct_value = undefined
      this.structList = []
    },
    update: function () {
      this.block_list_all('data_structures', this.updateStructList)
    },
    lnchanged: function (item) {
      this.library_value = item
      this.struct_value = undefined
      this.structList = []
      this.struct_items = item.value.struct_items
    },
    sichanged: function (item) {
      this.struct_value = item
    },
    save: function () {
      this.model.data._LibraryID = this.library_value.value.id
      this.model.data._LibraryVersion = this.library_value.value.version
      this.model.data._LibraryName = this.library_value.value.name
      this.model.data._BlockID = this.struct_value.value.id
      this.model.data._BlockName = this.struct_value.value.name
      this.$emit('save')
    }
  }
}
</script>

<style>
</style>
