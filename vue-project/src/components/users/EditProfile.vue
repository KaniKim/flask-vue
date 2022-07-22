<template>
  <div>
    <v-card max-width="500">
      <v-card-title class="text-h5 grey lighten-2">
        Change User Info
      </v-card-title>

      <v-card-text>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </v-card-text>
      <v-form @submit.prevent="submitForm">
        <v-container>
          <v-row align="center" justify="center">
            <v-col cols="6" sm="6">
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
            <v-col cols="6" sm="6">
              <v-text-field
                v-model="name"
                counter="25"
                hint="This field is for name"
                label="Name"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row align="center" justify="center">
            <v-col cols="6" sm="6">
              <v-text-field
                v-model="password"
                :rules="passwordRules"
                type="password"
                counter="25"
                hint="This field is for id"
                label="Password"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn type="submit" variant="outlined" color="primary"
            >I accept
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </div>
</template>
<script>
import { editUser } from '@/api';

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      passwordRules: [
        password => !!password || 'Please enter a password',
        password => !!password || 'Please type password.',
        password =>
          (password &&
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/.test(
              password,
            )) ||
          'Minimum 6 characters, One capital latter, Special character, Number',
      ],
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
        name: this.name,
        email: this.email,
        password: this.password,
      };
      await editUser(userData)
        .then(() => {})
        .catch(err => {
          alert(err);
        });
      this.initForm();
    },
    initForm() {
      this.name = '';
      this.password = '';
      this.email = '';
    },
  },
};
</script>
