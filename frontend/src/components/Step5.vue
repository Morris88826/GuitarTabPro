<template>
  <div id="step5" style="display: none">
    <div id="step5-main">
      <img id="tab" class="mt-4" src="" alt="Guitar TAB" style="width: 100%" />
    </div>
    <div
      id="step5-loading"
      class="mt-3"
      style="
        display: none;
        justify-content: center;
        align-items: center;
        height: 80vh;
      "
    >
      <a-spin />
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    init() {
      document.getElementById("step5").style.display = "block";
      document.getElementById("step5-loading").style.display = "flex";
      document.getElementById("step5-main").style.display = "none";
      this.generateTAB();
    },
    reset() {
      document.getElementById("step5").style.display = "none";
      document.getElementById("step5-loading").style.display = "none";
      document.getElementById("step5-main").style.display = "none";
    },
    generateTAB() {
      this.axios
        .get("/generatetab")
        .then((response) => {
          let data = response.data;
          if (data.success) {
            let tab = document.getElementById("tab");
            tab.src = data.tab;
            document.getElementById("step5-loading").style.display = "none";
            document.getElementById("step5-main").style.display = "block";

            return;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style></style>
