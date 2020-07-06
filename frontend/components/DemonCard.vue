<template>
  <div
    draggable
    @dragstart="dragStart"
    @dragend="dragEnd"
    class="demon-card">
    <div class="demon-card__headline">
      <div class="demon-card__headline__level">
        <span style="font-size: 0.75em">Lv.</span>{{ demon.level }}
      </div>
      <div class="demon-card__headline__name no-spacing">
        {{ demon.name }}
      </div>
      <div class="demon-card__headline__race">
        {{ demon.race }}
      </div>
      <div class="demon-card__headline__info" @click="$emit('more-info', demon)">&#9432;</div>
    </div>
    <img
      class="demon-card__image"
      :src="imageUrl"
    />
    <div class="demon-card__stats">
      <div
        v-for="resistance, idx of demon.resistances"
        :key="idx"
        class="demon-card__stats__stat demon-card__stats__stat--resistance"
      >
        <img class="element-icon" :src="`icons/elements/${idx}.png`" />
        <div
          :class="`resistance-${resist[resistance]}`"
        >
          {{ resist[resistance] }}
        </div>
      </div>
    </div>
    <div class="demon-card__stats">
      <div class="demon-card__stats__stat">
        <div>Hp</div>
        <hr />
        <div>{{ demon.health }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>Mp</div>
        <hr />
        <div>{{ demon.mana }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>St</div>
        <hr />
        <div>{{ demon.strength }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>Dx</div>
        <hr />
        <div>{{ demon.dexterity }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>Ma</div>
        <hr />
        <div>{{ demon.magic }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>Ag</div>
        <hr />
        <div>{{ demon.agility }}</div>
      </div>
      <div class="demon-card__stats__stat">
        <div>Lu</div>
        <hr />
        <div>{{ demon.luck }}</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Demon } from '@/fusion/demons';

@Component
export default class DemonCard extends Vue {
  @Prop({ required: true }) readonly demon!: Demon;

  resist = {
    '-': '–',
    s: 'Rs',
    w: 'Wk',
    r: 'Rp',
    n: 'Nu',
    d: 'Dr',
  }

  get paddedID() {
    return String(this.demon.id).padStart(3, '0');
  }

  get imageUrl() {
    return `${this.$api}/images/devbu/devbu${this.paddedID}`
      + '?max_width=232&max_height=250&background_color=%23ececec';
  }

  dragStart(event: DragEvent) {
    if (event.dataTransfer) {
      event.dataTransfer.setData('application/json', JSON.stringify(this.demon));
      event.dataTransfer.setDragImage(this.$el,
        this.$el.clientWidth / 2, this.$el.clientHeight / 2);
    }
    this.$el.classList.add('held');
  }

  dragEnd() {
    this.$el.classList.remove('held');
  }
}
</script>

<style lang="scss">
.demon-card {
  display: flex;
  flex-direction: column;
  padding: 0.65em;
  border: 0.15em rgb(128, 128, 128) solid;
  border-radius: 0.65em;
  background-color: #ececec;
  font-size: 0.8rem;
  margin-bottom: 1em;

  &.held {
    transform: scale(0.95) !important;
    filter: brightness(0.9);
    outline: 0.25em sandybrown dotted;
    outline-offset: 0.15em;
  }

  &__image {
    width: 100%;
    max-width: 232px;
    height: 250px;
    object-fit: contain;
  }

  &__headline {
    display: grid;
    grid-template-columns: min-content auto;

    & > * {
      margin: 0;
    }

    &__level {
      grid-area: 1/1;
      padding-right: 0.5ch;
      font-weight: 700;
    }

    &__name {
      font-weight: 700;
      grid-area: 1/2;
    }

    &__race {
      font-size: 0.75em;
      grid-area: 2/1/3/3;
      text-transform: uppercase;
    }

    &__info {
      display: none;
      position: absolute;
      right: 0.5ch;
      top: 0;
      font-size: 2rem;
      color: darkcyan;
      font-weight: bold;
      font-style: italic;
      cursor: pointer;
    }
  }

  &:hover .demon-card__headline__info {
    display: block;
  }

  &__stats {
    display: flex;
    justify-content: space-between;

    & > *,
    &__stat > * {
      margin: 0;
    }

    &__stat {
      border: 0.065em rgb(128, 128, 128) solid;
      border-radius: 0.5em;
      width: 3.65ch;
      overflow: hidden;

      & + & {
        margin-left: 0.15em;
      }

      div:first-child {
        font-weight: 600;
        background-color: rgb(255, 177, 20);;
        overflow: hidden;
      }

      div {
        padding: 0.25em;
        padding-bottom: 0em;
        text-align: right;
      }

      &--resistance {
        width: 3.125ch;
        background-color: rgb(255, 177, 20);;
        padding: 0.125em;

        .element-icon {
          display: block;
          margin: auto;
          width: 0.85em;
        }

        & div {
          text-align: center;
          font-size: 0.85em;
        }

        .resistance-–{
          color: black;
        }

        .resistance-Wk {
          color: red;
        }

        .resistance-Nu {
          color: gray;
        }

        .resistance-Rp {
          color: purple;
        }

        .resistance-Rs {
          color: blue;
        }

        .resistance-Dr {
          color: green;
        }
      }
    }
  }
}
</style>
