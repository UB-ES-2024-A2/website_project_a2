<template>
  <div id="leftcol" class="left-slider">
    <div class="library-content-wrap">
      <nav class="library-content">
        <header class="library-header btn" @click="setSize">
          <div class="library-info">
            <div class="library-icon">
            <svg width="40" height="40" viewBox="0 0 47 28" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 19L20 19.3333L14 26V4.66667C14 3.95943 14.1806 3.28115 14.5021 2.78105C14.8236 2.28096
              15.2596 2 15.7143 2L18.3593 2C18.8139 2 19.2499 2.28095 19.5714 2.78105C19.8929 3.28115 20 4.29276 20 5V19Z"
                    fill="#535151" stroke="#535151" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 19L7.99998 19.3333L2 26V4.66667C2 3.95943 2.18061 3.28115 2.5021 2.78105C2.82359 2.28096 3.25962
              2 3.71428 2L6.35925 2C6.81391 2 7.24994 2.28095 7.57143 2.78105C7.89292 3.28115 8 4.29276 8 5V19Z"
                    fill="#535151" stroke="#535151" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M45 25L35.5 18.6111L26 25V4.55556C26 3.87778 26.286 3.22776 26.795 2.7485C27.304 2.26925 27.9944 2
              28.7143 2H42.2857C43.0056 2 43.696 2.26925 44.205 2.7485C44.714 3.22776 45 3.87778 45 4.55556V25Z"
                    fill="#535151" stroke="#535151" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="library-title-header">
            Your library
          </div>
          </div>
        </header>

        <div class="my-books-wrap">
          <div class="filter-header-my-books" v-show="getOriginalMyBooksList.length !== 0">
            <div class="search-my-books"  ref="inputSearchMyBook">
              <div class="search-my-books-icon" @click="setIsVisible">
                <div class="tooltip-container" style="padding-inline: var(--panel-gap);">
                  <span class="tooltip-text">Search</span>
                  <svg style="display: block; padding-inline: var(--panel-gap)" width="35" height="35" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M38 38L29.3 29.3M34 18C34 26.8366 26.8366 34 18 34C9.16344 34 2 26.8366 2 18C2 9.16344 9.16344 2 18 2C26.8366 2 34 9.16344 34 18Z" stroke="#919090" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <transition name="fade">
                <div v-show="getIsVisible" class="input-my-book-wrap">
                  <input
                    type="search"
                    spellcheck="false"
                    maxlength="200"
                    placeholder="Search in Your Library"
                    v-model="searchQuery"
                    class="search-input"
                    :class="{active: isLoading}"
                  />
                </div>
              </transition>
            </div>
            <div class="tooltip-container">
                <span class="tooltip-text">Sort</span>
                <div class="btn" ref="dropdownFilter">
                  <svg v-show="getCurrentIcon === 'alphabetical'" @click="toggleIconDropDown" width="20" height="13" viewBox="0 0 20 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.4415 1.62732H19M10.4415 6.4421H16.5547M10.4415 11.2569H14.1094M1.5 11.2569L2.32 9M7 11.2569L6.31667 9M2.32 9L4.5 3L6.31667 9M2.32 9H6.31667" stroke="#919090" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-show="getCurrentIcon === 'popular'" @click="toggleIconDropDown" width="20" height="13" viewBox="0 0 21 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.9415 0.999924H19.5M10.9415 5.8147H17.0547M10.9415 10.6295H14.6094M5 4.94413L2.5 10.6295L8.5 7.12948H1.5L7.5 10.6295L5 4.94413Z" stroke="#919090" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>

                  <!-- Dropdown Sort -->
                  <transition name="slide-fade-vertical">
                    <div class="dropdown-content-filter" v-show="getIconDropDown">
                      <div class="option-dropdown-filter" role="option"
                           :class="{'unselected': getCurrentIcon === 'alphabetical'}"
                            @click="setAlphabeticalSort">
                        <span class="icon-content-filter">
                          <svg width="20" height="13" viewBox="0 0 20 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10.4415 1.62732H19M10.4415 6.4421H16.5547M10.4415 11.2569H14.1094M1.5 11.2569L2.32 9M7 11.2569L6.31667 9M2.32 9L4.5 3L6.31667 9M2.32 9H6.31667" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          </svg>
                        </span>
                        <span class="text-dropdown-filter">
                          Alphabetical
                        </span>
                      </div>

                      <div class="option-dropdown-filter" role="option"
                           :class="{'unselected': getCurrentIcon === 'popular'}"
                            @click="setPopularSort">
                        <span class="icon-content-filter">
                          <svg width="20" height="13" viewBox="0 0 21 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M10.9415 0.999924H19.5M10.9415 5.8147H17.0547M10.9415 10.6295H14.6094M5 4.94413L2.5 10.6295L8.5 7.12948H1.5L7.5 10.6295L5 4.94413Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          </svg>
                        </span>
                        <span class="text-dropdown-filter">
                          Popular
                        </span>
                      </div>
                    </div>
                    </transition>

              </div>
            </div>
          </div>

          <!-- Show the loader animation of the My Books -->
          <Transition name="slide-fade" mode="out-in">
            <div v-if="getLoadingMyBooks" class="my-books-content">
              <place-holder :items="10"/>
            </div>
          </Transition>

          <Transition name="slide-fade" mode="out-in">
            <div v-if="getFilteredMyBooksList.length" class="my-books-content">
                <grid :column="getFilteredMyBooksList"/>
            </div>
            <div v-else-if="!getLoadingMyBooks && !specialCharacters" class="no-books-message">
                No books found in Your Library.
            </div>
          </Transition>
          <div v-show="specialCharacters" class="no-books-message">
              No special characters allowed
          </div>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import GridLibrary from '@/components/GridLibrary'
import GridPlaceHolderMyBooks from '@/components/GridPlaceHolderMyBooks'
import debounce from 'lodash/debounce'

const IconEnum = Object.freeze({
  ALPHABETICAL: 'alphabetical',
  POPULAR: 'popular'
})
export default {
  name: 'Library',
  props: {
    myBooksList: Array,
    loadingMyBooks: Boolean
  },
  watch: {
    searchQuery () {
      this.isLoading = true
      this.debouncedFilter()
    },
    myBooksList: {
      handler () {
        this.originalMyBooksList = [...this.myBooksList]
        this.filteredMyBooksList = [...this.myBooksList]
        this.filterSuggestions()
      },
      immediate: true
    }
  },
  data () {
    return {
      isLoading: false,
      isVisible: false,
      searchQuery: '',
      currentIcon: IconEnum.ALPHABETICAL,
      iconDropDown: false,
      originalMyBooksList: [],
      filteredMyBooksList: [],
      specialCharacters: false
    }
  },
  components: {
    'grid': GridLibrary,
    'place-holder': GridPlaceHolderMyBooks
  },
  computed: {
    getCurrentIcon () {
      return this.currentIcon
    },
    getIconDropDown () {
      return this.iconDropDown
    },
    getIsVisible () {
      return this.isVisible
    },
    getLoadingMyBooks () {
      return this.loadingMyBooks
    },
    getFilteredMyBooksList () {
      return this.filteredMyBooksList
    },
    getOriginalMyBooksList () {
      return this.originalMyBooksList
    }
  },
  methods: {
    setIsVisible () {
      this.isVisible = !this.isVisible
    },
    toggleIconDropDown () {
      this.iconDropDown = !this.iconDropDown
    },
    closeSearch () {
      const searchInput = this.$refs.inputSearchMyBook
      const dropdown = this.$refs.dropdownFilter

      // Cierra el input de búsqueda si se hace clic fuera de él
      if (searchInput && !searchInput.contains(event.target) && dropdown && !dropdown.contains(event.target)) {
        this.searchQuery = ''
        this.isVisible = false
      }

      // Cierra el desplegable si se hace clic fuera de él
      if (dropdown && !dropdown.contains(event.target)) {
        this.iconDropDown = false
      }
    },
    setAlphabeticalSort () {
      this.iconDropDown = false
      if (this.currentIcon === IconEnum.ALPHABETICAL) return
      this.currentIcon = IconEnum.ALPHABETICAL
      this.filterSuggestions()
    },
    setPopularSort () {
      this.iconDropDown = false
      if (this.currentIcon === IconEnum.POPULAR) return
      this.currentIcon = IconEnum.POPULAR
      this.filterSuggestions()
    },
    setSize () {
      this.searchQuery = ''
      this.$emit('set-size')
    },
    filterSuggestions () {
      if (this.specialCharacters) this.specialCharacters = false
      if (this.searchQuery.trim() === '') {
        this.filteredMyBooksList = this.originalMyBooksList
      } else {
        if (this.hasSpecialCharacters(this.searchQuery.trim())) {
          this.filteredMyBooksList = []
          this.specialCharacters = true
          this.isLoading = false
          return
        }
        this.filteredMyBooksList = this.originalMyBooksList.filter(book =>
          book.data.title.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      }

      // Aplica la ordenación en base al currentIcon
      if (this.currentIcon === IconEnum.ALPHABETICAL) {
        this.filteredMyBooksList.sort((a, b) =>
          a.data.title.localeCompare(b.data.title)
        )
      } else if (this.currentIcon === IconEnum.POPULAR) {
        this.filteredMyBooksList.sort((a, b) => b.data.rating - a.data.rating)
      }
      this.isLoading = false
    },
    hasSpecialCharacters (input) {
      const specialCharactersRegex = /^[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ0-9]+( +[a-zA-ZñÑáéíóúÁÉÍÓÚüçÜ0-9]+)*$/
      return !specialCharactersRegex.test(input)
    }
  },
  created () {
    this.debouncedFilter = debounce(this.filterSuggestions, 1000)
  },
  mounted () {
    document.addEventListener('click', this.closeSearch)
  },
  beforeDestroy () {
    document.removeEventListener('click', this.closeSearch)
  }
}
</script>

<style scoped>
.left-slider {
  background: var(--box-background-color);
  overflow: auto;
  grid-area: left-slider;
  margin-right: calc(-1 * var(--panel-gap));
  border: 1px solid var(--box-border-color);
  border-radius: calc(var(--border-radius) *2);
  display: flex;
  gap: var(--panel-gap);
  flex-direction: column;
  container-type: inline-size;
}

.library-content-wrap {
  display: flex;
  gap: var(--panel-gap);
  padding: var(--panel-gap);
  height: 100vh;
}

.library-content {
  display: grid;
  gap: var(--panel-gap);
  grid-template-areas: 'nav-control'
                       'library-content';
  grid-template-rows: 1fr auto;
  width: 100%;
}

.my-books-wrap{
  padding-inline: calc(var(--panel-gap));
  gap: var(--panel-gap);
  display: grid;
  grid-area: library-content;
  overscroll-behavior-y: contain;
  overflow-x: hidden;
  grid-template-areas: 'filter-header-my-books'
                       'my-books-content';
  grid-template-rows: calc(var(--panel-gap) *7) auto;
  height: 100vh;
}

.library-header {
  padding-inline: calc(var(--panel-gap) *3);
  gap: var(--panel-gap);
  grid-area: nav-control;
  display: flex;
  justify-content: space-between;
  align-items: center;
  justify-items: center;
  border: 0;
}

.library-info{
  display: flex;
  align-items: center;
  gap: var(--panel-gap);
}

.library-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.library-title-header {
  font-size: 1rem;
  color: var(--title-header-library);
  font-weight: bold;
  text-align: center;
}

.filter-header-my-books {
  grid-area: filter-header-my-books;
  display: flex;
  justify-content: space-between;
  align-items: center;
  justify-items: center;
}

.search-my-books{
  transition: all .22s ease-in;
  width: 100%;
  padding-inline: var(--panel-gap);
  position: relative;
  border-radius: 500px;
}

.search-my-books-icon{
  display: flex;
  left: 0.25rem;
  right: auto;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.input-my-book-wrap{
  border: 0;
  margin: 0;
  padding: 0;
  vertical-align: baseline;
}

.search-input {
  display: flex;
  left: 0;
  padding-block: calc(var(--panel-gap));
  padding-left: calc(var(--panel-gap) * 5);
  background: transparent;
  border-radius: calc(var(--border-radius) * 100);
  cursor: pointer;
  border: 0.125rem solid transparent;
  color: var(--text-color);
  outline: none;
}

.search-input.active{
  --border-angle: 0turn;
  --main-bg: conic-gradient(
    from var(--border-angle),
    var(--button-background),
    var(--button-background) 5%,
    var(--button-background) 60%,
    var(--button-background) 95%
  );
  --gradient-border: conic-gradient(
    from var(--border-angle),
    transparent 25%,
    var(--text-color),
    var(--purple-background) 99%,
    transparent
  );
  background: var(--main-bg) padding-box,
  var(--gradient-border) border-box,
  var(--main-bg) border-box;

  animation: bg-spin 3s linear infinite;
  transition: box-shadow 0.3s ease;
}

.search-input::-webkit-search-cancel-button {
  -webkit-appearance: none;
  appearance: none;
}

.search-input:focus {
  border-color: var(--text-color);
}

.search-input.active:focus {
  border-color: transparent;
}

.search-my-books:hover {
  box-shadow: inset 0 0 0.25rem var(--search-color-shadow);
}

.my-books-content {
  grid-area: my-books-content;
}

.dropdown-content-filter {
  position: absolute;
  background-color: var(--dropdown-backgroudn-color);
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
  right: 0;
  color: var(--text-color);
}

.unselected{
  background: var(--half-transparent-background-purple);
}

.unselected:hover{
  background: var(--half-transparent-background-purple) !important;
}

.option-dropdown-filter{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: var(--border-radius);
  list-style: none;
}

.icon-content-filter{
  align-self: start;
}

.text-dropdown-filter{
  text-align: right;
}

.option-dropdown-filter:hover {
  background: var(--half-transparent-background);
}

.no-books-message {
  text-align: center;
  font-size: 1rem;
  color: var(--title-header-library);
  font-weight: bold;
  padding: var(--panel-gap);
  font-style: italic;
}

@container (max-width: 19rem) {
  .library-title-header {
    display: none !important;
  }

  .my-books-wrap{
    padding-inline: 0 !important;
    grid-template-areas: 'my-books-content' !important;
    grid-template-rows: auto !important;
  }

  .filter-header-my-books {
    display: none !important;
  }
}

@media (max-width: 42.375rem) {
  .left-slider {
    margin: var(--panel-gap);
  }

  .library-title-header, .library-header, .filter-header-my-books{
    display: none !important;
  }
.my-books-wrap {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: var(--panel-gap);
    overflow-y: hidden;
    overflow-x: auto;
    height: auto;
  }

  .my-books-content {
    flex: 1;
    display: block;
    white-space: nowrap;
    overflow-x: auto;
  }
}

@keyframes bg-spin {
  to {
    --border-angle: 1turn;
  }
}

@property --border-angle {
  syntax: "<angle>";
  inherits: true;
  initial-value: 0turn;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-fade-vertical-enter-active, .slide-fade-vertical-leave-active {
  transition: opacity 0.4s, transform 0.4s ease;
}

.slide-fade-vertical-enter {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-fade-vertical-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
  transform: translateX(10px);
}
</style>
