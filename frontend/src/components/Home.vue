<template>
  <div class="container mt-4">
    <div id="home-step1" class="row mt-3">
      <div class="col text-style">Step1: Choose your video</div>
      <Step1 ref="step1" />
    </div>
    <div id="home-step2" class="row mt-3">
      <div class="col text-style">Step2: Trim the video</div>
      <Step2 ref="step2" />
    </div>
    <div id="home-step3" class="row mt-3">
      <div class="col text-style">
        Step3: Select the Region of Interest(ROI)
      </div>
      <Step3 ref="step3" />
    </div>
    <div id="home-step4" class="row mt-3">
      <div class="col text-style">Step4: Select Independent Frames</div>
      <Step4 ref="step4" />
    </div>
    <div id="home-step5" class="row mt-3">
      <div class="col text-style">Step5: Generate TAB</div>
      <Step5 ref="step5" />
    </div>
  </div>
</template>

<script>
import Step1 from "./Step1.vue";
import Step2 from "./Step2.vue";
import Step3 from "./Step3.vue";
import Step4 from "./Step4.vue";
import Step5 from "./Step5.vue";

export default {
  data() {
    return {
      show_video: false,
      searchURL: null,
      available_videos: [],
      selected_video: null,
      timePeriod: [0, 100],
      previousTimePeriod: [0, 100],
      video_duration: 100,
      thumbnail: null,
    };
  },
  components: { Step1, Step2, Step3, Step4, Step5 },
  methods: {
    changeToSection(id) {
      var element = document.createElement("a");
      element.setAttribute("href", "#" + id);
      element.style.display = "none";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    goToStep(step) {
      if (step === 2) {
        this.changeToSection("home-step2");
        this.$refs.step2.init(this.$refs.step1.selected_video);
        this.$refs.step3.reset();
        this.$refs.step4.reset();
        this.$refs.step5.reset();
      } else if (step === 3) {
        this.changeToSection("home-step3");
        this.$refs.step3.init();
        this.$refs.step4.reset();
        this.$refs.step5.reset();
      } else if (step === 4) {
        this.changeToSection("home-step4");
        this.$refs.step4.init();
        this.$refs.step5.reset();
      } else if (step === 5) {
        this.changeToSection("home-step5");
        this.$refs.step5.init();
      }
    },
    searchVideo() {
      this.initStep2();
      this.axios
        .post("/searchytvideo", { url: this.searchURL })
        .then((response) => {
          if (response.data.success) {
            var data = response.data.data;
            this.available_videos = [];
            for (var i = 0; i < data.length; i++) {
              this.available_videos.push(data[i]);
            }
          } else {
            this.searchURL = null;
            this.available_videos = [];
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    async viewYouTubeVideo(itag) {
      this.axios
        .post("/downloadytvideo", { url: this.searchURL, itag: itag })
        .then((response) => {
          let data = response.data;
          if (data.success === true) {
            document.getElementById("step-2").style.display = "block";
            let video = document.getElementById("video-preview");
            document.getElementById("trim-result").style.display = "none";
            video.src = data.video;
            this.getDuration(video).then((duration) => {
              document.getElementById("video-preview").style.display = "block";
              document.getElementById("trim-bar").style.display = "block";
              this.video_duration = duration;
              this.timePeriod = [0, duration];
              this.previousTimePeriod = [0, duration];
              this.show_video = true;
            });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    downloadVideo_base64(base64_video) {
      var a = document.createElement("a"); //Create <a>
      a.href = base64_video;
      a.download = "output.mp4"; //File name Here
      a.click(); //Downloaded file
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
