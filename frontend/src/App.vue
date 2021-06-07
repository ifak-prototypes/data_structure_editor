<template>
  <div id="app">
  <v-app id="prod40">
    <data-structure-editor/>
  </v-app>
  </div>
</template>

<script>
// @ is an alias to /src
import DataStructureEditor from '@/views/DataStructureEditor.vue'

export default {
  name: 'home',
  components: {
    DataStructureEditor
  }
}
</script>
