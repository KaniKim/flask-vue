<template>
  <div>
    <br />
    <br />

    <v-row align="center" justify="center">
      <v-col cols="5">
        <div @keydown.enter.stop>
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
                <v-chip
                  class="ma-1"
                  closable="true"
                  @click:close="remove(item)"
                >
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
          <v-sheet class="mx-auto" max-width="600">
            <v-slide-group show-arrows>
              <v-slide-group-item
                v-for="board_category in board_name"
                :key="board_category"
                v-slot="{ isSelected, toggle }"
              >
                <v-btn
                  class="ma-2"
                  rounded
                  :color="isSelected ? 'primary' : undefined"
                  @click="name = board_category"
                  v-on:click="toggle"
                >
                  {{ board_category }}
                </v-btn>
              </v-slide-group-item>
            </v-slide-group>
          </v-sheet>
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
              @keydown.enter.stop
              min-width="100"
              type="submit"
              class="white--text"
              color="deep-purple accent-4"
              @click="submitForm"
            >
              Yes
            </v-btn>
          </v-col>
        </div>
      </v-col>
    </v-row>
  </div>
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
    board_name: [
      'Science',
      'Art',
      'NFT',
      'BlockChain',
      'AI',
      'AIMMO',
      'Security',
      'Nichijou',
      'ETC',
    ],
    name: '',
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
      if (this.name === '') {
        alert('Please select Board');
        return;
      }
      let tagsArray = [];
      for (var key in this.tags) {
        tagsArray.push(this.tags[key]);
      }
      const columnData = {
        title: this.title,
        content: this.content,
        tags: tagsArray,
        name: this.name,
      };
      await writeColumn(columnData)
        .then(() => {
          alert('Write Complete');
        })
        .catch(err => {
          alert(err);
        });
      this.initForm();
    },
    initForm() {
      this.name = '';
      this.title = '';
      this.content = '';
      this.tags = '';
    },
  },
};
</script>
