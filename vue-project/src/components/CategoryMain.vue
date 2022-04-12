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

    <v-toolbar-title>Hello From Kani</v-toolbar-title>
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
    <v-col cols="6">
      <div id="app">
        <v-table height="300px">
          <thead>
            <tr>
              <th class="text-left">Number</th>
              <th class="text-left">Category</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, i) in slides"
              :key="i"
              style="cursor: pointer"
              @click="cateProfile(item)"
            >
              <td>{{ i + 1 }}</td>
              <td>{{ item }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>
    </v-col>
  </v-row>
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
import Cookies from "js-cookie";

export default {
  data: () => ({
    drawer: false,
    valid: true,
    slides: null,
    select: null,
    checkbox: false,
    links: ["Home", "About Us", "Category", "Contact Us"],
    items_drawer: [
      {
        title: "Home",
        route: "/",
        value: true,
      },

      {
        title: "Write",
        route: "/write",
        value: true,
      },
      {
        title: "Category",
        route: "/category",
        value: true,
      },
    ],
  }),

  created() {
    axios.defaults.headers.common["Authorization"] =
      Cookies.get("access_token");
    axios
      .get("http://localhost:8000/category")
      .then((res) => {
        console.log(res.data);
        this.slides = res.data;
      })
      .catch((err) => {
        alert(err);
      });
  },
  methods: {
    cateProfile(cate) {
      window.location.href = "http://localhost:8080/category/post/" + cate;
    },
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
};
</script>
