<template>
  <div>
    <div>
      <v-row justify="center">
        <v-col cols="10">
          <br />
          <div class="d-flex">
            <v-text-field
              class="mx-2 rounded-lg"
              v-model="data.body"
              rows="1"
              placeholder="Add a comment"
            >
            </v-text-field>
            <v-chip class="short" large @click="saveComment">
              <v-icon large right>
                mdi-checkbox-multiple-marked-circle-outline
              </v-icon></v-chip
            >
          </div>
        </v-col>
      </v-row>
    </div>
    <v-card class="overflow-y-auto overflow-x-hidden" height="130" border="1">
      <br />
      <comment
        v-for="comment in comments"
        :key="comment.id"
        :user="user"
        :comment="comment"
        @comment-updated="updateComment($event)"
        @comment-deleted="deleteComment($event)"
      >
      </comment>
    </v-card>
  </div>
</template>
<style>
.short {
  width: 60px;
  height: 60px !important;
}
</style>
<script>
import comment from "./CommentItem";
export default {
  components: {
    comment,
  },
  props: {
    user: {
      required: true,
      type: Object,
    },
  },
  data: function () {
    return {
      data: {
        body: "",
      },
      comments: [
        {
          id: 1,
          body: "How's it going?",
          edited: false,
          created_at: new Date().toLocaleString(),
          author: {
            id: 1,
            name: "Nick Basile",
          },
        },
        {
          id: 2,
          body: "Pretty good. Just making a painting.",
          edited: false,
          created_at: new Date().toLocaleString(),
          author: {
            id: 2,
            name: "Bob Ross",
          },
        },
      ],
    };
  },
  methods: {
    updateComment($event) {
      let index = this.comments.findIndex((element) => {
        return element.id === $event.id;
      });

      this.comments[index].body = $event.body;
    },
    deleteComment($event) {
      let index = this.comments.findIndex((element) => {
        return element.id === $event.id;
      });

      this.comments.splice(index, 1);
    },
    saveComment() {
      let newComment = {
        id: this.comments[this.comments.length - 1].id + 1,
        body: this.data.body,
        edited: false,
        created_at: new Date().toLocaleString(),
        author: {
          id: this.user.id,
          name: this.user.name,
        },
      };

      this.comments.push(newComment);

      this.data.body = "";
    },
  },
};
</script>
