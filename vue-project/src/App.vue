<template>
  <v-app>
    <v-main>
      <DrawNav></DrawNav>
      <router-view></router-view>
      <FooFighter></FooFighter>
    </v-main>
  </v-app>
</template>

<script>
import DrawNav from "@/components/layout/DrawNav";
import FooFighter from "@/components/layout/FooFighter";
export default {
  components: { FooFighter, DrawNav },
};
</script>
