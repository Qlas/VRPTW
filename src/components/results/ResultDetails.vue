<template>
  <div class="box">
    <network ref="network" :nodes="nodes" :edges="edges" :options="options" />
  </div>
</template>

<script>
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
      for (let client of this.resultClient) {
        if (client.position > maxPos) maxPos = client.position;
        nodes.push({
          id: client.id,
          label: client.client + "\n" + client.start_of_service,
          shape: "box",
          x: client.position * 100,
          y: (client.truck - (this.trucks.length - 1) / 2) * 50,
        });
      }

      nodes.push({
        id: -1,
        label: "Depot",
        shape: "box",
        x: (maxPos + 1) * 100,
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
        for (let id in truck) {
          edges.push({
            from: before,
            to: truck[id].id,
            arrows: "to",
          });
          before = truck[id].id;
        }
        edges.push({
          from: before,
          to: -1,
          arrows: "to",
        });
      }
      return edges;
    },
  },
};
</script>
