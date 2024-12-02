import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || '',
    displayMode: localStorage.getItem('displayMode') || 'grid'
  },
  mutations: {
    setToken (state, payload) {
      state.token = payload.token
      localStorage.setItem('token', payload.token)
    },
    setDisplayMode (state, display) {
      state.displayMode = display
      localStorage.setItem('displayMode', display)
    }
  },
  actions: {
    setToken ({ commit }, payload) {
      commit('setToken', payload)
    },
    setDisplayMode ({ commit }, display) {
      commit('setDisplayMode', display)
    }
  },
  getters: {
    token: state => state.token,
    displayMode: state => state.displayMode
  }
})
