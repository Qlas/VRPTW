<template>
  <article class="tile is-child box">
    <ValidationObserver v-slot="{ handleSubmit }">
      <form @submit.prevent="handleSubmit(processForm)">
        <section>
          <div class="columns">
            <ValidatedInput
              class="column is-half"
              v-model="name"
              placeholder="Enter a calculation name"
              maxlength="32"
              :validation="{
                name: 'name',
                rules: 'required|alpha_dash',
              }"
              :field="{ label: 'Name', expanded: true }"
            />
            <ValidatedInput
              class="column is-half"
              inputType="b-numberinput"
              v-model="capacity"
              min="1"
              :validation="{
                rules: 'required|numeric',
              }"
              :field="{ label: 'Truck Capacity' }"
            />
          </div>
          <b-table :data="chosenClients">
            <b-table-column label="Name" centered v-slot="props">
              {{ props.row.name }}
            </b-table-column>
            <b-table-column label="Start" centered v-slot="props">
              <ValidatedInput
                inputType="b-numberinput"
                v-model="start[props.row.name]"
                min="0"
                :max="end[props.row.name]"
                :validation="{
                  rules: 'required|numeric',
                }"
                :showStar="false"
                :field="{}"
              />
            </b-table-column>
            <b-table-column label="End" centered v-slot="props">
              <ValidatedInput
                inputType="b-numberinput"
                v-model="end[props.row.name]"
                :min="start[props.row.name]"
                :validation="{
                  rules: 'required|numeric',
                }"
                :showStar="false"
                :field="{}"
              />
            </b-table-column>
            <b-table-column label="Demand" centered v-slot="props">
              <ValidatedInput
                inputType="b-numberinput"
                v-model="demand[props.row.name]"
                min="0"
                :validation="{
                  rules: 'required|numeric',
                }"
                :showStar="false"
                :field="{}"
              />
            </b-table-column>
            <template #empty>
              <div class="has-text-centered">No records</div>
            </template>
            <template #footer>
              <b-button
                style="width: 100%"
                @click="() => (isCardModalActive = true)"
              >
                Select Clients</b-button
              >
            </template>
          </b-table>
          <button class="button is-primary is-pulled-right">Calculate</button>
        </section>
      </form>
    </ValidationObserver>

    <b-modal v-model="isCardModalActive" :width="640" scroll="keep">
      <section>
        <div class="card">
          <header class="modal-card-head">Select Clients</header>

          <b-field>
            <b-select
              multiple
              v-model="chosenClients"
              @input="changeSelectValue"
            >
              <option
                v-for="option in clients.slice(1)"
                :value="option"
                :key="option.id"
              >
                {{ option.name }}
              </option>
            </b-select>
          </b-field>
          <footer class="modal-card-foot">
            <button
              class="button"
              type="button"
              @click="isCardModalActive = false"
            >
              Close
            </button>
          </footer>
        </div>
      </section>
    </b-modal>
  </article>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";

export default {
  name: "CalculateForm",

  props: [],

  data() {
    return {
      capacity: 1,
      name: "",
      start: {},
      end: {},
      demand: {},
      chosenClients: [],
      isCardModalActive: false,
    };
  },

  methods: {
    ...mapActions("clients", ["getClients", "addClient", "updateClient"]),
    ...mapMutations("results", ["openPreview", "clearPreview"]),
    ...mapActions("results", ["addResult"]),

    changeSelectValue(chosenClients) {
      for (let client of chosenClients) {
        if (this.start[client.name] === undefined) {
          this.start[client.name] = this.end[client.name] = 0;
          this.demand[client.name] = 1;
        }
      }
    },

    processForm() {
      if (Object.keys(this.chosenClients).length === 0) {
        this.$buefy.toast.open({
          message: `You should select at least one client!`,
          position: "is-top",
          type: "is-danger",
          container: "div.toast-space",
        });
        return;
      }

      let requestData = {
        name: this.name,
        capacity: this.capacity,
        clients: {},
      };

      for (let client of this.chosenClients) {
        requestData.clients[client.name] = {
          start: this.start[client.name],
          end: this.end[client.name],
          demand: this.demand[client.name],
        };
      }

      this.addResult(requestData)
        .then((result) => {
          this.clearPreview();
          this.openPreview(result.name);
          this.$buefy.toast.open({
            message: "Added a new Calculation",
            position: "is-top",
            type: "is-primary",
            container: "div.toast-space",
          });
          this.$router.push("/results");
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
