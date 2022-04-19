<template>
  <div class="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
export default {
  name: "App",
  components: { Navbar },
};
</script>
#app { font-family: Roboto, Helvetica, Arial, sans-serif; }
<style scoped></style>
