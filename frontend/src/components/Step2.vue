<template>
  <div id="step2" style="display: none">
    <div class="row">
      <div class="col-6 mt-3">
        <div id="step2-original" style="display: none">
          <div class="row">
            <div class="col text-style" style="font-size: 18px">
              Original Video:
            </div>
          </div>
          <div style="text-align: center">
            <video
              class="mt-3"
              style="width: 80%; margin: auto"
              id="step2-video-preview"
              controls
            />
          </div>
          <br />
          <div id="trim-bar" style="width: 80%; margin: auto">
            <a-slider
              class="mt-2"
              v-model:value="timePeriod"
              range
              :max="video_duration"
              :step="0.01"
              @change="changeCurrentVideoTime"
            />
            <div style="text-align: center">
              <button class="btn btn-primary" @click="trimVideo">Trim</button>
            </div>
          </div>
        </div>
        <div
          id="step2-original-loading"
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
      <div class="col-6 mt-3">
        <div id="step2-trimmed" style="display: none">
          <div class="row">
            <div class="col text-style" style="font-size: 18px">
              Trimmed Video:
            </div>
          </div>
          <div style="text-align: center">
            <video
              class="mt-3"
              style="width: 80%; margin: auto"
              id="step2-trimmed-video-preview"
              controls
            />
          </div>
        </div>
        <div
          id="step2-trimmed-loading"
          style="
            display: none;
            justify-content: center;
            align-items: center;
            height: 100%;
          "
        >
          <a-spin />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      timePeriod: [0, 100],
      video_duration: 100,
    };
  },
  methods: {
    async init(file) {
      document.getElementById("step2").style.display = "block";
      document.getElementById("step2-original").style.display = "none";
      document.getElementById("step2-original-loading").style.display = "flex";
      document.getElementById("step2-trimmed").style.display = "none";
      document.getElementById("step2-trimmed-loading").style.display = "none";

      let video = document.getElementById("step2-video-preview");
      video.src = await this.fileLoad(file[0]);
      var duration = await this.getDuration(video);
      this.video_duration = duration;
      this.timePeriod = [0, duration];
      this.previousTimePeriod = [0, duration];
      document.getElementById("step2-original").style.display = "block";
      document.getElementById("step2-original-loading").style.display = "none";
    },

    reset() {
      document.getElementById("step2").style.display = "none";
      document.getElementById("step2-original").style.display = "none";
      document.getElementById("step2-original-loading").style.display = "none";
      document.getElementById("step2-trimmed").style.display = "none";
      document.getElementById("step2-trimmed-loading").style.display = "none";

      this.timePeriod = [0, 100];
      this.video_duration = 100;
    },

    fileLoad(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
      });
    },

    getDuration(video) {
      return new Promise((resolve) => {
        video.onloadedmetadata = () => {
          resolve(video.duration);
        };
      });
    },

    changeCurrentVideoTime() {
      let video = document.getElementById("step2-video-preview");
      if (this.previousTimePeriod[0] !== this.timePeriod[0]) {
        video.currentTime = this.timePeriod[0];
      } else {
        video.currentTime = this.timePeriod[1];
      }
      this.previousTimePeriod = this.timePeriod;
    },
    trimVideo() {
      document.getElementById("step2-trimmed").style.display = "none";
      document.getElementById("step2-trimmed-loading").style.display = "flex";
      let video = document.getElementById("step2-video-preview");
      this.axios
        .post("/trimvideo", {
          video: video.src,
          start_t: this.timePeriod[0],
          end_t: this.timePeriod[1],
        })
        .then((response) => {
          let data = response.data;
          if (data.success) {
            let t_video = document.getElementById(
              "step2-trimmed-video-preview"
            );
            t_video.src = data.video;
            document.getElementById("step2-trimmed").style.display = "block";
            document.getElementById("step2-trimmed-loading").style.display =
              "none";

            this.$parent.goToStep(3);
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
.text-style {
  font-size: 20px;
  font-family: "Lucida Console", Courier, monospace !important;
}
</style>
