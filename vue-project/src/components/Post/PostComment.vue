<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <br />
        <v-content>
          <h1>Write Your Content</h1>
        </v-content>
        <br />
        <v-content
          filled
          auto-grow
          label="Title"
          rows="1"
          v-model="title"
          row-height="20"
          ><h1>Hello</h1></v-content
        >
        <v-content
          solo
          auto-grow
          name="input-7-4"
          v-model="content"
          label="Content"
        ></v-content>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import AxiosInst from "@/plugins/axios";
export default {
  data: () => ({
    title: null,
    content: null,
    tags: null,
  }),

  created() {
    AxiosInst.get("http://localhost:8000/post", {
      params: {
        category_name: this.$route.params.cate,
      },
    })
      .then((res) => {
        this.items = res.data;
      })
      .catch((err) => {
        alert(err);
      });
  },
};
</script>
