<template>
  <div class="tl-config-dashboard container">
    <h1>Calculate dashboard</h1>
    <div class="tile is-ancestor">
      <div class="tile is-vertical">
        <CalculateForm />
      </div>
    </div>
    <hr />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import CalculateForm from "@/components/calculate/CalculateForm.vue";
export default {
  components: { CalculateForm },
  name: "Calculate",

  data() {
    return {};
  },

  methods: {
    ...mapActions("clients", ["getClients", "removeClient"]),
  },

  computed: {
    ...mapGetters("clients", ["clients"]),
  },

  created() {},
};
</script>
