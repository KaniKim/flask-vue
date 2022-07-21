<template>
  <div>
    <br />
    <br />
    <br />
    <v-card class="mx-auto" max-width="800">
      <v-img
        class="align-end text-black"
        height="400"
        :src="require(`@/assets/aiko.png`)"
        cover
      >
        <v-card-title>{{ this.user_name }}'s Information</v-card-title>
      </v-img>

      <v-card-subtitle class="pt-4"> {{ this.user_name }} </v-card-subtitle>

      <v-card-text>
        <div>Email: {{ this.user_email }}</div>
        <div>Welcome to your information.</div>
      </v-card-text>

      <v-card-actions>
        <v-btn color="orange"> Edit </v-btn>
        <v-btn color="orange"> Delete </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { checkUser } from '@/api';

export default {
  data: () => ({
    user_name: '',
    user_email: '',
  }),
  created() {
    checkUser()
      .then(res => {
        this.user_email = res.data['email'];
        this.user_name = res.data['name'];
      })
      .catch(err => {
        alert(err);
      });
  },
};
</script>
