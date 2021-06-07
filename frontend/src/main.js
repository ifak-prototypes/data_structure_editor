import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

import '../node_modules/vuetify/dist/vuetify.min.css'
import '../node_modules/material-design-icons/iconfont/material-icons.css'

Vue.config.productionTip = false
Vue.use(Vuetify)
Vue.prototype.$http = axios

Vue.mixin({
  methods: {
    file_read: function (name, model, callback) {
      this.$http
        .get('http://localhost:8081/dse/api/v1/file/read/' + model.ctype + '/' + model.repository.name + '/' + name)
        .then((response) => {
          model.file.content = JSON.parse(response.data.value)
        })
        .then(() => {
          if (callback !== undefined) {
            callback()
          }
        })
        .catch((e) => {
          alert(e)
        })
    },
    struct_list_all: function (ctype, callback) {
      this.$http
        .get('http://localhost:8081/dse/api/v1/repository/list_all_structs/' + ctype)
        .then((response) => {
          callback(response.data.value)
        })
        .catch((e) => {
          alert(e)
        })
    },
    block_list_all: function (ctype, callback) {
      this.$http
        .get('http://localhost:8081/dse/api/v1/repository/list_all_blocks/' + ctype)
        .then((response) => {
          callback(response.data.value)
        })
        .catch((e) => {
          alert(e)
        })
    },
    uuid: function () {
      var d = new Date().getTime()
      var d2 = (performance && performance.now && (performance.now() * 1000)) || 0
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16
        if (d > 0) {
          r = (d + r) % 16 | 0
          d = Math.floor(d / 16)
        } else {
          r = (d2 + r) % 16 | 0
          d2 = Math.floor(d2 / 16)
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
      })
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
