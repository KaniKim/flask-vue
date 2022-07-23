<template>
  <div align="center">
    <v-alert
      v-if="alert"
      v-model="alert"
      border="start"
      variant="tonal"
      closable="true"
      close-label="Close Alert"
      color="deep-purple accent-4"
      title="Closable Alert"
      :key="componentKey"
    >
      At {{ name }}, there is not existed columns. Lets write some columns.
    </v-alert>
    <br />
    <v-row justify="center" align="center">
      <v-col cols="8">
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
                @click="getColumns(board_category)"
                v-on:click="toggle"
              >
                {{ board_category }}
              </v-btn>
            </v-slide-group-item>
          </v-slide-group>
        </v-sheet>
        <v-table
          align="center"
          theme="white"
          :key="componentKey"
          class="text-xs-center"
        >
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Like</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in board_columns" :key="item.name">
              <router-link
                style="text-decoration: none; color: inherit"
                :to="{
                  name: 'Column',
                  params: { column_id: item.column._id.$oid, name: item.name },
                }"
              >
                <td>{{ item.column.title }}</td>
              </router-link>
              <td>{{ item.column.like }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { allColumn, specificBoard } from '@/api/column';

export default {
  data() {
    return {
      alert: false,
      board_columns: [],
      page: 1,
      componentKey: 0,
      board_name: [
        'All',
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
    };
  },
  methods: {
    forceRerender() {
      this.componentKey += 1;
    },
    getColumns(board_name) {
      if (board_name === 'All') {
        allColumn()
          .then(res => {
            if (this.alert === true) {
              this.alert = false;
            }
            this.board_columns = [];
            // eslint-disable-next-line no-unused-vars
            res.data.columns.forEach((data, index, array) => {
              this.board_columns.push(data);
            });
          })
          .catch(err => {
            alert(err);
          });
      } else {
        specificBoard(board_name)
          .then(res => {
            this.board_columns = [];
            this.alert = false;
            // eslint-disable-next-line no-unused-vars
            res.data.columns.forEach((data, index, array) => {
              this.board_columns.push(data);
            });
            this.name = board_name;
          })
          // eslint-disable-next-line no-unused-vars
          .catch(err => {
            this.board_columns = [];
            this.alert = true;
            this.name = board_name;
          });
        this.forceRerender();
      }
    },
  },
};
</script>
<style>
.pagination {
  bottom: 0;
  position: absolute;
  display: flex;
  left: 0;
  right: 0;
  justify-content: center;
}
</style>
