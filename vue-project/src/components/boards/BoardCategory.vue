<template>
  <div class="text-center">
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
        <v-table theme="white" :key="componentKey">
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Calories</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in board_columns" :key="item.name">
              <td>{{ item.title }}</td>
              <td>{{ item.like }}</td>
            </tr>
          </tbody>
        </v-table>
        <br />
        <v-pagination
          v-model="page"
          :length="6"
          class="pagination"
        ></v-pagination>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { allColumn } from '@/api/column';

export default {
  data() {
    return {
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
            this.board_columns = [];
            // eslint-disable-next-line no-unused-vars
            res.data.columns.forEach((data, index, array) => {
              this.board_columns.push(data);
            });
          })
          .catch(err => {
            alert(err);
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
