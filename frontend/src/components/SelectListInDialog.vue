<template>
  <v-card>
    <v-toolbar dense color="blue darken-1" dark>
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="model.show_clone_button !== undefined" icon color="blue darken-3" small dark @click="$emit('clone')">
        <v-icon dense>cloud_download</v-icon>
      </v-btn>
      <v-btn icon color="blue darken-3" small dark @click="$emit('create')">
        <v-icon dense>add</v-icon>
      </v-btn>
    </v-toolbar>
    <v-list>
      <template v-for="(item, index) in model.items">
        <v-list-tile :key="index">
          <v-list-tile-content>
            <v-list-tile-title v-html="item.name"></v-list-tile-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-btn icon ripple @click="$emit('select', index)">
              <v-icon :style="{ color: item.color }">check_circle</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-action v-if="model.show_push_button !== undefined">
            <v-btn icon ripple @click="$emit('push', index)">
              <v-icon color="blue lighten-2">cloud_upload</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-action>
            <v-btn icon ripple @click="$emit('rename', item.name)">
              <v-icon color="green lighten-1">edit</v-icon>
            </v-btn>
          </v-list-tile-action>
          <v-list-tile-action>
            <v-btn icon ripple @click="$emit('delete', index)">
              <v-icon color="red lighten-1">delete</v-icon>
            </v-btn>
          </v-list-tile-action>
        </v-list-tile>
      </template>
    </v-list>
  </v-card>
</template>

<script>
export default {
  name: 'select-list-in-dialog',
  data: function () {
    return {
      title: 'The title',
      model: {
        items: [
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' },
          { name: 'test2', color: 'grey' }
        ]
      }
    }
  }
}
</script>
