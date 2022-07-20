<template>
  <div>
    <v-app-bar color="grey-lighten-2">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer color="grey-darken-2" v-model="drawer">
      <v-list style="color: white" bg-color="grey-darken-2">
        <v-list-item
          v-for="(item, index) in items"
          value="item.value"
          color="white"
          :key="index"
          link
          @click="$router.push(item.to)"
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
      drawer: false,
      items: [
        {
          title: 'Home',
          id: 1,
          icon: 'mdi-home',
          to: '/',
        },
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
    };
  },
};
</script>
