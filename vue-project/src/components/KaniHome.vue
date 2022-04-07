<template>
  <v-app-bar
    color="gray"
    prominent
    src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
  >
    <v-app-bar-nav-icon
      variant="text"
      @click.stop="drawer = !drawer"
    ></v-app-bar-nav-icon>

    <v-toolbar-title>Kani</v-toolbar-title>
    <v-spacer></v-spacer>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" temporary>
    <v-list>
      <v-list-item
        v-for="item in items_drawer"
        :key="item.title"
        :to="item.route"
        link
      >
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
  <br />
  <br />
  <br />
  <v-row justify="center">
    <v-img
      max-height="300"
      max-width="300"
      src="https://kr.vuejs.org/images/logo.png"
    >
    </v-img>
  </v-row>
  <br />
  <br />
  <v-content>
    <h1 align="center">Kani's VuePage</h1>
  </v-content>

  <v-footer padless fixed width="100%" bottom class="bg-grey-lighten-1">
    <v-container fluid>
      <v-row justify="center">
        <v-btn
          v-for="link in links"
          :key="link"
          color="white"
          variant="text"
          class="mx-2"
          rounded="xl"
        >
          {{ link }}
        </v-btn>
        <v-col class="text-center text-white mt-4" cols="12">
          {{ new Date().getFullYear() }} — <strong>HomePage</strong>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    drawer: false,
    valid: true,
    name: "",
    nameRules: [
      (v) => !!v || "Name is required",
      (v) => (v && v.length <= 10) || "Name must be less than 10 characters",
    ],
    email: "",
    password: "",
    emailRules: [
      (v) => !!v || "E-mail is required",
      (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
    ],
    select: null,
    items: ["Item 1", "Item 2", "Item 3", "Item 4"],
    checkbox: false,
    links: ["Home", "About Us", "Category", "Contact Us"],
    items_drawer: [
      {
        title: "Home",
        route: "/",
      },
      {
        title: "Login",
        route: "/login",
      },
      {
        title: "Register",
        route: "/register",
      },
      {
        title: "Category",
        route: "/category",
      },
    ],
  }),
  watch: {
    group() {
      this.drawer = false;
    },
  },
  created() {
    axios
      .get("http://localhost:8000/user/login")
      .then((res) => {
        const user = res.data.user;

        if (user) {
          this.$store.commit("setUser", user);
        } else {
          this.$router.push({ name: "Login" });
        }
      })
      .catch((err) => {
        console.error(err);
      });
  },
  computed: {
    user() {
      return this.$store.getters.user;
    },
  },
};
</script>
