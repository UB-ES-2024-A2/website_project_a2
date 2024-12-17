<template>
  <ul class="suggestions-list" role="listbox" aria-label="Suggestions">
          <!-- Suggestions Group -->
          <li class="suggestions-entire-list" role="presentation" v-if="suggestions.length">
            <h3 class="suggestion-title">
              {{ title }}
            </h3>
            <ul role="presentation">
                <li class="option" role="option"
                    v-for="suggestion in suggestions"
                    :key="suggestion.name"
                    :class="{ 'disabled-option': !selectSuggestionAvailable }">

                  <div v-if="selectSuggestionAvailable">
                    <router-link
                     :to="computedHref(suggestion)"
                     class="option-link">

                    <span class="icon-container" v-html="icon"/>

                    <span class="grid-label-wrap">
                      <span class="label-wrap">
                        <span>
                          {{ suggestion.name }}
                        </span>
                      </span>
                    </span>

                    <span class="final-label" v-if="selectSuggestionAvailable">
                      Jump to
                    </span>
                  </router-link>
                  </div>

                  <div v-else
                       class="option-link"
                       :class="{ 'disabled-option': !selectSuggestionAvailable }">
                    <span class="icon-container" v-html="icon"/>

                    <span class="grid-label-wrap">
                      <span class="label-wrap">
                        <span>
                          {{ suggestion.name }}
                        </span>
                      </span>
                    </span>

                    <span class="final-label" v-if="selectSuggestionAvailable">
                      Jump to
                    </span>
                  </div>

                </li>

            </ul>
          </li>

          <!-- Line Suggestions -->
          <li class="line-suggestions" v-if="isNext"/>

  </ul>
</template>

<script>
import { encode } from '../../utils/encoding.js'

export default {
  name: 'Suggestion',
  props: {
    suggestions: Array,
    title: String,
    icon: String,
    isNext: Boolean,
    selectSuggestionAvailable: Boolean
  },
  data () {
    return {}
  },
  methods: {
    computedHref (suggestion) {
      const newQuery = {
        search: suggestion.name,
        type: suggestion.type,
        id: suggestion.id
      }
      // Convertir el objeto a una cadena de consulta
      const queryString = new URLSearchParams(newQuery).toString()

      // Codificar la cadena de consulta
      const encodedQuery = encode(queryString)

      // Retornar la URL codificada
      return `${this.$route.path}?q=${encodedQuery}`
    }
  }
}
</script>

<style scoped>
.suggestions ul {
  list-style-type: none;
  padding: 0;
}

.suggestions-list{
  padding: var(--panel-gap);
  overflow-x: hidden;
  overflow-y: auto;
  list-style: none;
  margin-top: 0;
  margin-bottom: 0;
  box-sizing: border-box;
}

.suggestions-entire-list{
  display: flex;
  font-weight: 600;
  color: var(--text-color);
  flex-direction: column;
  padding-block: 0.375rem;
  padding-inline: var(--panel-gap);
  padding-bottom: calc(0.375rem + var(--panel-gap));
}

.suggestion-title{
  font-size: var(--font-size-xs);
  font-weight: 600;
  align-self: flex-start;
  text-align: left;
  padding: var(--panel-gap);
  margin-block-start: 1em;
  margin-block-end: 1em;
}

.option{
  margin-right: var(--panel-gap);
  margin-left: var(--panel-gap);
  border-radius: var(--border-radius);
  list-style: none;
}

.option-link{
  text-decoration: none;
  display: grid;
  grid-template: 'leadingIcon label lastLabel';
  border-radius: var(--border-radius);
  padding-block: var(--border-radius);
  padding-inline: var(--panel-gap);
  width: 100%;
  align-items: start;
}

.icon-container{
  display: flex;
  margin-right: var(--panel-gap);
  align-items: center;
  min-height: 1.25rem;
  grid-area: leadingIcon;
}

.grid-label-wrap{
  margin-right: var(--panel-gap);
  display: flex;
  flex-direction: column;
  gap: calc(var(--panel-gap) /2);
  grid-area: label;
  align-items: start;
}

.label-wrap{
  color: var(--text-color);
  font-size: var(--font-size-xs);
  grid-area: label;
  line-height: 1.4285;
}

.final-label{
  display: flex;
  font-size: var(--font-size-xs);
  grid-area: lastLabel;
  color: var(--text-color-secundary);
  line-height: 1.6666;
  justify-content: end;
}

.line-suggestions{
  height: 1px;
  margin: var(--panel-gap) calc(var(--panel-gap)* 2) var(--panel-gap);
  background: var(--gray-background);
  box-sizing: border-box;
}

.suggestions li {
  cursor: pointer;
}

.disabled-option {
  cursor: default;
}

.option:hover {
  background: var(--half-transparent-background);
}

.option:active {
  background-color: var(--half-transparent-background);
}

.disabled-option:hover,
.disabled-option:active {
  background: none;
  color: inherit;
}

</style>
