<template>
  <div class="tl-config-dashboard container">
    <h1>Clients config dashboard</h1>
    <div class="buttons">
      <b-button
        class="is-primary ml-2"
        icon-left="plus-thick"
        @click="openCreateModal"
        v-if="$permissions.client.canAdd(authUser)"
      >
        Add new client
      </b-button>
    </div>

    <hr />
    <div
      class="columns is-centered"
      v-for="(clientGroup, index) of clientsGrouped"
      :key="index"
    >
      <div
        class="column is-two-fifths"
        v-for="(osp, index) of clientGroup"
        :key="index"
      >
        <div class="card">
          <div class="card-content">
            <p class="title">
              {{ osp.name }}
            </p>
            <div class="columns">
              <div class="column">
                <b-table :data="[osp]" card-layout>
                  <b-table-column label="Description:">
                    <p style="word-break: break-all; max-width: 300pt">
                      {{ osp.description }}
                    </p>
                  </b-table-column>
                </b-table>
              </div>
            </div>
          </div>

          <footer class="card-footer">
            <b-button
              class="card-footer-item is-dark"
              icon-left="pencil"
              inverted
              @click="openEditModal(osp)"
              v-if="$permissions.client.canChange(authUser)"
              >Edit</b-button
            >
            <b-button
              class="card-footer-item is-danger"
              icon-left="trash-can"
              inverted
              @click="openDeleteDialog(osp)"
              v-if="$permissions.client.canDelete(authUser)"
              >Delete</b-button
            >
          </footer>
        </div>
      </div>
    </div>

    <b-modal
      :active.sync="isClientModalActive"
      has-modal-card
      trap-focus
      aria-role="dialog"
      aria-modal
    >
      <ClientForm :currentData="ClientEdit" />
    </b-modal>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import ClientForm from "@/components/clients/ClientForm.vue";
export default {
  components: {
    ClientForm,
  },
  name: "Clients",

  data() {
    return {
      groupSize: 2,
      isClientModalActive: false,
      ClientEdit: {},
    };
  },

  methods: {
    ...mapActions("clients", ["getClients", "removeClient"]),

    openCreateModal() {
      this.ClientEdit = null;
      this.isClientModalActive = true;
    },
    openEditModal(osp) {
      this.ClientEdit = osp;
      this.isClientModalActive = true;
    },

    openDeleteDialog(osp) {
      this.$buefy.dialog.confirm({
        title: "Deleting Client",
        message: `Are you sure you want to <b>delete</b> Client ${osp.name}?`,
        confirmText: "Delete ",
        type: "is-danger",
        hasIcon: true,
        onConfirm: () => {
          this.removeClient(osp.id)
            .then(() => {
              this.$buefy.toast.open({
                message: `Client ${osp.name} deleted!`,
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

  computed: {
    ...mapGetters("clients", ["clients"]),
    ...mapGetters("auth", ["isAuthenticated", "authUser"]),

    clientsGrouped() {
      let clientsGrouped = [];
      let clientsCopy = [...this.clients];
      clientsCopy = clientsCopy.slice(1);

      while (clientsCopy.length) {
        clientsGrouped.push(clientsCopy.splice(0, this.groupSize));
      }

      return clientsGrouped;
    },
  },

  created() {
    this.getClients();
  },
};
</script>
