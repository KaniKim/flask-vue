<template>
  <div>
    <div v-show="state === false">
      <v-row justify="center">
        <v-col cols="8">
          <v-card>
            <v-card-header-text>{{ comment.body }}</v-card-header-text>
            <v-card-subtitle
              >{{ comment.author.name }} <span>&bull;</span
              >{{ comment.created_at }} <span></span
              ><v-icon @click="state = 'editing'"
                >mdi-grease-pencil</v-icon
              ></v-card-subtitle
            >
          </v-card>
        </v-col>
      </v-row>
    </div>
    <v-dialog v-model="state" width="500">
      <v-card class="overflow-x-hidden overflow-y-hidden">
        <v-row justify="center">
          <v-col cols="12">
            <v-text-field
              v-model="data.body"
              rows="1"
              placeholder="Update comment"
            >
            </v-text-field>
            <v-row>
              <v-col cols="4">
                <v-btn @click="saveEdit">Update</v-btn>
              </v-col>
              <v-col cols="4">
                <v-btn @click="resetEdit">Cancel</v-btn>
              </v-col>
              <v-col cols="4">
                <v-btn @click="deleteComment">Delete</v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      required: true,
      type: Object,
    },
    comment: {
      required: true,
      type: Object,
    },
  },
  data: function () {
    return {
      state: false,
      data: {
        body: this.comment.body,
      },
    };
  },
  computed: {
    editable() {
      return this.user.id === this.comment.id;
    },
  },
  methods: {
    resetEdit() {
      this.state = false;
      this.data.body = this.comment.body;
    },
    saveEdit() {
      this.state = false;

      this.$emit("comment-updated", {
        id: this.comment.id,
        body: this.data.body,
      });
    },
    deleteComment() {
      this.$emit("comment-deleted", {
        id: this.comment.id,
      });
    },
  },
};
</script>
