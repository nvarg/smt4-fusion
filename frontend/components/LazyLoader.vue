<template>
  <div class="lazy-loader"></div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class LazyLoader extends Vue {
  @Prop({ required: true }) loadMore!: (el: Element, observer: IntersectionObserver) => void;

  @Prop() root: Element | undefined;

  @Prop({ default: 0 }) threshold!: number;

  observer = new IntersectionObserver(this.handleObserver, {
    root: this.root,
    threshold: this.threshold,
  });

  handleObserver(entries: IntersectionObserverEntry[]) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        this.loadMore(this.$el, this.observer);
      }
    });
  }

  observe() {
    this.observer.observe(this.$el);
  }

  unobserve() {
    this.observer.unobserve(this.$el);
  }

  mounted() {
    this.observer.observe(this.$el);
  }
}
</script>

<style lang="scss">
.lazy-loader {
  height: 1px;
  z-index: -100;
}
</style>
