<template>
  <v-app>
    <LayoutFullVue></LayoutFullVue>
    <v-main><router-view></router-view></v-main>
    <FooFightVue></FooFightVue>
  </v-app>
</template>

<script>
import LayoutFullVue from './components/LayoutFull.vue';
import FooFightVue from './components/layouts/FooFight';

export default {
  name: 'App',

  components: {
    FooFightVue,
    LayoutFullVue,
  },

  data: () => ({
    //
  }),
};
</script>
