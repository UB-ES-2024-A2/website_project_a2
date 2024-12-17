<template>
  <div class="view-as gradient-custom-header">

     <!-- Filter options -->
      <div class="filter-options-wrap" v-if="token && currentTab !== 'book-page' && currentTab !== 'profile' && currentTab !== 'information'">
        <div class="filter-options" role="toolbar">
          <!-- All filter -->
          <Transition name="slide-up">
            <button id="filterAll" class="filter-btn" v-show="!filterBooks" :class="{'button-selected': filterAll}">All</button>
          </Transition>
          <Transition name="slide-up">
            <button id="undoFilter" class="filter-btn clear-btn" v-show="filterBooks" @click="clearFilter">X</button>

          </Transition>
          <button id="filterBooks" class="filter-btn" :class="{'button-selected': filterBooks}" @click="selectFilter('filterBooks')">Books</button>

          <!-- Genres Selected -->
          <div class="content-selected">
              <div v-for="genre in getGenreViewButtons" :key="genre">
              <button id="genre" class="genres-buttons">
                <span class="genre-icon-content" v-html="getIconByGenre(genre,'#FFFFFF', '#282828')"/>
                <span style="white-space: nowrap"> {{genre}} </span>
                <span class="line"></span>
                <span class="close-icon" @click="deactivateGenre(genre)">
                  <svg width="16" height="16" viewBox="0 0 70 77" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M64.9999 5L35 38.5M35 38.5L5 72M35 38.5L5.00006 5M35 38.5L65 72" stroke="black" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </span>
              </button>
            </div>
          </div>

          <!-- Genre dropdowns -->
          <div class="dropdown" v-show="filterBooks" ref="dropdown">
            <button class="filter-btn" @click="toggleDropdown">Genre</button>
            <div class="dropdown-content" v-show="getDropdownOpen && getGenresList.length > 0">
              <div class="option-dropdown" role="option" v-for="genreItem in getGenresList" :key="genreItem"
                   @click="applyFilterGenre(genreItem)" :class="{'unselected': !getGenreListItem(genreItem)}">
                <span class="icon-content" v-html="getIconByGenre(genreItem,'#282828', '#FFFFFF')"/>
                <span class="text-dropdown">
                  {{ genreItem }}
                </span>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Toogle View: Grid, List and Compact -->
      <div class="toggle-wrap" v-if="currentTab !== 'book-page' && currentTab !== 'profile' && currentTab !== 'information'">
        <input type="radio" id="toggle1" name="toggle" class="toggleCheckbox" @click="setView('grid')" :checked="view === 'grid'"/>
        <input type="radio" id="toggle2" name="toggle" class="toggleCheckbox" @click="setView('list')" :checked="view === 'list'"/>
        <input type="radio" id="toggle3" name="toggle" class="toggleCheckbox" @click="setView('compact')" :checked="view === 'compact'"/>

        <div class="toggleContainer">
          <label for="toggle1" class="toggleLabel">
            <svg width="16" height="16" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <title>Grid View</title>
              <path d="M20 6H6V20H20V6Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M42 6H28V20H42V6Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M42 28H28V42H42V28Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20 28H6V42H20V28Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </label>

          <label for="toggle2" class="toggleLabel">
            <svg width="16" height="16" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <title>List View</title>
              <path d="M38 9.5H24M38 31H24M2 2H16V16H2V2ZM2 24H16V38H2V24Z" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </label>

          <label for="toggle3" class="toggleLabel centered">
            <svg width="16" height="16" viewBox="0 0 40 26" fill="none" xmlns="http://www.w3.org/2000/svg">
              <title>Compact View</title>
              <path d="M28.5 9H2M38 2.5H2M38 24H2M2 17H21" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </label>

          <div class="toggleIndicator gradient-custom"></div>
        </div>

      </div>
    </div>
</template>
<script>

import { genreIcons } from '@/assets/icon.js'

export default {
  name: 'FilterHeader',
  props: {
    searchResults: Array,
    currentTab: String
  },
  data () {
    return {
      filterAll: true,
      filterBooks: false,
      filters: ['filterAll'],
      genresList: {
        'Fiction': true,
        'Classic': true,
        'Romance': true,
        'Adventure': true,
        'Fantasy': true,
        'Horror': true,
        'Epic': true,
        'Science Fiction': true
      },
      dropdownOpen: false

    }
  },
  computed: {
    view () {
      return this.$store.getters.displayMode
    },
    token () {
      return this.$store.getters.token
    },
    getGenreViewButtons () {
      return Object.keys(this.genresList).filter(key => !this.genresList[key])
    },
    getGenresList () {
      return Object.keys(this.genresList)
    },
    getDropdownOpen () {
      return this.dropdownOpen
    }
  },
  methods: {
    setView (display) {
      if (display !== this.view) {
        this.$store.dispatch('setDisplayMode', display)
      }
    },
    initFilter () {
      const filterList = this.filters

      this.filterAll = filterList.includes('filterAll')
      this.filterBooks = filterList.includes('filterBooks')
    },
    selectFilter (filterId) {
      const filter = document.getElementById(filterId)
      let filterList = [...this.filters]

      if (this.hasOwnProperty(filterId)) {
        this[filterId] = !this[filterId]
      }

      if (!filter.classList.contains('button-selected')) {
        filter.classList.add('button-selected')
        if (!filterList.includes(filterId)) {
          filterList.push(filterId)
        }
      } else {
        filter.classList.remove('button-selected')
        filterList = filterList.filter(item => item !== filterId)
      }

      this.filters = filterList
      this.$emit('filter-changed', {filters: this.filters})
    },
    clearFilter () {
      this.filterAll = true
      this.filterBooks = false

      this.filters = ['filterAll']
      Object.keys(this.genresList).forEach((genre) => {
        this.genresList[genre] = true
      })
      this.$emit('genres-updated', [...this.getGenreViewButtons])
      this.$emit('filter-changed', {filters: this.filters})
    },
    applyFilterGenre (genre) {
      this.genresList[genre] = !this.genresList[genre]
      this.$emit('genres-updated', [...this.getGenreViewButtons])
    },

    deactivateGenre (genre) {
      if (!this.genresList[genre]) {
        this.genresList[genre] = true
        this.$emit('genres-updated', [...this.getGenreViewButtons])
      }
    },
    getIconByGenre (genre, color1, color2) {
      if (genreIcons[genre]) {
        return genreIcons[genre](color1, color2)
      } else {
        console.error(`Icon for genre "${genre}" not found`)
        return ''
      }
    },
    toggleDropdown () {
      this.dropdownOpen = !this.dropdownOpen
    },
    closeDropdown (event) {
      const dropdown = this.$refs.dropdown
      if (dropdown && !dropdown.contains(event.target)) {
        this.dropdownOpen = false
      }
    },
    getGenreListItem (genre) {
      return this.genresList[genre]
    }
  },
  mounted () {
    document.addEventListener('click', this.closeDropdown)
  },
  beforeDestroy () {
    document.removeEventListener('click', this.closeDropdown)
  }
}
</script>
<style scoped>
.filter-options-wrap {
  display: flex;
  align-items: center;
  flex-grow: 1;
  padding: calc(var(--panel-gap) / 2);
}

.filter-options {
  display: flex;
  gap: 1rem;
  grid-template-columns: repeat(3, 1fr);
  font-size: var(--font-size-xs);
}

.content-selected{
  display: flex;
  flex-direction: row;
  gap: var(--panel-gap);
  overflow-x: auto;
  max-width: 10rem;
}

.filter-btn {
  color: var(--text-color);
  border-radius: calc(var(--border-radius) * 3);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: 0;
  background-color: var(--half-transparent-background);
}

.clear-btn{
  border-radius: calc(var(--border-radius) * 9);
}

.button-selected{
  font-weight: 600;
  color: var(--reverse-text-color);
  background-color: var(--reverse-background);
}

.filter-btn:hover {
  background-color: var(--half-transparent-background);
  color: var(--text-color);
}

/* Dropdown styling */
.dropdown {
  position: relative;
}

.dropdown-content {
  position: absolute;
  background-color: var(--box-background-color);
  border: 1px solid var(--half-transparent-background);
  border-radius: calc(var(--border-radius) * 2);
  z-index: 4;
  overflow-y: auto;
  height: auto;
  max-height: 20rem;
  width: 100%;
  min-width: 13rem;
  margin-top: 0.5rem;
  padding: calc(var(--panel-gap)* 2);
  padding-inline: calc(var(--panel-gap)* 2);
}

.unselected{
  background: var(--half-transparent-background-purple);
}

.unselected:hover{
  background: var(--half-transparent-background-purple) !important;
}

.option-dropdown{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: var(--border-radius);
  list-style: none;
}

.icon-content{
  align-self: start;
}

.text-dropdown{
  text-align: right;
}

.option-dropdown:hover {
  background: var(--half-transparent-background);
}

.view-as{
  grid-area: filter-option;
  display: flex;
  flex-direction: row;
  position: sticky;
  top: 0;
  opacity: 1;
  justify-content:flex-start;
  padding: calc(var(--panel-gap)*2);
  align-items: center;
  height: 5rem;
}

.toggle-wrap {
    display: flex;
    align-items: center;
    margin-left: auto;
    padding: calc(var(--panel-gap) / 2);
}

.toggleContainer {
    position: relative;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid var(--box-border-color);
    border-radius: calc(var(--border-radius) * 2);
    background: var(--box-background-color);
    font-weight: bold;
    overflow: hidden;
    align-items: center;
}

.toggleLabel {
    padding: 10px;
    text-align: center;
    cursor: pointer;
    color: var(--text-color);
    font-size: var(--font-size-xs);
    z-index: 1;
    transition: color 0.3s;
    display: flex;
}

.toggleIndicator {
    content: '';
    position: absolute;
    width: 29.33%;
    height: 90%;
    left: 0;
    border-radius: calc(var(--border-radius) * 2);
    transition: all 0.3s;
}

.genres-buttons{
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: calc(var(--border-radius) * 3);
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 600;
  color: var(--reverse-text-color);
  background-color: var(--reverse-background);
  border: 0;
}

.genre-icon-content{
  margin-right: 0.5rem;
}

.line{
  height: 1.5rem;
  width: 0.1rem;
  background-color: var(--box-background-color);
  margin: 0 0.5rem;
}

.close-icon{
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggleCheckbox {
    display: none;
}

#toggle1:checked ~ .toggleContainer  .toggleIndicator {
    left: 2%;
}

#toggle2:checked ~ .toggleContainer .toggleIndicator {
    left: 35.33%;
}

#toggle3:checked ~ .toggleContainer .toggleIndicator {
    left: 68.66%;
}

/* Transition when the element enters */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.25s ease-out;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

</style>
