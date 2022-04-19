<template>
  <div id="step1">
    <div class="input-group mt-3">
      <MDBFile v-model="selected_video" />
      <button class="btn btn-primary" @click="viewVideo">Search</button>
    </div>
  </div>
</template>

<script>
import { MDBFile } from "mdb-vue-ui-kit";
export default {
  data() {
    return {
      selected_video: null,
    };
  },
  components: { MDBFile },
  methods: {
    async viewVideo() {
      if (this.selected_video !== null) {
        this.$parent.goToStep(2);
      }
    },
  },
};
</script>

<style scoped>
.text-style {
  font-size: 20px;
  font-family: "Lucida Console", Courier, monospace !important;
}
</style>
