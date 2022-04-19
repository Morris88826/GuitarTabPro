import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
// import "bootstrap/scss/bootstrap.scss";
import router from "./routers";
import axios from "axios";
import VueAxios from "vue-axios";
import "mdb-vue-ui-kit/css/mdb.min.css";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

const app = createApp(App);
axios.defaults.baseURL = "http://127.0.0.1:5000";

app.use(Antd);
app.use(router);
app.use(VueAxios, axios);
app.mount("#app");
