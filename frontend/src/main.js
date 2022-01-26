import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    pokemons: []
  },
  mutations: {
    setPokemons (state, data) {
      state.pokemons = Object.values(data)
      for (let i = 0; i < state.pokemons.length; i++) {
        state.pokemons[i].isEdit = false
      }
    },
    
    editPoke (state, secret) {
      state.secret = secret
    }
  },
  getters: {
    getPokemons: state => {
      return state.pokemons
    },
    getPokemon: (state) => (id) => {
      return state.pokemons.find(pokemon => pokemon.id === id)
    }
  }
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
