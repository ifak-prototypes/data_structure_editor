<template>
  <v-dialog v-model="model.visible" width="800px">
    <v-card>
      <v-card-title class="grey lighten-4 py-4 title">

        {{ model.title }}

      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field

                label="Repository URL*"
                v-model="model.url"
                required

              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field

                label="Local Name of the Repository*"
                v-model="model.name"
                required

              ></v-text-field>
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
          @click="$emit('save', model.id)"
          >Clone Repository</v-btn>

        <v-btn flat color="primary"
          @click="model.visible=false"
          >Cancel</v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'dialog-clone',
  props: ['model']
}
</script>

<style>
</style>
