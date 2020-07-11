<template>
  <div
    @drop="drop"
    @dragover.prevent
    @dragenter.prevent="dragEnter"
    @dragleave.prevent="dragLeave"
    class="demon-stock">
    <h2>Stock ({{ demons.length }} / 20)</h2>
    <transition-group
      name="demon-stock__item-"
    >
      <DemonStockItem
        v-for="demon in demons"
        :key="demon.id"
        :demon="demon"
        @remove="remove"
        @more-info="(demon) => $emit('more-info', demon)"
        class="demon-stock__item"
      />
    </transition-group>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import axios from 'axios';

import DemonStockItem from '@/components/DemonStockItem.vue';
import { Demon } from '@/smt4';

@Component({
  components: { DemonStockItem },
})
export default class DemonStock extends Vue {
  demons: Demon[] = []

  mounted() {
    const demons = document?.cookie
      ?.split('; ')
      ?.find((c) => c.startsWith('stock'))
      ?.split('=')[1];

    axios.get(`${this.$api}/demons`, {
      params: { ids: demons },
    }).then((response) => {
      this.demons = response.data;
    });
  }

  @Watch('demons')
  save() {
    document.cookie = `stock=${this.demons.map((d) => d.id)}`;
  }

  drop(event: DragEvent) {
    this.dragLeave();
    const data = event.dataTransfer?.getData('application/json');

    if (data) {
      const demon = JSON.parse(data) as Demon;
      if (this.demons.length < 20
        && this.demons.findIndex((value) => value.id === demon.id) === -1) {
        this.demons.push(demon);
      }
    }
  }

  dragEnter(event: DragEvent) {
    const data = event.dataTransfer?.getData('application/json');

    if (data) {
      this.$el.classList.add('drag-over');
      const demon = JSON.parse(data) as Demon;
      if (this.demons.length >= 20
        || this.demons.findIndex((value) => value.id === demon.id) !== -1) {
        this.$el.classList.add('drag-over--disabled');
      }
    }
  }

  dragLeave() {
    this.$el.classList.remove('drag-over');
    this.$el.classList.remove('drag-over--disabled');
  }

  remove(demonId: number) {
    this.demons = this.demons.filter((item) => item.id !== demonId);
  }
}
</script>

<style lang="scss">
.demon-stock {
  display: flex;
  flex-direction: column;
  outline: 0.125em dotted sandybrown;
  overflow-y: auto;
  padding: 1em;

  &__item {
    &--enter, &--leave-to {
      transform: translateX(-100%);
    }

    &--enter-active {
      transition: all 0.6s ease;
    }

    &--leave-active {
      transition: all 0.2s ease;
    }
  }

  &.drag-over {
    outline: 0.25em solid sandybrown;

    & > * {
      pointer-events: none;
    }

    &--disabled {
      background-color: transparentize($color: #f03, $amount: 0.6);
    }
  }
}
</style>
