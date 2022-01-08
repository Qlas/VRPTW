<template>
  <b-navbar
    class="is-spaced has-shadow mb-2"
    type="is-primary"
    wrapper-class="container"
  >
    <template slot="brand">
      <b-navbar-item :to="{ path: '/' }" tag="router-link">
        <b-icon :style="{ margin: '6px' }" icon="account-hard-hat"></b-icon>
        <transition name="slide-left">
          <p
            v-if="$route.path !== '/'"
            class="subtitle is-5 is-unselectable has-spacing no-wrap"
            style="color: white"
          >
            VRPTW
          </p>
        </transition>
      </b-navbar-item>
    </template>
    <template slot="start">
      <b-navbar-item :to="{ path: '/results' }" tag="router-link">
        <b-icon :style="{ margin: '6px' }" icon="view-list-outline" />
        <p class="is-unselectable">Results</p>
      </b-navbar-item>
      <b-navbar-item :to="{ path: '/calculate' }" tag="router-link">
        <b-icon :style="{ margin: '6px' }" icon="calculator" />
        <p class="is-unselectable">Calculate</p>
      </b-navbar-item>
      <b-navbar-item
        :to="{ path: '/clients' }"
        tag="router-link"
        v-if="isAuthenticated && $permissions.client.any(authUser)"
      >
        <b-icon :style="{ margin: '6px' }" icon="human-edit" />
        <p class="is-unselectable">Clients</p>
      </b-navbar-item>
    </template>

    <template slot="end">
      <b-dropdown :triggers="['hover']" v-if="isAuthenticated">
        <button class="button is-primary" slot="trigger">
          <b-icon icon="account"></b-icon>
          {{ authUser.username }}
          <b-icon icon="menu-down"></b-icon>
        </button>

        <b-dropdown-item aria-role="listitem" @click="logout">
          <div class="media">
            <b-icon class="media-left" icon="account-cancel"></b-icon>
            <div class="media-content">
              <p>Logout</p>
            </div>
          </div>
        </b-dropdown-item>
      </b-dropdown>
      <b-navbar-item v-else tag="div">
        <div class="buttons">
          <b-button tag="router-link" to="/login" type="is-secondary">
            <strong>Sign in</strong>
          </b-button>
        </div>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { NotificationProgrammatic as Notification } from "buefy";

export default {
  name: "Navbar",

  computed: {
    ...mapGetters("auth", ["isAuthenticated", "authUser"]),
  },

  methods: {
    ...mapActions("auth", ["endAuthSession"]),

    logout() {
      this.endAuthSession();
      if (this.$route.path != "/") {
        this.$router.push("/");
      }
      Notification.open({
        message: "Logout complete",
        type: "is-success",
        hasIcon: true,
      });
    },
  },
};
</script>

<style scoped lang="scss">
@keyframes slideLeftIn {
  0% {
    opacity: 0;
    transform: translateX(-1rem);
    max-width: 0px;
  }
  100% {
    opacity: 1;
    transform: translateX(0);
    max-width: 120px;
  }
}
@keyframes slideLeftOut {
  0% {
    opacity: 1;
    transform: translateX(0);
    max-width: 120px;
  }
  100% {
    opacity: 0;
    transform: translateX(-1rem);
    max-width: 0px;
  }
}
//Animation: Slide left
.slide-left-enter-active {
  animation: slideLeftIn 0.4s ease-out;
}
.slide-left-leave-active {
  animation: slideLeftOut 0.4s ease-in;
}
.slide-left-enter,
.slide-left-leave-to {
  opacity: 0;
  max-width: 0px;
  transform: translateX(-1rem);
}
.slide-left-leave,
.slide-left-enter-to {
  opacity: 1;
  max-width: 120px;
  transform: translateX(0);
}
.no-wrap {
  white-space: nowrap;
}
.navbar.has-shadow {
  box-shadow: 0px 1px 0px hsla(0, 0%, 100%, 0.2);
}
</style>
