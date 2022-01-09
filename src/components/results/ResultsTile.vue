<template>
  <div>
    <div class="box preview-trigger">
      <div class="columns is-vcentered">
        <div class="column" @click="onPreviewClick">
          <div class="columns is-vcentered">
            <div class="column is-1 group-options">
              <b-icon
                :icon="isOpen ? 'chevron-down' : 'chevron-right'"
                type="is-primary"
                size="is-medium"
              />
            </div>
            <div class="column is-3">
              <h2>{{ name }}</h2>
            </div>
            <div class="column is-offset-4">
              <b-field grouped>
                <div class="control tl-count-tag">
                  <b-taglist attached>
                    <b-tag type="is-success">Max Capacity</b-tag>
                    <b-tag class="is-dark">{{ padInt(capacity) }}</b-tag>
                  </b-taglist>
                </div>

                <div class="control tl-count-tag">
                  <b-taglist attached>
                    <b-tag type="is-warning">Total Cost</b-tag>
                    <b-tag type="is-dark">{{ padInt(cost ? cost : 0) }}</b-tag>
                  </b-taglist>
                </div>
              </b-field>
            </div>
          </div>
        </div>
        <div class="column is-1">
          <b-button
            class="is-danger"
            icon-left="trash-can"
            @click="openDeleteDialog"
            >Delete</b-button
          >
        </div>
      </div>
    </div>
    <b-collapse class="preview-tile" animation="slide" :open="isOpen">
      <ResultDetails :resultClient="resultClient" :key="componentKey" />
    </b-collapse>
  </div>
</template>

<script>
import { mapActions, mapMutations } from "vuex";
import ResultDetails from "@/components/results/ResultDetails.vue";

export default {
  name: "ResultTile",

  components: { ResultDetails },

  props: [
    "id",
    "name",
    "info",
    "capacity",
    "cost",
    "user",
    "isOpen",
    "resultClient",
  ],
  data() {
    return { componentKey: 0 };
  },
  methods: {
    ...mapMutations("results", ["openPreview", "closePreview"]),
    ...mapActions("results", ["removeResult"]),
    onPreviewClick() {
      if (this.isOpen) this.closePreview(this.name);
      else {
        this.openPreview(this.name);
        this.componentKey += 1;
      }
    },

    padInt(value) {
      return value.toString().padStart(2, "0");
    },

    openDeleteDialog() {
      this.$buefy.dialog.confirm({
        title: "Deleting Client",
        message: `Are you sure you want to <b>delete</b> Result ${this.name}?`,
        confirmText: "Delete ",
        type: "is-danger",
        hasIcon: true,
        onConfirm: () => {
          this.removeResult(this.id)
            .then(() => {
              this.$buefy.toast.open({
                message: `Result ${this.name} deleted!`,
                position: "is-top",
                type: "is-primary",
                container: "div.toast-space",
              });
            })
            .catch((err) => {
              this.$errorHandler.handleResponseError(err);
            });
        },
      });
    },
  },
};
</script>

<style lang="scss">
.preview-tile {
  margin: -1.3em 0 2.5em 0;
}

.preview-trigger {
  cursor: pointer;
}

.tl-count-tag {
  margin: 0 1.5em;
}

.tl-count-tag-total {
  margin-left: 9.5em;
}

.group-options {
  width: 3% !important;
}
</style>