<template>
  <v-row align="center" justify="center">
    <v-col cols="5">
      <v-form
        @keydown.enter.prevent="submitForm"
        v-model="form"
        class="pa-4 pt-6"
      >
        <v-text-field
          v-model="title"
          filled
          color="deep-purple"
          label="Title"
        ></v-text-field>
        <v-text-field
          bg-color="white"
          v-model="textBox"
          v-on:keyup.space="addChips"
        >
          <template v-slot:prepend-inner>
            <div v-for="(chipText, index) in tags" :key="index">
              <v-chip class="ma-1" closable="true" @click:close="remove(item)">
                {{ chipText }}
              </v-chip>
            </div>
          </template>
        </v-text-field>
        <v-textarea
          v-model="content"
          auto-grow
          filled
          color="deep-purple"
          label="Content"
          rows="6"
        ></v-textarea>
        <v-checkbox
          v-model="agreement"
          :rules="[rules.required]"
          color="deep-purple"
        >
          <template v-slot:label>
            I agree to the&nbsp;Kaniko's publish*
          </template>
        </v-checkbox>
        <v-col justify="center" align="center">
          <v-btn
            min-width="100"
            class="white--text"
            color="deep-purple accent-4"
            type="submit"
            @click="agreement = true"
          >
            Yes
          </v-btn>
        </v-col>
      </v-form>
    </v-col>
  </v-row>
</template>
<script>
import { writeColumn } from '@/api/column';

export default {
  data: () => ({
    tags: [],
    textBox: '',
    agreement: false,
    content: '',
    title: '',
    form: false,
    items: [],
    rules: {
      required: v => !!v || 'This field is required',
    },
  }),
  methods: {
    addChips() {
      if (this.textBox.length) {
        this.tags.push(this.textBox);
        this.textBox = '';
      }
    },
    remove(item) {
      this.tags.splice(this.tags.indexOf(item), 1);
    },
    async submitForm() {
      let tagsArray = [];
      for (var key in this.tags) {
        tagsArray.push(this.tags[key]);
      }
      const columnData = {
        title: this.title,
        content: this.content,
        tags: tagsArray,
      };
      await writeColumn(columnData)
        .then(() => {})
        .catch(err => {
          alert(err);
        });
      this.initForm();
    },
    initForm() {
      this.title = '';
      this.content = '';
      this.tags = '';
    },
  },
};
</script>
