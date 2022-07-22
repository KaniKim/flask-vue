<template>
  <div class="text-center">
    <br />
    <v-row justify="center" align="center">
      <v-col cols="8">
        <v-table theme="white">
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Calories</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in desserts" :key="item.name">
              <td>{{ item.name }}</td>
              <td>{{ item.calories }}</td>
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
export default {
  data() {
    return {
      desserts: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
        },
        {
          name: 'Eclair',
          calories: 262,
        },
        {
          name: 'Cupcake',
          calories: 305,
        },
        {
          name: 'Gingerbread',
          calories: 356,
        },
        {
          name: 'Jelly bean',
          calories: 375,
        },
        {
          name: 'Lollipop',
          calories: 392,
        },
        {
          name: 'Honeycomb',
          calories: 408,
        },
        {
          name: 'Donut',
          calories: 452,
        },
        {
          name: 'KitKat',
          calories: 518,
        },
      ],
      page: 1,
    };
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
