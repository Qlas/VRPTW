<template>
  <div class="home">
    <section class="hero is-primary is-bold is-relative">
      <div class="hero-body">
        <div class="container has-text-centered">
          <transition name="slide-down">
            <h1 v-if="showElements" class="title is-size-1 is-spaced">VRPTW</h1>
          </transition>
          <transition name="slide-up-200ms">
            <h3 v-if="showElements" class="subtitle">
              Vehicle Routing Problem with Time Windows
            </h3>
          </transition>
        </div>
      </div>
      <div class="hero-foot">
        <div class="section has-smaller-padding">
          <div class="container">
            <div class="column is-12 has-text-centered">
              <transition name="slow-in-300ms">
                <div v-if="showElements">
                  <p class="is-unselectable">
                    Version
                    {{ tag !== "null" && tag_distance == 0 ? tag : hash }}
                  </p>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="hero is-lighter is-unselectable">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="columns is-centered is-multiline is-mobile">
            <div class="column is-half-mobile has-text-centered">
              <p class="title is-4 has-text-weight-semibold">Powerfull</p>
              <p
                class="subtitle is-6 has-text-grey-light"
                v-html="
                  'Control your routes with a single click'.replace(
                    '<b>',
                    '<b class=has-text-grey>'
                  )
                "
              ></p>

              <b-icon
                size="is-medium"
                type="is-danger"
                icon="speedometer-medium"
              ></b-icon>
            </div>

            <div class="column is-half-mobile has-text-centered">
              <p class="title is-4 has-text-weight-semibold">Intuitive</p>
              <p
                class="subtitle is-6 has-text-grey-light"
                v-html="
                  'Simple desing for busy people'.replace(
                    '<b>',
                    '<b class=has-text-grey>'
                  )
                "
              ></p>

              <b-icon
                size="is-medium"
                type="is-success"
                icon="head-check-outline"
              ></b-icon>
            </div>

            <div class="column is-half-mobile has-text-centered">
              <p class="title is-4 has-text-weight-semibold">Modern</p>
              <p
                class="subtitle is-6 has-text-grey-light"
                v-html="
                  'Say goodbye to php-like look '.replace(
                    '<b>',
                    '<b class=has-text-grey>'
                  )
                "
              ></p>

              <b-icon
                size="is-medium"
                type="is-info"
                icon="pencil-ruler"
              ></b-icon>
            </div>

            <div class="column is-half-mobile has-text-centered">
              <p class="title is-4 has-text-weight-semibold">Informative</p>
              <p
                class="subtitle is-6 has-text-grey-light"
                v-html="
                  'No details left unspoken'.replace(
                    '<b>',
                    '<b class=has-text-grey>'
                  )
                "
              ></p>

              <b-icon
                size="is-medium"
                type="is-warning"
                icon="chart-scatter-plot-hexbin"
              ></b-icon>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  components: {},
  computed: {
    ...mapGetters("auth", ["isAuthenticated", "authUser"]),
  },
  data() {
    return {
      showElements: false,
      hash: process.env.VUE_APP_GIT_HASH,
      tag: process.env.VUE_APP_GIT_TAG,
      tag_distance: process.env.VUE_APP_GIT_DISTANCE,
    };
  },
  mounted() {
    this.showElements = true;
  },
};
</script>
<style scoped lang="scss">
@import "@/styles/colors.scss";

section.hero.is-primary {
  background-image: linear-gradient($primary, $secondary);
}
@keyframes disappear {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
@keyframes slideDown {
  0% {
    opacity: 0;
    transform: translateY(-1rem);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(1rem);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slowIn {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
//Animation: Slide down • 0s
.slide-down-enter-active {
  animation: slideDown 0.4s ease-out;
}
.slide-down-enter,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-1rem);
}
.slide-down-leave,
.slide-down-enter-to {
  opacity: 1;
  transform: translateY(0);
}
//Animation: Slide up • 0.2s
.slide-up-200ms-enter-active {
  animation: disappear 0s forwards, slideUp 0.4s ease-out 0.2s; //name, duration, timing-function, delay, iteration-count, direction, fill-mode.
}
.slide-up-200ms-enter,
.slide-up-200ms-leave-to {
  opacity: 0;
  transform: translateY(1rem);
}
.slide-up-200ms-leave,
.slide-up-200ms-enter-to {
  opacity: 1;
  transform: translateY(0);
}
//Animation: Slow in • 0.3s, 0.4s, 0.5s, 0.6s, 0.7s
.slow-in-300ms-enter-active {
  animation: disappear 0s forwards, slowIn 0.4s ease-out 0.3s;
}
.slow-in-400ms-enter-active {
  animation: disappear 0s forwards, slowIn 0.4s ease-out 0.4s;
}
.slow-in-500ms-enter-active {
  animation: disappear 0s forwards, slowIn 0.4s ease-out 0.5s;
}
.slow-in-600ms-enter-active {
  animation: disappear 0s forwards, slowIn 0.4s ease-out 0.6s;
}
.slow-in-700ms-enter-active {
  animation: disappear 0s forwards, slowIn 0.4s ease-out 0.7s;
}
.slow-in-300ms-enter,
.slow-in-300ms-leave-to,
.slow-in-400ms-enter,
.slow-in-400ms-leave-to,
.slow-in-500ms-enter,
.slow-in-500ms-leave-to,
.slow-in-600ms-enter,
.slow-in-600ms-leave-to,
.slow-in-700ms-enter,
.slow-in-700ms-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
.slow-in-300ms-leave,
.slow-in-300ms-enter-to,
.slow-in-400ms-leave,
.slow-in-400ms-enter-to,
.slow-in-500ms-leave,
.slow-in-500ms-enter-to,
.slow-in-600ms-leave,
.slow-in-600ms-enter-to,
.slow-in-700ms-leave,
.slow-in-700ms-enter-to {
  opacity: 1;
  transform: scale(1);
}

.home {
  margin-top: -30pt;
}
</style>
