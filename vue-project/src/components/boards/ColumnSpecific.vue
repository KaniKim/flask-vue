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
          <v-col cols="12">
            <h1>Comment</h1>
            <v-text-field
              v-model="comment_content"
              filled
              color="deep-purple"
              label="comment"
              @keydown.enter="postComment"
            ></v-text-field>
            <v-list v-for="comment in comments" :key="comment.key">
              <v-list-item-title
                >{{ comment.content }} - {{ comment.author }}
                <v-btn
                  class="ma-2"
                  variant="text"
                  color="blue-lighten-2"
                  @click="addComment"
                  ><v-icon end icon="mdi-checkbox-marked-circle">
                  </v-icon> </v-btn
              ></v-list-item-title>
              <div v-for="next in comment.next_comment" :key="next.key">
                <v-list-item-subtitle>{{ next.content }}</v-list-item-subtitle>
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
import { getComment, postComment } from '@/api/comment';

export default {
  data: () => ({
    id: '',
    title: '',
    comment_content: '',
    tags: [],
    author: '',
    name: '',
    content: '',
    like: 0,
    column_id: '',
    comment: '',
    comments: null,
  }),
  methods: {
    addComment() {},
    postComment() {
      const data = {
        content: this.comment_content,
        column_id: this.$route.params.id,
      };
      postComment(data)
        // eslint-disable-next-line no-unused-vars
        .then(res => {
          getComment(this.$route.params.id)
            .then(res => {
              this.comments = res.data.comments;
            })
            .catch(err => {
              alert(err);
            });
        })
        .catch(err => {
          alert(err);
        });
    },
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
    getComment(this.$route.params.id)
      .then(res => {
        this.comments = res.data.comments;
      })
      .catch(err => {
        alert(err);
      });
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
