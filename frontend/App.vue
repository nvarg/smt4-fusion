<template>
  <div id="app">
    <div class="demon-list">
      <DemonCard
        v-for="demon, idx in demons"
        :key="idx"
        :demon="demon"
        class="demon-list__card"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';

import DemonCard from '@/components/DemonCard.vue';
import { Demon } from '@/fusion/demons';

@Component({
  components: { DemonCard },
})
export default class App extends Vue {
  demons: Demon[] = [];

  mounted() {
    for (let page = 1; page < 87; page += 1) {
      axios.get(`${this.$api}/demons?page=${page}`).then((response) => {
        this.demons = [...this.demons, ...response.data.results];
      });
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.demon-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;

  & > .demon-card {
    margin: 0 0 1.65em;
  }

  &__card {
    cursor: pointer;
    transition: transform 0.15s ease-in-out;
  }

  &__card:hover {
    transform: translateY(-0.5em);
  }
}

* {
  margin: 0;
  padding: 0;
}

* + * {
  margin: 0.75em 0 0;
}
</style>
