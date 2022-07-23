<template>
  <div>
    <v-card width="400">
      <v-card-item>
        <v-card-title>{{ title }}</v-card-title>

        <v-card-subtitle>{{ author }}</v-card-subtitle>
      </v-card-item>

      <v-card-text>
        {{ content }}
      </v-card-text>
    </v-card>
  </div>
</template>
<script>
import { specificColumn } from '@/api/column';

export default {
  data: () => ({
    title: '',
    content: '',
    tags: [],
    author: '',
  }),
  created() {
    const specific = {
      name: this.$route.params.name,
      column_id: this.$route.params.column_id,
    };
    specificColumn(specific)
      .then(res => {
        this.title = res.data.title;
        this.content = res.data.content;
        this.author = res.data.author;
        this.tags = res.data.tags;
      })
      .catch(err => {
        alert(err);
      });
  },
};
</script>
