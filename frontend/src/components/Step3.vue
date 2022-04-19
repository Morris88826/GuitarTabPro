<template>
  <div id="step3">
    <div id="step3-main" class="mt-3" style="display: none; text-align: center">
      <canvas id="canvas" :width="c_width" :height="c_height" />
      <div class="mt-3" v-if="selected_info !== null" style="text-align: center">
        <button class="btn btn-primary" @click="selectROI">
          Get Independent Frames
        </button>
      </div>
    </div>
    <div
      id="step3-loading"
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
      canvas: null,
      ctx: null,
      canvasOffset: null,
      offsetX: null,
      offsetY: null,
      isDown: false,
      startX: null,
      startY: null,
      image: null,
      c_width: 500,
      c_height: 300,
      selected_info: null,
    };
  },

  methods: {
    init() {
      document.getElementById("step3").style.display = "block";
      document.getElementById("step3-main").style.display = "none";
      document.getElementById("step3-loading").style.display = "flex";
      this.getThumbnail();
    },

    reset() {
      document.getElementById("step3").style.display = "none";
      document.getElementById("step3-main").style.display = "none";
      document.getElementById("step3-loading").style.display = "none";
      this.selected_info = null;
    },

    getThumbnail() {
      this.axios
        .get("/getthumbnail")
        .then((response) => {
          let data = response.data;
          if (data.success) {
            if (data.image !== undefined) {
              let image_header = "data:image/png;base64,";
              let image = image_header + data.image;
              this.getImageDimensions(image).then((dim) => {
                this.canvas.width = dim.w;
                this.canvas.height = dim.h;
                this.canvas.style.backgroundImage = "url('" + image + "')";
                document.getElementById("step3-main").style.display = "block";
                document.getElementById("step3-loading").style.display = "none";
              });
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },

    selectROI() {
      if (this.selected_info !== null) {
        this.axios
          .post("/saveroi", { roi: this.selected_info })
          .then((response) => {
            let data = response.data;
            if (data.success === true) {
              this.$parent.goToStep(4);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    handleMouseDown(e) {
      e.preventDefault();
      e.stopPropagation();

      this.ctx = this.canvas.getContext("2d");
      this.ctx.strokeStyle = "blue";
      this.ctx.lineWidth = 2;
      var rect = this.canvas.getBoundingClientRect();
      this.offsetX = rect.left;
      this.offsetY = rect.top;

      // save the starting x/y of the rectangle
      this.startX = parseInt(e.clientX - this.offsetX);
      this.startY = parseInt(e.clientY - this.offsetY);

      // set a flag indicating the drag has begun
      this.isDown = true;
    },

    handleMouseUp(e) {
      e.preventDefault();
      e.stopPropagation();

      // the drag is over, clear the dragging flag
      this.isDown = false;

      this.selected_info = {
        start_x: Math.min(this.startX, parseInt(e.clientX - this.offsetX)),
        start_y: Math.min(this.startY, parseInt(e.clientY - this.offsetY)),
        end_x: Math.max(this.startX, parseInt(e.clientX - this.offsetX)),
        end_y: Math.max(this.startY, parseInt(e.clientY - this.offsetY)),
      };
    },

    handleMouseOut(e) {
      e.preventDefault();
      e.stopPropagation();

      // the drag is over, clear the dragging flag
      this.isDown = false;
    },

    handleMouseMove(e) {
      e.preventDefault();
      e.stopPropagation();

      // if we're not dragging, just return
      if (!this.isDown) {
        return;
      }

      // get the current mouse position
      this.mouseX = parseInt(e.clientX - this.offsetX);
      this.mouseY = parseInt(e.clientY - this.offsetY);

      // Put your mousemove stuff here

      // clear the canvas
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // calculate the rectangle width/height based
      // on starting vs current mouse position
      var width = this.mouseX - this.startX;
      var height = this.mouseY - this.startY;

      //   console.log(this.startX, this.startY, this.mouseX, this.mouseY);

      // draw a new rect from the start position
      // to the current mouse position
      this.ctx.strokeRect(this.startX, this.startY, width, height);
    },

    getImageDimensions(file) {
      return new Promise(function (resolved) {
        var i = new Image();
        i.onload = function () {
          resolved({ w: i.width, h: i.height });
        };
        i.src = file;
      });
    },
  },

  mounted() {
    this.canvas = document.getElementById("canvas");
    this.canvas.addEventListener("mousedown", (e) => {
      this.handleMouseDown(e);
    });
    this.canvas.addEventListener("mousemove", (e) => {
      this.handleMouseMove(e);
    });
    this.canvas.addEventListener("mouseup", (e) => {
      this.handleMouseUp(e);
    });
    this.canvas.addEventListener("mouseout", (e) => {
      this.handleMouseOut(e);
    });
  },
};
</script>

<style></style>
