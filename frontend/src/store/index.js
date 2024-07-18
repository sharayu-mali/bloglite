import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user:null,
    followers:null,
    following:null
  },
  getters: {
  },
  mutations: {
    setuser (state,user) {
      state.user=user
    },
    set_followers (state,followers) {
      state.followers=followers
    }, 
    set_following (state,following) {
      state.following=following
    }
  },
  actions: {
  },
  modules: {
  }
})
