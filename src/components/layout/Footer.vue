<template>
  <footer class="footer">
    <nav class="level container">
      <div class="level-right">
        <div>
          <div class="level-item">
            <img src="@/assets/logo.png" :style="{ maxHeight: '70px' }" />
            <p style="margin-left: 20px">
              <router-link to="/"><strong>VRPTW</strong></router-link>
            </p>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; margin-left: 450px">
          <router-link
            v-for="route in $router.options.routes"
            :key="route.path"
            v-bind:class="{ isOn: route.path == $route.path }"
            :to="route.path"
            >{{
              route.meta.canBeOnFooter &&
              (route.meta.requiresAuth ? isAuthenticated : true)
                ? route.name
                : null
            }}</router-link
          >
        </div>
      </div>
      <div class="level-left"></div>
    </nav>
  </footer>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Footer",
  computed: {
    ...mapGetters(["isAuthenticated"]),
  },
};
</script>

<style scoped>
.footer {
  padding: 2rem 1rem 2rem;
  background-color: rgb(228, 228, 228);
}
.isOn {
  color: rgb(15, 10, 0);
}
</style>
