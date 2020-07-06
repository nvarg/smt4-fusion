<template>
  <svg
    :viewBox='`-${size/2} -${size/2} ${size} ${size}`'
    class='statgram'
  >
    <line
      v-for='(point, idx) in equallySpacedPoints(this.size / 2)'
      :key='`axis-${idx}`'
      x1='0' y1='0'
      :x2='point.x' :y2='point.y'
      class='statgram__axis'
    />

    <polygon class='statgram__grid'
      v-for="idx in Array(nticks).keys()" :key='`grid-${idx}`'
      :points='svgPointString(equallySpacedPoints((idx + 1) * size / nticks / 2 - 10))'
    />

    <polygon
      :points='svgPointString(points)'
      :fill="fill"
      :stroke="stroke"
      class='statgram__gon'
    />

    <text
      v-for="(point, idx) in equallySpacedPoints(size * 1.05 / 2)"
      :key='labels[idx]'
      :x="point.x"
      :y="point.y"
      class='statgram__spoketext'
    >
      {{ labels[idx] }}
    </text>

    <text
      v-for='(point, idx) in tooltipPoints'
      :key='`tooltip-${idx}`'
      :x='point.x' :y='point.y'
      class='statgram__tooltip__text'
    >
      {{ stats[idx] }}
    </text>
  </svg>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class Statgram extends Vue {
  @Prop({ default: 500 }) readonly size!: number;

  @Prop({ required: true }) readonly stats!: number[];

  @Prop({ required: true }) readonly labels!: string[];

  @Prop({ required: true }) readonly max!: number[];

  @Prop({ default: 3 }) readonly nticks!: number;

  @Prop({ default: 'rgba(70, 130, 180, 0.65)' }) readonly fill!: string;

  @Prop({ default: 'rgba(0, 0, 0, 0)' }) readonly stroke!: string;

  created() {
    if (this.labels.length !== this.stats.length
      || this.max.length !== this.stats.length) {
      console.error(
        'Statgram labels, stats, and max length don\'t match!',
        this.stats,
        this.labels,
        this.max,
      );
    }
  }

  equallySpacedPoints(lengths: number | number[]): { x: number; y: number }[] {
    return Array.from({ length: this.stats.length }, (_, idx) => {
      const theta = (2 * Math.PI * idx) / this.stats.length - Math.PI / 2;
      return {
        x: (typeof lengths === 'number' ? lengths : lengths[idx]) * Math.cos(theta),
        y: (typeof lengths === 'number' ? lengths : lengths[idx]) * Math.sin(theta),
      };
    });
  }

  get points() {
    return this.equallySpacedPoints(
      this.stats.map((stat, idx) => (stat * this.size * 0.95) / this.max[idx] / 2),
    );
  }

  get tooltipPoints() {
    return this.equallySpacedPoints(
      this.stats.map((stat, idx) => (stat * this.size) / this.max[idx] / 2),
    );
  }

  // eslint-disable-next-line class-methods-use-this
  svgPointString(points: { x: number; y: number }[]): string {
    return points.map(({ x, y }) => `${x} ${y}`).join(', ');
  }
}
</script>

<style lang="scss">
.statgram {
  overflow: visible;
  background-color: none;
  max-width: 100%;

  text {
    pointer-events: none;
    text-anchor: middle;
    text-shadow: -0.5px 0.5px 0 #fff,
                 0.5px 0.5px 0 #fff,
                 0.5px -0.5px 0 #fff,
                 -0.5px -0.5px 0 #fff;
  }

  &__axis {
    stroke: currentColor;
    stroke-width: 2.5;
    stroke-linecap: round;
  }

  &__grid {
    fill: none;
    stroke: currentColor;
    stroke-width: 1.75;
  }

  &__gon {
    stroke-width: 2.5;
    stroke-join: round;
  }

  &__tooltip {
    &__collision {
        opacity: 0;
    }

    &__text {
      font-size: 1.5rem;
      transition: opacity 250ms ease-in;
      opacity: 0;

    }
  }

  &:hover &__tooltip__text {
    opacity: 1;
  }

  &__spoketext {
    font-size: 1.5rem;
  }
}
</style>
