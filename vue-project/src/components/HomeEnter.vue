<template>
  <div>
    <br />
    <br />
    <br />
    <br />
    <v-row align="center" justify="center">
      <v-img
        :src="require(`@/assets/aiko.png`)"
        alt="aiko"
        max-height="400px"
        max-width="400px"
        style="border-radius: 28px"
      />
    </v-row>
    <br />
    <br />
    <v-row align="center" justify="center">
      <h1>Welcome {{ this.user_name }}</h1>
    </v-row>
  </div>
</template>
<script>
import { checkUser } from '@/api';

export default {
  data: () => ({
    user_name: '',
  }),
  created() {
    checkUser()
      .then(res => {
        this.user_name = res.data['name'];
      })
      .catch(err => {
        alert(err);
      });
  },
};
</script>
