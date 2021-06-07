<template>
    <v-toolbar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      color="blue darken-3"
      dark
      app
      fixed
    >
      <v-toolbar-title style="" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="$emit('toggle_menu_visibility')"></v-toolbar-side-icon>
      </v-toolbar-title>
      <span>{{ title }}</span>
      <!--
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="search"
        label="Search"
        class="hidden-sm-and-down"
      ></v-text-field>
      -->
      <v-spacer></v-spacer>
      <!--
      <v-btn icon>
        <v-icon>apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>notifications</v-icon>
      </v-btn>
      <v-btn icon large>
        <v-avatar size="32px" tile>
          <img
            src="https://cdn.vuetifyjs.com/images/logos/logo.svg"
            alt="Vuetify"
          >
        </v-avatar>
      </v-btn>
      -->
    </v-toolbar>
</template>

<script>
export default {
  name: 'app-tool-bar',
  props: ['title']
}
</script>
