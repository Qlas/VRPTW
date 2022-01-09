<template>
  <div class="tl-config-dashboard container">
    <h1>Results dashboard</h1>
    <div class="" v-if="!loading_sources">
      <div v-for="(preview, index) of results" :key="index">
        <ResultsTile
          :id="preview.id"
          :name="preview.name"
          :capacity="preview.capacity"
          :cost="preview.cost"
          :resultClient="preview.result_client"
          :isOpen="openedPreviews.includes(preview.name)"
        />
      </div>
    </div>
    <hr />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ResultsTile from "@/components/results/ResultsTile.vue";
export default {
  components: { ResultsTile },
  name: "Results",

  data() {
    return {
      loading_sources: true,
    };
  },

  methods: {
    ...mapActions("results", ["getResults"]),
    ...mapActions("clients", ["getClientDistance"]),
  },

  computed: {
    ...mapGetters("results", ["results"]),
    ...mapGetters("results", ["openedPreviews"]),
  },

  created() {
    this.getResults().then(() => {
      this.getClientDistance().then(() => {
        this.loading_sources = false;
      });
    });
  },
};
</script>
