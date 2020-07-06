<template>
  <div id="app" class="app">
    <h1>Shin Megami Tensei IV Tool</h1>
    <div class="app__container no-spacing">
      <div> <!-- allows the stock to remain onscreen with position sticky -->
        <DemonStock
          @more-info="moreInfo"
          class="app__container__stock"
        />
      </div>
      <DemonList
        @more-info="moreInfo"
        class="app__container__demon-list"
      />
    </div>
    <DemonInfo
      :demon="infoDemon ? infoDemon : {}"
      ref="demon-info"
      class="app__more-info hidden"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Ref } from 'vue-property-decorator';
import DemonStock from '@/components/DemonStock.vue';
import DemonList from '@/components/DemonList.vue';
import DemonInfo from '@/components/DemonInfo.vue';

import { Demon } from '@/fusion/demons';

@Component({
  components: { DemonStock, DemonList, DemonInfo },
})
export default class App extends Vue {
  infoDemon: Demon | object = {};

  @Ref('demon-info') demonInfo!: DemonInfo;

  moreInfo(demon: Demon) {
    this.infoDemon = demon;
    this.demonInfo.$el.classList.remove('hidden');
  }
}
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

.app {
  &__more-info {
    margin: 0;
    width: 72rem;
    max-width: 100%;

    height: 48rem;
    max-height: 100%;

    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    z-index: 100;

    box-shadow: 0 0 0 100vmax rgba(0, 0, 0, 0.75);
  }

  &__container {
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
