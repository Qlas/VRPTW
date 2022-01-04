<template>
    <div id="app">
        <Navbar />
        <Announcement v-if="this.$route.name !== 'Home' || isAuthenticated" />
        <div class="content">
            <div class="toast-space"></div>
            <router-view />
        </div>
        <Footer />
    </div>
</template>

<script>
var head = document.getElementsByTagName("head")[0];

var mdilink = document.createElement("link");
mdilink.id = "MaterialDesign";
mdilink.rel = "stylesheet";
mdilink.type = "text/css";
mdilink.media = "all";

var falink = document.createElement("link");
falink.id = "FontAwesome";
falink.rel = "stylesheet";
falink.type = "text/css";
falink.media = "all";

var mdiRequest = new Request(
    "https://cdn.materialdesignicons.com/5.8.55/css/materialdesignicons.min.css"
);
var faRequest = new Request(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css"
);
fetch(faRequest).then(function () {
    falink.href =
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css";
});

fetch(mdiRequest)
    .then(function (value) {
        if (value.status == 404) {
            throw new Error("Redirected page not found");
        }
        mdilink.href =
            "https://cdn.materialdesignicons.com/5.8.55/css/materialdesignicons.min.css";
    })
    .catch(() => {
        mdilink.href =
            "https://cdnjs.cloudflare.com/ajax/libs/MaterialDesign-Webfont/5.8.55/css/materialdesignicons.min.css";
    });
head.appendChild(mdilink);
head.appendChild(falink);

import { mapGetters } from "vuex";
// @ is an alias to /src
import Announcement from "@/components/layout/Announcement.vue";
import Navbar from "@/components/layout/Navbar.vue";
import Footer from "@/components/layout/Footer.vue";

export default {
    name: "Home",
    components: {
        Announcement,
        Navbar,
        Footer,
    },
    computed: {
        ...mapGetters("auth", ["isAuthenticated"]),
    },
};
</script>

<style lang="scss">
// CUSTOM
body {
    scroll-behavior: smooth;
}

.toast-space {
    pointer-events: none;
    height: 70pt;
    width: 100%;
    position: fixed;
    z-index: 100;
    margin-top: -40pt;
}

.content {
    flex-grow: 1;
}

#app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
.gitlab-background {
    background-image: linear-gradient(#ff4500, #ffa500);
}

.confluence-background {
    background-image: linear-gradient(#4e51ec, #00c3ff);
}

//BUEFY

// Import Bulma's core
@import "~bulma/sass/utilities/_all";
@import "@/styles/colors.scss";

// Setup $colors to use as bulma classes (e.g. 'is-twitter')
$addColors: (
    "primary": (
        $primary,
        $primary-invert,
    ),
    "secondary": (
        $secondary,
        $secondary-invert,
    ),
);

$colors: map-merge($colors, $addColors);

// Links
$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
