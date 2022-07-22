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
        <v-btn color="orange" @click="showDialogEdit">Edit</v-btn>
        <v-btn color="orange" @click="showDialogDelete"> Delete </v-btn>
        <v-dialog v-model="dialogEdit">
          <EditProfile @hide="hideDialog"></EditProfile>
        </v-dialog>
        <v-dialog v-model="dialogDelete">
          <DeleteProfile @hide="hideDialog"></DeleteProfile>
        </v-dialog>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { checkUser } from '@/api';
import EditProfile from '@/components/users/EditProfile';
import DeleteProfile from '@/components/users/DeleteProfile';

export default {
  components: { EditProfile, DeleteProfile },
  data: () => ({
    user_name: '',
    user_email: '',
    dialogEdit: false,
    dialogDelete: false,
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
  methods: {
    hideDialog() {
      this.dialogEdit = false;
      this.dialogDelete = false;
    },
    showDialogEdit() {
      this.dialogEdit = true;
    },
    showDialogDelete() {
      this.dialogDelete = true;
    },
  },
};
</script>
