<template>
  <v-dialog v-model="model.visible" persistent width="800px">
    <v-card>
      <v-card-title class="grey lighten-4 py-4 title">

        {{ model.title }}

      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field

                label="Username*"
                v-model="model.data.name"
                required
                prepend-icon="person"

              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field

                label="Password*"
                :type="'password'"
                v-model="model.data.password"
                required
                prepend-icon="lock"

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

        <v-btn flat primary large block
          class="grey lighten-2"
          @click="$emit('save', model.id)"
          >Login</v-btn>

        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {

  name: 'content-1',
  props: ['model']

}
</script>

<style>
</style>
