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
              :items="categories"
              v-model = cb1_value
              label="Data Type Category"
              @change="function (item) { dtchanged(item, 'cb1') }"
            />
          </v-row>
          <v-row v-if="cb2_visible">
            <v-combobox
              :items="categories"
              v-model = cb2_value
              label="Data Type Category"
              @change="function (item) { dtchanged(item, 'cb2') }"
            />
          </v-row>
          <v-row v-if="cb3_visible">
            <v-combobox
              :items="reduced_categories"
              v-model = cb3_value
              label="Data Type Category"
              @change="function (item) { dtchanged(item, 'cb3') }"
            />
          </v-row>

          <v-row v-if="scalar_fields_visible">
            <v-combobox
              :items="scalar_items"
              v-model = scalar_value
              label="Scalar Data Type"
            />
          </v-row>

          <v-row v-if="struct_fields_visible">
            <v-combobox
              :items="library_items"
              v-model = library_value
              label="Library Name"
              @change="function (item) { lnchanged(item) }"
            />
          </v-row>
          <v-row v-if="struct_fields_visible">
            <v-combobox
              :items="struct_items"
              v-model = struct_value
              label="Struct Name"
              @change="function (item) { sichanged(item) }"
            />
          </v-row>

          <v-row>
            <v-combobox
              :items="direction_items"
              v-model = direction_value
              label="Direction"
            />
          </v-row>

          <v-row>
            <v-combobox
              :items="transmission_characteristic_items"
              v-model = transmission_characteristic_value
              label="Transmission Characteristic"
            />
          </v-row>

          <v-row>
            <v-combobox
              :items="access_items"
              v-model = access_value
              label="Access"
            />
          </v-row>

          <v-row>
            <v-combobox
              :items="persistence_items"
              v-model = persistence_value
              label="Persistence"
            />
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Value Range"
                v-model="model.data._ValueRange"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Default Value"
                v-model="model.data._DefaultValue"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Substitute Value"
                v-model="model.data._SubstituteValue"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Physical Unit"
                v-model="model.data._PhysicalUnit"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Conditions"
                v-model="model.data._Conditions"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-combobox
              :items="support_items"
              v-model = support_value
              label="Support"
            />
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Conditional Support"
                v-model="model.data._ConditionalSupport"
              ></v-text-field>
            <v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Value Semantics"
                v-model="model.data._ValueSemantics"
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
  name: 'dialog-create-or-block-structure-entry',
  components: {
  },
  props: ['model'],
  data: function () {
    return {
      itemlist: {
        selected_index: undefined,
        selected_name: undefined,
        items: []
      },
      categories: [
        { text: 'Scalar', value: 'Scalar' },
        { text: 'Struct', value: 'StructReference' },
        { text: 'List', value: 'List' }
      ],
      reduced_categories: [
        { text: 'Scalar', value: 'Scalar' },
        { text: 'Struct', value: 'StructReference' }
      ],
      scalar_items: [
        { text: 'float32', value: 'float32' },
        { text: 'float64', value: 'float64' },
        { text: 'int32', value: 'int32' },
        { text: 'int64', value: 'int64' },
        { text: 'string', value: 'string' }
      ],
      direction_items: [
        { text: 'in', value: 'IN' },
        { text: 'out', value: 'OUT' },
        { text: 'in + out', value: 'INOUT' }
      ],
      direction_value: undefined,
      transmission_characteristic_items: [
        { text: 'cyclic', value: 'cyclic' },
        { text: 'acyclic', value: 'acyclic' }
      ],
      transmission_characteristic_value: undefined,
      access_items: [
        { text: 'read', value: 'r' },
        { text: 'write', value: 'w' },
        { text: 'read/write', value: 'rw' }
      ],
      access_value: undefined,
      persistence_items: [
        { text: 'retain', value: 'retain' },
        { text: 'non-retain', value: 'non-retain' }
      ],
      persistence_value: undefined,
      support_items: [
        { text: 'optional', value: 'optional' },
        { text: 'mandatory', value: 'mandatory' },
        { text: 'conditional', value: 'conditional' }
      ],
      support_value: undefined,
      library_items: [],
      struct_items: [],
      cb2_visible: false,
      cb3_visible: false,
      scalar_fields_visible: false,
      struct_fields_visible: false,
      cb1_value: undefined,
      cb2_value: undefined,
      cb3_value: undefined,
      scalar_value: undefined,
      library_value: undefined,
      library_version: undefined,
      struct_value: undefined,
      structList: []
    }
  },
  methods: {
    updateBlockEntryProperties: function (propParent, propName, propCollection, defaultIndex) {
      var propValue
      if (propParent[propName] !== undefined) {
        var v = propParent[propName]
        var i = 0
        for (i = 0; i < propCollection.length; ++i) {
          if (propCollection[i].value === v) {
            propValue = propCollection[i]
            break
          }
        }
      } else {
        propValue = propCollection[defaultIndex]
        propParent[propName] = propCollection[defaultIndex].value
      }
      if (propName === '_Direction') {
        this.direction_value = propValue
      } else if (propName === '_TransmissionCharacteristic') {
        this.transmission_characteristic_value = propValue
      } else if (propName === '_Access') {
        this.access_value = propValue
      } else if (propName === '_Persistence') {
        this.persistence_value = propValue
      } else if (propName === '_Support') {
        this.support_value = propValue
      }
    },
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
          for (l = 0; l < lib.Structs.length; ++l) {
            str = lib.Structs[l]
            var structItem = {}
            structItem.text = str.Name
            structItem.value = {}
            structItem.value.id = str.ID
            structItem.value.name = str.Name
            libraryItem.value.struct_items.push(structItem)
          }
          this.library_items.push(libraryItem)
        }
      }

      // update the data type fields
      var x, y
      if ('Scalar' in this.model.data) {
        this.cb1_value = this.categories[0]
        this.scalar_fields_visible = true
        for (x = 0; x < this.scalar_items.length; ++x) {
          if (this.model.data.Scalar[0]._ScalarType === this.scalar_items[x].value) {
            this.scalar_value = this.scalar_items[x]
            break
          }
        }
      } else if ('StructReference' in this.model.data) {
        this.cb1_value = this.categories[1]
        this.struct_fields_visible = true
        for (x = 0; x < this.library_items.length; ++x) {
          if (this.library_items[x].value.id === this.model.data.StructReference[0]._LibraryID) {
            for (y = 0; y < this.library_items[x].value.struct_items.length; ++y) {
              if (this.library_items[x].value.struct_items[y].value.id === this.model.data.StructReference[0]._StructID) {
                this.library_value = this.library_items[x]
                this.struct_items = this.library_items[x].value.struct_items
                this.struct_value = this.library_items[x].value.struct_items[y]
              }
            }
          }
        }
      } else if ('List' in this.model.data) {
        this.cb1_value = this.categories[2]
        this.cb2_visible = true
        if ('Scalar' in this.model.data.List[0]) {
          this.cb2_value = this.categories[0]
          this.scalar_fields_visible = true
          for (x = 0; x < this.scalar_items.length; ++x) {
            if (this.model.data.List[0].Scalar[0]._ScalarType === this.scalar_items[x].value) {
              this.scalar_value = this.scalar_items[x]
              break
            }
          }
        } else if ('StructReference' in this.model.data.List[0]) {
          this.cb2_value = this.categories[1]
          this.struct_fields_visible = true
          for (x = 0; x < this.library_items.length; ++x) {
            if (this.library_items[x].value.id === this.model.data.List[0].StructReference[0]._LibraryID) {
              for (y = 0; y < this.library_items[x].value.struct_items.length; ++y) {
                if (this.library_items[x].value.struct_items[y].value.id === this.model.data.List[0].StructReference[0]._StructID) {
                  this.library_value = this.library_items[x]
                  this.struct_items = this.library_items[x].value.struct_items
                  this.struct_value = this.library_items[x].value.struct_items[y]
                }
              }
            }
          }
        } else if ('List' in this.model.data.List[0]) {
          this.cb2_value = this.categories[2]
          this.cb3_visible = true
          if ('Scalar' in this.model.data.List[0].List[0]) {
            this.cb3_value = this.categories[0]
            this.scalar_fields_visible = true
            for (x = 0; x < this.scalar_items.length; ++x) {
              if (this.model.data.List[0].List[0].Scalar[0]._ScalarType === this.scalar_items[x].value) {
                this.scalar_value = this.scalar_items[x]
                break
              }
            }
          } else if ('StructReference' in this.model.data.List[0].List[0]) {
            this.cb3_value = this.categories[1]
            this.struct_fields_visible = true
            for (x = 0; x < this.library_items.length; ++x) {
              if (this.library_items[x].value.id === this.model.data.List[0].List[0].StructReference[0]._LibraryID) {
                for (y = 0; y < this.library_items[x].value.struct_items.length; ++y) {
                  if (this.library_items[x].value.struct_items[y].value.id === this.model.data.List[0].List[0].StructReference[0]._StructID) {
                    this.library_value = this.library_items[x]
                    this.struct_items = this.library_items[x].value.struct_items
                    this.struct_value = this.library_items[x].value.struct_items[y]
                  }
                }
              }
            }
          }
        }
      }
      this.updateBlockEntryProperties(this.model.data, '_Direction', this.direction_items, 1)
      this.updateBlockEntryProperties(this.model.data, '_TransmissionCharacteristic', this.transmission_characteristic_items, 1)
      this.updateBlockEntryProperties(this.model.data, '_Access', this.access_items, 0)
      this.updateBlockEntryProperties(this.model.data, '_Persistence', this.persistence_items, 1)
      this.updateBlockEntryProperties(this.model.data, '_Support', this.support_items, 1)
      if (this.model.data._PhysicalUnit === undefined) {
        this.model.data._PhysicalUnit = 'None'
      }
    },
    update: function () {
      this.cb1_value = undefined
      this.cb2_visible = false
      this.cb3_visible = false
      this.scalar_fields_visible = false
      this.struct_fields_visible = false
      this.struct_list_all('data_structures', this.updateStructList)
    },
    lnchanged: function (item) {
      this.library_value = item
      this.struct_items = item.value.struct_items
    },
    sichanged: function (item) {
      this.struct_value = item
    },
    dtchanged: function (item, control) {
      if (control === 'cb1' && item.value === 'List') {
        this.cb2_visible = true
        this.cb3_visible = false
        this.scalar_fields_visible = false
        this.struct_fields_visible = false

        this.cb2_value = undefined
        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb1' && item.value === 'Scalar') {
        this.cb2_visible = false
        this.cb3_visible = false
        this.scalar_fields_visible = true
        this.struct_fields_visible = false

        this.cb2_value = undefined
        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb1' && item.value === 'StructReference') {
        this.cb2_visible = false
        this.cb3_visible = false
        this.scalar_fields_visible = false
        this.struct_fields_visible = true

        this.cb2_value = undefined
        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb2' && item.value === 'List') {
        this.cb2_visible = true
        this.cb3_visible = true
        this.scalar_fields_visible = false
        this.struct_fields_visible = false

        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb2' && item.value === 'Scalar') {
        this.cb2_visible = true
        this.cb3_visible = false
        this.scalar_fields_visible = true
        this.struct_fields_visible = false

        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb2' && item.value === 'StructReference') {
        this.cb2_visible = true
        this.cb3_visible = false
        this.scalar_fields_visible = false
        this.struct_fields_visible = true

        this.cb3_value = undefined
        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb3' && item.value === 'Scalar') {
        this.cb2_visible = true
        this.cb3_visible = true
        this.scalar_fields_visible = true
        this.struct_fields_visible = false

        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      } else if (control === 'cb3' && item.value === 'StructReference') {
        this.cb2_visible = true
        this.cb3_visible = true
        this.scalar_fields_visible = false
        this.struct_fields_visible = true

        this.scalar_value = undefined
        this.library_value = undefined
        this.struct_value = undefined
      }
    },
    appendDataType: function (o, v) {
      var r = {}
      if (v === 'List') {
        o.List = [r]
      } else if (v === 'Scalar') {
        o.Scalar = [r]
        r._ScalarType = this.scalar_value.value
      } else if (v === 'StructReference') {
        o.StructReference = [r]
        r._LibraryID = this.library_value.value.id
        r._LibraryVersion = this.library_value.value.version
        r._LibraryName = this.library_value.value.name
        r._StructID = this.struct_value.value.id
        r._StructName = this.struct_value.value.name
      }
      return r
    },
    computeDataTypes: function () {
      var x = this.model.data
      if (this.cb1_value !== undefined) {
        x = this.appendDataType(x, this.cb1_value.value)
      }
      if (this.cb2_value !== undefined) {
        x = this.appendDataType(x, this.cb2_value.value)
      }
      if (this.cb3_value !== undefined) {
        x = this.appendDataType(x, this.cb3_value.value)
      }
      return x
    },
    removeDataType: function (x) {
      if (Object.keys(x).includes('List')) {
        delete x.List
      } else if (Object.keys(x).includes('Scalar')) {
        delete x.Scalar
      } else if (Object.keys(x).includes('StructReference')) {
        delete x.StructReference
      }
    },
    save: function () {
      this.removeDataType(this.model.data)
      this.computeDataTypes()
      this.model.data._Direction = this.direction_value.value
      this.model.data._TransmissionCharacteristic = this.transmission_characteristic_value.value
      this.model.data._Access = this.access_value.value
      this.model.data._Persistence = this.persistence_value.value
      this.model.data._Support = this.support_value.value
      this.$emit('save')
    }
  }
}
</script>

<style>
</style>
