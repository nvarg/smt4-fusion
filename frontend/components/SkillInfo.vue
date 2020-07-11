<template>
  <div
    class="skill-info"
    tabindex="-1"
  >
    <div class="skill-info__header no-spacing">
      <img
        :src="`${this.$api}/images/icons/${skill.type}?crop=false&background_color=%23ffb114`"
      />
      <span v-if="level">
        <span
          style="font-size: 0.75em;"
        >
          Lv.
        </span>{{ level }}:
      </span>
      {{ skill.name }}
    </div>
    <div
      class="skill-info__body"
    >
      <div
        v-if="skill.damage || skill.target"
        class="skill-info__body__top no-spacing"
      >
        <div v-if="skill.damage">{{ skill.damage }} Damage</div>
        <div v-if="skill.target">Targets {{ skill.target }}</div>
      </div>
      <div v-if="skill.effect">
        {{ skill.effect }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Skill } from '@/smt4';

@Component
export default class SkillInfo extends Vue {
  @Prop({ required: true }) skill!: Skill;

  @Prop() level!: number;
}
</script>

<style lang="scss">
.skill-info {
  cursor: pointer;
  border: 0.065em solid rgba(0, 0, 0, 0.2);
  padding: 0.35em 0.65em;
  border-radius: 0.25em;
  background-color: rgba(20, 20, 20, 0.1);
  font-size: 0.9rem;

  &__header {
    font-weight: bold;
  }

  &__body {
    display: none;
    overflow-y: hidden;

    animation: dropdown 1s;
    @keyframes dropdown {
      from { max-height: 0; }
      to { max-height: 25ch; }
    }

    &__top {
      display: flex;

      & > div {
        flex-basis: 50%;
        flex-grow: 1;
      }
    }
  }

  &:focus-within &__body,
  &:hover &__body {
    display: block;
  }
}
</style>
