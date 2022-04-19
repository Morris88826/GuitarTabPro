<template>
  <div id="step4" style="display: none">
    <div id="step4-main" style="display: none; width: 80%; margin: auto">
      <div
        id="carouselExampleIndicators"
        class="carousel slide mt-3"
        data-bs-ride="carousel"
      >
        <div class="carousel-indicators">
          <button
            v-for="frame in selected_frames"
            :key="frame.id"
            type="button"
            data-bs-target="#carouselExampleIndicators"
            :data-bs-slide-to="frame.id"
            :class="{
              active: frame.id == 0 ? true : false,
            }"
            :aria-current="frame.id === 0 ? true : false"
            aria-label="frame.path"
          ></button>
        </div>
        <div class="carousel-inner">
          <div
            :class="{
              'carousel-item': true,
              active: frame.id == 0 ? true : false,
            }"
            v-for="frame in selected_frames"
            :key="frame.id"
          >
            <img :src="frame.src" class="d-block w-100" alt="..." />
          </div>
        </div>
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleIndicators"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleIndicators"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <div
        class="mt-3"
        style="text-align: center"
      >
        <button class="btn btn-primary" @click="generateTAB">
          Generate TAB
        </button>
      </div>
    </div>
    <div
      id="step4-loading"
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
  data() {
    return {
      selected_frames: [],
    };
  },

  methods: {
    init() {
      document.getElementById("step4").style.display = "block";
      document.getElementById("step4-main").style.display = "none";
      document.getElementById("step4-loading").style.display = "flex";
      this.getIndependentFrames();
    },
    reset() {
      document.getElementById("step4").style.display = "none";
      document.getElementById("step4-main").style.display = "none";
      document.getElementById("step4-loading").style.display = "none";
      this.selected_frames = [];
    },

    generateTAB() {
      this.$parent.goToStep(5);
    },

    getIndependentFrames() {
      this.axios
        .get("/getindependentframes")
        .then((response) => {
          let data = response.data;
          if (data.success) {
            this.selected_frames = data.selected_frames;
            document.getElementById("step4-main").style.display = "block";
            document.getElementById("step4-loading").style.display = "none";
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

<style scoped>
.carousel-control-prev-icon {
  background: black;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z'/%3e%3c/svg%3e");
  border-radius: 5px;
}
.carousel-control-prev-icon::after {
  content: none;
}

.carousel-control-next-icon {
  background: black;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath d='M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
  border-radius: 5px;
}

.carousel-control-next-icon::after {
  content: none;
}

.carousel-indicators [data-bs-target] {
  background-color: black;
}
</style>
