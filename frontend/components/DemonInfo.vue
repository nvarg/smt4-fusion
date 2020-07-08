<template>
  <div class="demon-info no-spacing">
    <div
      @click.prevent="close"
      class="demon-info__close"
    >
      close
    </div>
    <img
      :src="imageUrl"
      draggable="false"
      class="demon-info__image"
    />
    <div class="demon-info__lore">
      <h3>Lore</h3>
      <p v-for="(loreText, idx) in lore" :key="idx">{{ loreText }}</p>
    </div>
    <div class="demon-info__stats">
      <Statgram
        :num="7"
        :stats="stats"
        :max="[1100, 500, 130, 130, 130, 130, 130]"
        :labels="['Health', 'Mana', 'Strength', 'Dexterity', 'Magic', 'Agility', 'Luck']"
        :size="400"
        fill="rgba(255, 177, 20, 0.75)"
      />
    </div>
    <div class="demon-info__fusions">
      <h3>Fusions</h3>
    </div>
    <div class="demon-info__skill">
      <h3>Skills</h3>
      <h3>Level Up Skills</h3>
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Vue,
  Prop,
  Watch,
} from 'vue-property-decorator';
import axios from 'axios';

import { Demon } from '@/fusion/demons';
import DemonCard from '@/components/DemonCard.vue';
import Statgram from '@/components/Statgram.vue';

@Component({
  components: { DemonCard, Statgram },
})
export default class DemonInfo extends Vue {
  @Prop({ required: true }) demon!: Demon;

  lore: string[] = [];

  cancelToken = axios.CancelToken.source();

  close() {
    this.$el.classList.add('hidden');
  }

  @Watch('demon')
  updateLoreText() {
    axios.get(`${this.$api}/demons/${this.demon.id}/lore`, {
      cancelToken: this.cancelToken.token,
    }).then(
      (response) => { this.lore = response.data as string[]; },
    );
  }

  get imageUrl() {
    return `${this.$api}/images/devbu/devbu${String(this.demon.id).padStart(3, '0')}`
      + '?max_width=300&max_height=700&background_color=%23cecece';
  }

  get stats() {
    if (this.demon.id === undefined) {
      return Array.from({ length: 7 }, () => 0);
    }

    return [
      this.demon.health,
      this.demon.mana,
      this.demon.strength,
      this.demon.dexterity,
      this.demon.magic,
      this.demon.agility,
      this.demon.luck,
    ];
  }
}
</script>

<style lang="scss">
.demon-info {
  display: grid;
  grid-gap: 1em;
  background-color: #cecece;
  border: 0.15em solid gray;
  border-radius: 0.25em;
  padding: 1em;

  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr 2fr;

  &.hidden {
    display: none;
  }

  &__close {
    position: absolute;
    cursor: pointer;
    color: #f01036;
    font-weight: bold;
    font-size: 0.8rem;
    border: 0.185em solid #f01036;
    border-radius: 0.25em;
    padding: 0.25em 0.75em;
    top: 1ch;
    right: 1ch;

    &::after {
      content: 'x';
    }
  }

  &__image {
    margin: auto;
    margin-top: auto !important;
    grid-area: 1/1/3/2;
  }

  &__stats {
    grid-area: 1/2;
    padding: 3.5em;
  }

  &__lore {
    grid-area: 2/2;
    position: relative;
    max-height: 100%;
    overflow: hidden;
    line-height: 1.5;

    &::after {
      position: absolute;
      display: block;
      content: '';
      bottom: 0;
      width: 100%;
      height: 25%;
      background-image: linear-gradient(to bottom, transparent, #cecece);
    }
  }

  &__fusions {
    grid-area: 2/3;
  }

  &__skills {
    grid-area: 3/3;
  }
}
</style>
