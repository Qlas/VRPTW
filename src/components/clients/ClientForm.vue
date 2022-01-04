<template>
  <ValidationObserver v-slot="{ handleSubmit }">
    <form @submit.prevent="handleSubmit(processForm)">
      <div class="modal-card" style="width: 40em">
        <header class="modal-card-head">
          <p class="modal-card-title">
            {{ currentData ? `Edit ${currentData.name}` : "Add a new Client" }}
          </p>
        </header>
        <section class="modal-card-body">
          <ValidatedInput
            v-model="name"
            placeholder="Enter a client name"
            maxlength="32"
            :validation="{
              name: 'name',
              rules: 'required|alpha_dash',
            }"
            :field="{ label: 'Name', expanded: true }"
          />

          <ValidatedInput
            v-model="description"
            placeholder="Enter client description"
            type="textarea"
            maxlength="255"
            :validation="{ name: 'Description', rules: '' }"
            :field="{ label: 'Description', expanded: true }"
          />
          <b-table :data="clients.filter((e) => e.name !== startName)">
            <b-table-column v-slot="props" label="Name" width="80pt" centered>
              <p>{{ props.row.name }}</p>
            </b-table-column>

            <b-table-column label="Cost" centered v-slot="props">
              <ValidatedInput
                inputType="b-numberinput"
                v-model="cost[props.row.name]"
                min="0"
                :validation="{
                  rules: 'required|numeric',
                }"
                :showStar="false"
                :field="{}"
              />
            </b-table-column>
            <b-table-column label="Time" centered v-slot="props">
              <ValidatedInput
                inputType="b-numberinput"
                v-model="time[props.row.name]"
                min="0"
                :validation="{
                  rules: 'required|numeric',
                }"
                :showStar="false"
                :field="{}"
              />
            </b-table-column>
          </b-table>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">
            Close
          </button>
          <button class="button is-primary">
            <p v-if="!currentData">Add</p>
            <p v-else>Update</p>
          </button>
        </footer>
      </div>
    </form>
  </ValidationObserver>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "ClientForm",

  props: ["currentData"],

  data() {
    return {
      name: this.currentData ? this.currentData.name : "",
      description: this.currentData ? this.currentData.description : "",
      cost: this.currentData ? this.currentData.cost : {},
      time: this.currentData ? this.currentData.time : {},
      startName: this.currentData ? this.currentData.name : "",
    };
  },

  methods: {
    ...mapActions("clients", ["getClients", "addClient", "updateClient"]),

    processForm() {
      const processFormAction = this.currentData
        ? this.updateClient
        : this.addClient;

      let requestData = {
        name: this.name,
        description: this.description,
        cost: this.cost,
        time: this.time,
      };

      if (this.currentData) {
        requestData = {
          update: {
            payload: {
              name: this.name,
              description: this.description,
              cost: this.cost,
              time: this.time,
            },
            clientId: this.currentData.id,
          },
        };
      }

      const toastMessage = this.currentData
        ? `Updated ${this.name} OS pool`
        : "Added a new OS pool";

      processFormAction(requestData)
        .then(() => {
          this.$parent.close();
          this.$buefy.toast.open({
            message: toastMessage,
            position: "is-top",
            type: "is-primary",
            container: "div.toast-space",
          });
        })
        .catch((err) => {
          this.$errorHandler.handleResponseError(err);
        });
    },
  },

  computed: {
    ...mapGetters("clients", ["clients"]),
  },

  created() {
    this.getClients();
  },
};
</script>
