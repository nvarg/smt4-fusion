<template>
  <div
    @drop="drop"
    @dragover.prevent
    @dragenter.prevent="dragEnter"
    @dragleave.prevent="dragLeave"
    class="demon-stock">
    <h2>Stock ({{ demons.length }} / 20)</h2>
    <div>
      <DemonStockItem
        v-for="demon in demons"
        :key="demon.id"
        :demon="demon"
        @remove="remove"
        class="demon-stock__item"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Demon } from '@/fusion/demons';

import DemonStockItem from '@/components/DemonStockItem.vue';

@Component({
  components: { DemonStockItem },
})
export default class DemonStock extends Vue {
  demons: Demon[] = []

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
  outline: 0.125em dotted sandybrown;
  overflow-y: auto;
  padding: 1em;

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
