<template>
  <div id="app">
    <h1>Shin Megami Tensei IV Tool</h1>
    <div class="app__container no-spacing">
      <div> <!-- allows the stock to remain in screen with position sticky -->
        <DemonStock class="app__container__stock"/>
      </div>
      <DemonList class="app__container__demon-list"/>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import DemonStock from '@/components/DemonStock.vue';
import DemonList from '@/components/DemonList.vue';

@Component({
  components: { DemonStock, DemonList },
})
export default class App extends Vue { }
</script>

<style lang="scss">
body {
  box-sizing: border-box;
}

#app {
  margin: auto;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0.75em;
}

.app__container {
  display: flex;

  &__stock {
    position: sticky;
    top: 2.75vh;
    min-width: 34ch;
    margin-right: 1em;
    height: 89vh;
  }

  &__demon-list {
    flex-grow: 1;
  }
}

* {
  margin: 0;
  padding: 0;
}

* + * {
  margin: 0.75em 0 0;
}

.no-spacing > * {
  margin-top: 0;
}
</style>
