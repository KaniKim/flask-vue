<template>
  <v-main>
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
    <v-form @submit.prevent="submitForm">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="email"
              :rules="emailRules"
              counter="25"
              hint="This field is for email"
              label="Email"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="password"
              type="password"
              counter="25"
              hint="This field is for password"
              label="Password"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="6" sm="6">
            <v-btn type="submit" variant="outlined" color="primary" block>
              Check Login
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-main>
</template>

<script>
import { loginUser } from '@/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      emailRules: [
        email =>
          !email ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(email) ||
          'E-mail must be valid',
      ],
    };
  },
  methods: {
    async submitForm() {
      const userData = {
        email: this.email,
        password: this.password,
      };
      await loginUser(userData)
        .then(res => {
          console.log(res.data);
          localStorage.setItem('access_token', res.data.access_token);
          localStorage.setItem('refresh_token', res.data.refresh_token);
        })
        .catch(err => {
          alert(err);
        });
      await this.$router.push({ path: '/' });
      this.initForm();
    },
    initForm() {
      this.password = '';
      this.email = '';
    },
  },
};
</script>
