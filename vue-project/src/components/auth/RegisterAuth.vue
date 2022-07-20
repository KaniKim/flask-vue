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
              :rules="rules"
              counter="25"
              hint="This field is for email"
              label="Email"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="centeR" justify="center">
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="name"
              :rules="rules"
              counter="25"
              hint="This field is for name"
              label="Name"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="password"
              :rules="rules"
              counter="25"
              hint="This field is for id"
              label="Password"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row align="center" justify="center">
          <v-col cols="6" sm="6">
            <v-btn type="submit" variant="outlined" color="primary" block>
              Check Assign
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-main>
</template>

<script>
import { registerUser } from '@/api';

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      rules: [v => v.length <= 25 || 'Max 25 characters'],
    };
  },
  methods: {
    async submitForm() {
      const userData = {
        name: this.name,
        email: this.email,
        password: this.password,
      };
      await registerUser(userData);
    },
    initForm() {
      this.name = '';
      this.password = '';
      this.email = '';
    },
  },
};
</script>
