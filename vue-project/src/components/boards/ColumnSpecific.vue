<template>
  <div>
    <br />
    <v-row justify="center" align="center">
      <v-col cols="6">
        <v-card min-width="400">
          <v-card-item>
            <v-card-title>{{ title }}</v-card-title>

            <v-card-subtitle>{{ author }}</v-card-subtitle>
          </v-card-item>

          <v-card-text>
            {{ content }}
          </v-card-text>
          <v-btn
            class="ma-2"
            variant="text"
            color="blue-lighten-2"
            @click="addLike"
            >{{ like }} <v-icon end icon="mdi-checkbox-marked-circle"> </v-icon>
          </v-btn>
          <v-divider inset></v-divider>
          <v-col cols="4">
            <h1>Comment</h1>
            <v-list v-for="comment in comments" :key="comment.key">
              <v-list-item-title>{{ comment.content }}</v-list-item-title>
              <div v-for="recomment in comment.recomments" :key="recomment.key">
                <v-list-item-subtitle>{{
                  recomment.recontent
                }}</v-list-item-subtitle>
              </div>
            </v-list>
          </v-col>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { clickLike, specificColumn } from '@/api/column';

export default {
  data: () => ({
    id: '',
    title: '',
    content: '',
    tags: [],
    author: '',
    name: '',
    like: 0,
    column_id: '',
    comments: [
      {
        content: 'hello',
        recomments: [
          {
            recontent: 'hello too',
          },
          {
            recontent: 'hello too',
          },
        ],
      },
    ],
  }),
  methods: {
    addLike() {
      clickLike(this.$route.params.id)
        .then(() => {
          this.like++;
        })
        .catch(err => {
          alert(err);
        });
    },
  },
  created() {
    const specific = {
      name: this.$route.params.name,
      column_id: this.$route.params.id,
    };
    specificColumn(specific)
      .then(res => {
        this.id = res.data.id;
        this.title = res.data.title;
        this.content = res.data.content;
        this.author = res.data.author;
        this.tags = res.data.tags;
        this.like = res.data.like;
      })
      .catch(err => {
        alert(err);
      });
  },
};
</script>
