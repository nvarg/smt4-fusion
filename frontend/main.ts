import Vue from 'vue';
import App from './App.vue';

Vue.config.productionTip = false;
Vue.prototype.$api = process.env.API || '';

new Vue({
  render: (h) => h(App),
}).$mount('#app');
