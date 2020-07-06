<template>
  <div class="demon-list">
    <div
      sticky
      class="demon-list__settings">
      <button>
        Sort: {{ settings.order }}
        <div>
          <div class="selection no-spacing">
            <template v-for="{ label, value } in orderOptions">
              <input
                v-model="settings.order"
                :key="value"
                :id="`order-${value}`"
                :value="value"
                type="radio"
              />
              <label :key="label" :for="`order-${value}`">
                {{ label }}
              </label>
            </template>
          </div>
          <p class="nowrap">Select an attribute to order by</p>
        </div>
      </button>
      <button @click="settings.desc = !settings.desc">
        {{ settings.desc ? 'asc' : 'desc' }}
      </button>
      <button>
        Name{{ settings.name ? `: ${settings.name}` : '' }}
        <div>
          <input v-model="settings.name"/>
          <p>Search demons by name</p>
        </div>
      </button>
      <button>
        Race{{ settings.race ? `: ${settings.race}` : '' }}
        <div>
          <select v-model="settings.race" style="width: 100%">
            <option value="">All</option>
            <option v-for="option in raceOptions" :key="option">
              {{ option }}
            </option>
          </select>
          <p class="nowrap">Only show demons of selected race</p>
        </div>
      </button>
      <button>
        Max Lvl: {{ settings.max_level }}
        <div>
          <input v-model.number="settings.max_level"
            style="width: 5ch; margin-right: calc(100% - 5ch - 16px)"
            id="max_level" type="number" min="1" max="99" />
          <p class="nowrap">Enter your summon level cap</p>
        </div>
      </button>
      <button
        @click="settings = { ...defaultSettings }"
        style="font-weight: 600;"
      >
        Reset
      </button>
    </div>
    <div class="demon-list__grid no-spacing">
      <DemonCard
        v-for="demon in demons"
        @more-info="(demon) => $emit('more-info', demon)"
        :key="demon.id"
        :demon="demon"
        class="demon-list__grid__card"
      />
    </div>
    <LazyLoader
      :load-more="loadMore"
      ref="lazy-loader"
      class="demon-list__lazy-loader"
    />
  </div>
</template>

<script lang="ts">
import {
  Component, Vue, Watch, Ref,
} from 'vue-property-decorator';
import axios from 'axios';

import DemonCard from '@/components/DemonCard.vue';
import LazyLoader from '@/components/LazyLoader.vue';
import { Demon } from '@/fusion/demons';

@Component({
  components: { DemonCard, LazyLoader },
})
export default class DemonList extends Vue {
  demons: Demon[] = [];

  hasNext = true;

  nextPage = 1;

  defaultSettings = {
    order: 'level',
    desc: false,
    name: '',
    race: '',
    // eslint-disable-next-line @typescript-eslint/camelcase
    max_level: 99,
  }

  settings = { ...this.defaultSettings }

  orderOptions = [
    { label: 'Lvl', value: 'level' },
    { label: 'Hp', value: 'health' },
    { label: 'Mp', value: 'mana' },
    { label: 'St', value: 'strength' },
    { label: 'Dx', value: 'dexterity' },
    { label: 'Ma', value: 'magic' },
    { label: 'Ag', value: 'agility' },
    { label: 'Lu', value: 'luck' },
  ]

  raceOptions = [
    'Herald', 'Megami', 'Avian', 'Tree', 'Divine', 'Flight', 'Yoma',
    'Nymph', 'Vile', 'Raptor', 'Wood', 'Deity', 'Avatar', 'Holy',
    'Genma', 'Fairy', 'Beast', 'Jirae', 'Snake', 'Reaper', 'Wilder',
    'Jaki', 'Vermin', 'Fury', 'Lady', 'Dragon', 'Kishin', 'Fallen',
    'Brute', 'Femme', 'Night', 'Tyrant', 'Drake', 'Spirit', 'Foul',
    'Ghost', 'Fiend', 'Enigma', 'Food', 'Zealot', 'Entity', 'Famed',
    'Amatsu', 'Kunitsu', 'Undead', 'Godly', 'Chaos', 'Element',
  ]

  @Ref('lazy-loader') readonly lazyLoader!: LazyLoader;

  @Watch('settings', { deep: true })
  reset() {
    const data = Object.entries(this.settings).filter(([, value]) => value);
    axios.get(`${this.$api}/demons`, {
      params: { page: 1, ...Object.fromEntries(data) },
    }).then((response) => {
      this.demons = response.data.results;
      this.hasNext = response.data.has_next;
      this.nextPage = 2;
    }).finally(this.lazyLoader.observe);
  }

  resetFilters() {
    this.settings = this.defaultSettings;
  }

  loadMore(el: Element, observer: IntersectionObserver) {
    if (this.hasNext) {
      observer.unobserve(el);
      const data = Object.entries(this.settings).filter(([, value]) => value);

      axios.get(`${this.$api}/demons`, {
        params: { page: this.nextPage, ...Object.fromEntries(data) },
      }).then((response) => {
        this.demons = [...this.demons, ...response.data.results];
        this.hasNext = response.data.has_next;
        this.nextPage += 1;
      }).finally(() => {
        observer.observe(el);
      });
    }
  }
}
</script>

<style lang="scss">
.demon-list {
  position: relative;

  .demon-card img {
    pointer-events: none;
  }

  &__settings {
    display: flex;
    padding: 0.375em 0.375em;
    z-index: 2;
    background-color: white;
    border: 0.065em solid gray;
    border-radius: 0.65em;
    top: 0;

    button {
      margin-top: 0;
      padding: 0.35em 0.85em;
      color: inherit;
      text-decoration: none;
      outline: currentcolor none medium;
      background-color: white;
      cursor: pointer;
      border: 0.065em solid rgb(32, 32, 32);
      border-radius: 0.85em;
      text-transform: capitalize;
      position: relative;

      &:hover, &:focus-within {
        background-color: rgb(237, 237, 237);
      }

      &:focus-within > div {
        display: block;
      }

      & > div {
        position: absolute;
        padding: 1.65em;
        border: 0.15em solid gray;
        border-radius: 0.65em;
        background-color: rgb(237, 237, 237);
        top: calc(100% + 0.85em);
        left: 0;
        z-index: 1;
        display: none;

        .selection {
          display: flex;

          label {
            border: 1px solid gray;
            border-radius: 0.65em;
            padding: 0.35em 1.25em;
            background-color: white;
          }

          input:checked + label {
            background-color: rgb(255, 177, 20);
          }

          input:focus + label {
            outline: dotted 0.065em rgb(32, 32, 32);
            outline-offset: 0.065em;
          }

          label + input {
            margin-left: 1ch;
          }
        }

        input[type=radio] {
          appearance: none;
          border: none;
          outline: none;
        }
      }
    }

    button + button {
      margin-left: 1ch;
    }

    p {
      text-transform: none;
    }
  }

  &__grid {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-around;

    & > .demon-card {
      margin-bottom: 1.65em;
    }

    &__card {
      cursor: grab;
      box-shadow: 0em 2.25em 2em -3em rgba(0, 0, 0, 0.65);
      transform: scale(0.95);
      transition: transform 0.15s ease-in,
                  box-shadow 0.15s ease-in;

      animation: 0.3s ease-out 0s 1 loadcardanim;
      @keyframes loadcardanim {
        0% {
          transform: scale(1);
          box-shadow: 0em 2.25em 2em -2em rgba(0, 0, 0, 0.65);
        }
        100% {
          transform: scale(0.95);
          box-shadow: 0em 2.25em 2em -3em rgba(0, 0, 0, 0.65);
        }
      }
    }

    &__card:hover {
      transform: translateY(-1.5em) scale(1);
      box-shadow: 0em 2.25em 2em -2em rgba(0, 0, 0, 0.65);
    }
  }

  &__lazy-loader {
    height: 50vh;
    width: 100%;
    position: absolute;
    bottom: 0;
  }

  .nowrap {
    white-space: nowrap;
  }
}
</style>
