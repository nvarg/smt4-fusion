<template>
  <div class="demon-info no-spacing">
    <div
      @click.prevent="close"
      class="demon-info__close"
    >
      close
    </div>
    <h2 class="demon-info__title">
      {{ demon.name }}
    </h2>
    <img
      :src="imageUrl"
      draggable="false"
      class="demon-info__image"
    />
    <div class="demon-info__lore">
      <h3>Lore</h3>
      <transition-group appear
        name="demon-info__lore-"
        mode="out-in"
        tag="div"
      >
        <p v-for="loreText in lore" :key="loreText">{{ loreText }}</p>
      </transition-group>
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
    <div class="demon-info__skills">
      <h3>Skills</h3>
        <transition-group appear
          name="demon-info__skills-"
        >
          <SkillInfo
            v-for="skill in innateSkills" :key="skill.name"
            :skill="skill"
          />
        </transition-group>
      <h3>Level Up Skills</h3>
        <transition-group appear
          name="demon-info__skills-"
        >
          <SkillInfo
             v-for="(skill, level) in levelupSkills" :key="skill.name"
            :level="level"
            :skill="skill"
          />
        </transition-group>
      <h3>Fusions</h3>
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

import DemonCard from '@/components/DemonCard.vue';
import Statgram from '@/components/Statgram.vue';
import SkillInfo from '@/components/SkillInfo.vue';

import { Demon, Skill } from '@/smt4';

@Component({
  components: { DemonCard, Statgram, SkillInfo },
})
export default class DemonInfo extends Vue {
  @Prop({ required: true }) demon!: Demon;

  lore: string[] = [];

  loreCancelToken = axios.CancelToken.source();

  innateSkills: Skill[] = []

  levelupSkills: { [level: number]: Skill[] } = {}

  skillsCancelToken = axios.CancelToken.source();

  close() {
    this.$el.classList.add('hidden');
  }

  @Watch('demon')
  updateLoreText() {
    this.lore = [];
    this.loreCancelToken = axios.CancelToken.source();
    axios.get(`${this.$api}/demons/${this.demon.id}/lore`, {
      cancelToken: this.loreCancelToken.token,
    }).then(
      (response) => { this.lore = response.data as string[]; },
    );
  }

  @Watch('demon')
  updateSkillList() {
    this.innateSkills = [];
    this.levelupSkills = {};
    this.skillsCancelToken = axios.CancelToken.source();
    axios.get(`${this.$api}/demons/${this.demon.id}/skills`, {
      cancelToken: this.skillsCancelToken.token,
    }).then(
      (response) => {
        this.innateSkills = response.data.innate;
        this.levelupSkills = response.data.level_up;
      },
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

  animation: modalFadein 0.5s ease-in;
  @keyframes modalFadein {
    from { opacity: 0; }
    to { opacity: 1; }
  }

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

  &__title {
    grid-area: 1/1;
  }

  &__image {
    margin: auto;
    margin-top: auto !important;
    grid-area: 1/1/3/2;

    animation: 0.3s ease-out 0s 1 imageFadeIn;
    @keyframes imageFadeIn {
      0% {
        opacity: 0;
      }
      100% {
        opacity: 1;
      }
    }
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

    &--enter-active {
      transition: opacity 1s ease;
    }

    &--enter {
      opacity: 0;
    }

    &--enter-to {
      opacity: 1;
    }

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
    grid-area: 1/3/4/4;

    &--enter-active {
      transition: all 0.6s ease;
      transform-origin: left;
    }

    &--enter, leave-to {
      transform: scaleX(0%);
      opacity: 0;
    }
  }
}
</style>
