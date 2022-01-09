<template>
  <div class="box">
    <network ref="network" :nodes="nodes" :edges="edges" :options="options" />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ResultsDetails",

  components: {},

  props: ["resultClient"],
  data() {
    return {
      trucks: [],
      options: {
        nodes: {
          borderWidth: 4,
          physics: false,
        },
        edges: {
          color: "lightgray",
        },
      },
    };
  },
  computed: {
    ...mapGetters("clients", ["clientDistance"]),
    nodes() {
      let nodes = [];
      nodes.push({
        id: 0,
        label: "Depot",
        shape: "box",
        x: 0,
        y: 0,
      });
      this.edges;
      let maxPos = 0;
      let client_before = "";
      for (let client of this.resultClient) {
        if (client.position > maxPos) maxPos = client.position;
        nodes.push({
          id: client.id,
          label: client.client + "\n" + client.start_of_service,
          shape: "box",
          x: client.position * 150,
          y: (client.truck - (this.trucks.length - 1) / 2) * 50,
        });
        client_before = client.client;
      }

      nodes.push({
        id: -1,
        label: "Depot",
        shape: "box",
        x: (maxPos + 1) * 150,
        y: 0,
      });
      return nodes;
    },
    edges() {
      let edges = [];
      for (let client of this.resultClient) {
        if (this.trucks[client.truck] === undefined)
          this.trucks[client.truck] = {};
        this.trucks[client.truck][client.position] = {
          client: client.client,
          id: client.id,
        };
      }
      for (let truck of this.trucks) {
        let before = 0;
        let before_client = "Depot";
        for (let id in truck) {
          console.log;
          edges.push({
            from: before,
            to: truck[id].id,
            arrows: "to",
            label:
              "" +
              this.clientDistance.find((obj) => {
                return (
                  (obj.client1 === before_client &&
                    obj.client2 === truck[id].client) ||
                  (obj.client2 === before_client &&
                    obj.client1 === truck[id].client)
                );
              }).time,
          });
          before = truck[id].id;
          before_client = truck[id].client;
        }
        edges.push({
          from: before,
          to: -1,
          arrows: "to",
          label:
            "" +
            this.clientDistance.find((obj) => {
              return (
                (obj.client1 === before_client && obj.client2 === "Depot") ||
                (obj.client2 === before_client && obj.client1 === "Depot")
              );
            }).time,
        });
      }
      return edges;
    },
  },
};
</script>
