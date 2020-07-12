<template>
  <div class="demon-headline no-spacing">
    <div class="demon-headline__name">
      <span>Lv.</span>{{ demon.level }} {{ demon.name }}
    </div>
    <div class="demon-headline__race">
      {{ demon.race }}
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Demon } from '@/smt4';

@Component
export default class DemonHeadline extends Vue {
  @Prop({ required: true }) demon!: Demon;
}
</script>

<style lang="scss">
.demon-headline {
  display: flex;
  flex-direction: column;

  &__name {
    span {
      font-size: 0.75em;
    }
  }

  &__race {
    font-size: 0.75em;
    text-transform: uppercase;
  }
}
</style>
