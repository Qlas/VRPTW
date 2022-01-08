<template>
  <div class="tl-config-dashboard container">
    <h1>Results dashboard</h1>
    <div v-for="(preview, index) of results" :key="index">
      <ResultsTile
        :id="preview.name"
        :name="preview.name"
        :capacity="preview.capacity"
        :cost="preview.cost"
      />
    </div>
    <hr />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import CalculateForm from "@/components/calculate/CalculateForm.vue";
import ResultsTile from "@/components/results/ResultsTile.vue";
export default {
  components: { ResultsTile },
  name: "Results",

  data() {
    return {};
  },

  methods: {
    ...mapActions("results", ["getResults"]),
  },

  computed: {
    ...mapGetters("results", ["results"]),
  },

  created() {
    this.getResults();
  },
};
</script>
