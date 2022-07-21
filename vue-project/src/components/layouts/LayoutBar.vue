<template>
  <div>
    <v-app-bar color="grey-lighten-2">
      <v-app-bar-nav-icon @click="forceRerender()"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer
      color="grey-darken-2"
      v-model="drawer"
      :key="componentKey"
    >
      <v-list v-if="!isLogin" style="color: white" bg-color="grey-darken-2">
        <v-list-item
          v-for="(item, index) in items_logout"
          value="item.value"
          color="white"
          :key="index"
          link
          @click="this.$router.push(item.to)"
          >{{ item.title }}</v-list-item
        >
      </v-list>
      <v-list v-else style="color: white" bg-color="grey-darken-2">
        <v-list-item
          v-for="(item, index) in items_login"
          value="item.value"
          color="white"
          :key="index"
          link
          @click="this.$router.push(item.to)"
          >{{ item.title }}</v-list-item
        >
      </v-list>
    </v-navigation-drawer>
  </div>
</template>
<script>
export default {
  data() {
    return {
      componentKey: 0,
      drawer: false,
      isLogin: false,
      items_logout: [
        {
          title: 'Login',
          id: 2,
          icon: 'mdi-information',
          to: '/login',
        },
        {
          title: 'SingUp',
          id: 3,
          to: '/sign-up',
        },
      ],
      items_login: [
        {
          title: 'Home',
          id: 1,
          icon: 'mdi-home',
          to: '/',
        },
        {
          title: 'Board',
          id: 2,
          icon: 'mdi-information',
          to: '/',
        },
        {
          title: 'Info',
          id: 3,
          to: '/me',
        },
      ],
    };
  },
  methods: {
    forceRerender() {
      this.componentKey += 1;
      this.drawer = !this.drawer;
      this.isLogin = !!localStorage.getItem('jwt');
    },
  },
};
</script>
