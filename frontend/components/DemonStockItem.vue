<template>
  <div
    @click="$emit('more-info', demon)"
    class="demon-stock-item no-spacing"
  >
    <img
      :src="`${$api}/images/charicon/charicon${String(demon.id).padStart(3, '0')}?crop=false`"
      draggable="false"
      class="demon-stock-item__charicon"
    />
    <DemonHeadline :demon="demon" />
    <a
      @click="$emit('remove', demon.id)"
      class="demon-stock-item__remove no-spacing"
    >
      <div>remove</div>
    </a>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Demon } from '@/smt4';

import DemonHeadline from '@/components/DemonHeadline.vue';

@Component({
  components: { DemonHeadline },
})
export default class DemonStockItem extends Vue {
  @Prop({ required: true }) demon!: Demon;
}
</script>

<style lang="scss">
.demon-stock-item {
  display: flex;
  padding: 0.35em;
  cursor: pointer;

  & + & {
    margin-top: 0.22em;
  }

  &__charicon {
    object-fit: contain;
  }

  .demon-headline {
    flex-grow: 1;
    margin-left: 1em;

    &__race {
      color: gray;
    }
  }

  &__remove {
    cursor: pointer;
    color: #f01143;
    padding: 0.25em 0.65em;
    border-radius: 0.35em;
    font-weight: bold;
    font-size: 0.8rem;
    border: 0.125em solid #f01143;
    display: flex;
    align-self: center;

    div {
      transition: transform 0.0s ease-in;
      transform-origin: left center;
      transform: scaleX(0);
      width: 0;
    }

    &:after {
      content: 'x';
    }
  }

  &:hover {
    .demon-stock-item__remove {
      div {
        transition: transform 0.25s ease-in;
        transform: scaleX(1);
        width: auto;
      }

      &:after {
        content: '';
      }
    }
  }
}
</style>
