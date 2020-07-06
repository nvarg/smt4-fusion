<template>
  <div
    @click="$emit('more-info', demon)"
    class="demon-stock-item no-spacing"
  >
    <img
      :src="`${$api}/images/charicon/charicon${String(demon.id).padStart(3, '0')}`"
      draggable="false"
      class="demon-stock-item__charicon"
    />
    <div class="demon-stock-item__name">
      <span>Lv.</span>{{ demon.level }} {{ demon.name }}
    </div>
    <div class="demon-stock-item__race">
      {{ demon.race }}
    </div>
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
import { Demon } from '@/fusion/demons';

@Component
export default class DemonStockItem extends Vue {
  @Prop({ required: true }) demon!: Demon;
}
</script>

<style lang="scss">
.demon-stock-item {
  display: grid;
  margin-top: 0;
  grid-template-columns: 3em 1fr auto;
  padding: 0.15em 0;
  padding: 0.35em;
  cursor: pointer;

  animation: 0.3s ease-out 0s 1 slideInFromLeft;
  @keyframes slideInFromLeft {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(0);
    }
  }

  & + & {
    margin-top: 0.22em;
  }

  &__charicon {
    object-fit: contain;
    grid-area: 1/1/3/2;
    align-self: center;
    justify-self: start;
  }

  &__name {
    span {
      font-size: 0.75rem;
    }
  }

  &__race {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: gray;
    grid-area: 2/2/3/3;
  }

  &__remove {
    cursor: pointer;
    align-self: center;
    justify-self: end;
    grid-area: 1/3/3;
    color: #f01143;
    padding: 0.25em 0.65em;
    border-radius: 0.35em;
    font-weight: bold;
    font-size: 0.8rem;
    border: 0.125em solid #f01143;
    display: flex;

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
