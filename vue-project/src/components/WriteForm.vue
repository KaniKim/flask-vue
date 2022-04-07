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
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <br />
        <v-content>
          <h1>Write Your Content</h1>
        </v-content>
        <br />
        <v-textarea
          filled
          auto-grow
          label="Title"
          rows="1"
          v-model="title"
          row-height="20"
        ></v-textarea>
        <v-textarea
          solo
          auto-grow
          name="input-7-4"
          v-model="content"
          label="Content"
        ></v-textarea>
        <v-text-field
          label="tags"
          v-model="currentInput"
          @keypress.enter="saveChip"
        >
        </v-text-field>
        <v-chip-group>
          <v-chip v-for="(chip, i) of chips" :key="chip.label"
            >{{ chip }}
            <v-icon @click="deleteChip(i)" small right>
              mdi-close-circle-outline
            </v-icon>
          </v-chip>
        </v-chip-group>
        <br />
        <br />
        <v-btn depressed elevation="2" @click="writePost">Submit</v-btn>
        <v-col cols="4">
          <v-select
            v-model="category_name"
            :items="category"
            filled
            label="Choose Category"
          ></v-select>
        </v-col>
      </v-col>
    </v-row>
  </v-container>
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
  data: function () {
    return {
      drawer: false,
      valid: true,
      category_name: null,
      category: [
        { name: "life", value: "life" },
        { name: "work", value: "work" },
        { name: "balance", value: "balance" },
      ],
      chips: [],
      currentInput: "",
      title: "",
      content: "",
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
    };
  },
  methods: {
    saveChip() {
      const { chips, currentInput, set } = this;
      ((set && chips.indexOf(currentInput) === -1) || !set) &&
        this.currentInput !== "" &&
        chips.push(currentInput);
      this.currentInput = "";
    },
    deleteChip(index) {
      this.chips.splice(index, 1);
    },
    writePost() {
      axios
        .post("http://localhost:8000/category", {
          title: this.title,
          content: this.content,
          tags: this.chips,
          category: this.category_name,
          username: this.$store.getters.user,
          password: this.$store.getters.password,
        })
        .then((res) => {
          console.log(res);
          alert(res.data.msg);
        })
        .catch((err) => {
          console.error(err);
          alert("Email or Password is Wrong");
        });
    },
  },
};
</script>
