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
    <v-list :items="items_drawer"></v-list>
  </v-navigation-drawer>
  <v-main>
    <v-content>
      <h1 align="center">Register Page</h1>
    </v-content>
    <br />
    <br />
    <v-row justify="center" align="center"
      ><v-col md="4" lg="4" cols="4">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-text-field
            v-model="name"
            :counter="10"
            :rules="nameRules"
            label="Name"
            required
          ></v-text-field>

          <v-text-field
            v-model="email"
            :rules="emailRules"
            label="E-mail"
            required
          ></v-text-field>

          <v-text-field
            type="password"
            v-model="password"
            :rules="passwordRules"
            label="Password"
            required
          ></v-text-field>
          <v-row justify="center">
            <v-checkbox
              v-model="checkbox"
              :rules="[(v) => !!v || 'You must agree to continue!']"
              label="Do you agree?"
              required
            ></v-checkbox>

            <v-btn
              :disabled="!valid"
              color="success"
              class="mr-4"
              @click="register"
            >
              Register
            </v-btn>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-main>
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
      (v) => (v && v.length <= 3) || "Name must be less than 10 characters",
    ],
    email: "",
    password: "",
    passwordRules: [
      (v) => !!v || "Password is required",
      (v) =>
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#%&])(?=.{8,})/.text(v) ||
        "Password must be valid",
    ],
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
        title: "Login",
        value: "foo",
      },
      {
        title: "Register",
        value: "bar",
      },
      {
        title: "Category",
        value: "fizz",
      },
    ],
  }),
  watch: {
    group() {
      this.drawer = false;
    },
  },

  methods: {
    register() {
      axios
        .post("http://localhost:8000/user", {
          name: this.name,
          email: this.email,
          password: this.password,
        })
        .then((res) => {
          console.log(res.data);
        });
    },
    reset() {
      this.$refs.form.reset();
    },
  },
};
</script>
