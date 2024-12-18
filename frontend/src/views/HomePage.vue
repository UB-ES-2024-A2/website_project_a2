<template>
  <div>
    <div @resize="ResetColumnSizes">
      <div id="page" class="grid-layout min-vh-100">

        <main-header
                      :actualPage="currentTab"
                      @category-selected="startCategory"
                      @home-update="startHome"
                      @search-selected="startSearch"
                      @info-selected="startInfo"/>

        <library
          :myBooksList="myBooksList"
          :loadingMyBooks="loadingMyBooks"
           @set-size="setSize"/>

        <div id="leftdragbar" class="leftdragbar" @mousedown="StartLeftDrag"
                                                  @touchstart="StartLeftDrag"></div>

        <div id="tabs" class="tabs">
          <filter-header :searchResults="searchResults" :currentTab="currentTab" @genres-updated="handleGenresUpdate"/>

          <transition name="slide-fade" mode="out-in">
            <component :is="currentTab" :searchResults="searchResults" :loading="loading" :myBooksList="myBooksList"
                        @update-my-books="setMyBooks"
                        @updated-comments="readMyBooks"/>
          </transition>

          <footer-tabs/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DefaultLibrary from '@/components/DefaultLibrary'
import BookPage from '@/components/BookPage'
import DefaultTab from '@/components/Tab'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import FilterHeader from '@/components/FilterHeader'
import CategoryTab from '@/components/CategoryTab'

import Information from '@/components/Information'

import Profile from '@/components/Profile'
import BookService from '@/services/BookService'
import VueJwtDecode from 'vue-jwt-decode'

const PageEnum = Object.freeze({
  HOME: 'default',
  BOOK: 'book-page',
  CATEGORY: 'category',
  PROFILE: 'profile',
  INFO: 'information'

})

export default {
  name: 'HomePage',
  components: {
    'main-header': Navbar,
    'library': DefaultLibrary,
    'default': DefaultTab,
    'book-page': BookPage,
    'footer-tabs': Footer,
    'filter-header': FilterHeader,
    'category': CategoryTab,
    'information': Information,
    'profile': Profile

  },

  data () {
    return {
      isLeftDragging: false,
      columnSizes: ['6rem', 'var(--dragbar-width)', 'auto'],
      searchResults: [],
      currentTab: PageEnum.HOME,
      loading: true,
      myBooksList: [],
      loadingMyBooks: true
    }
  },
  created () {
    this.initializeSearchResults()
  },
  methods: {
    handleGenresUpdate (selectedGenres) {
      this.loading = true
      this.searchResults[0].list = []
      if (selectedGenres.length === 0) {
        this.initializeSearchResults()
        this.loading = false
        return
      }
      BookService.filterBooks(selectedGenres).then(response => {
        const books = response.data.data
        this.searchResults[0].list = books.map(book => ({
          type: 'book',
          data: {
            title: book.title,
            genres: book.genres || [],
            image: book.image,
            authors: book.authors || 'Unknown Author',
            synopsis: book.synopsis || 'No synopsis available',
            id: book.id_book
          }
        }))
        this.loading = false
      })
        .catch(error => {
          console.error('Error loading books:', error)
          this.loading = false
        })
    },
    ResetColumnSizes () {
      let page = document.getElementById('page')
      if (!page) return

      const [leftCol, dragbar, mainContent] = this.columnSizes
      const totalWidth = leftCol + dragbar + mainContent
      this.columnSizes = [
        `${(leftCol / totalWidth) * 100}fr`,
        `8px`,
        `${(mainContent / totalWidth) * 100}fr`
      ]
      page.style.gridTemplateColumns = this.columnSizes.join(' ')
    },
    SetCursor (cursor) {
      let page = document.getElementById('page')
      page.style.cursor = cursor
    },
    StartLeftDrag (event) {
      this.isLeftDragging = true
      this.SetCursor('ew-resize')
      window.addEventListener('mousemove', this.OnDrag)
      window.addEventListener('mouseup', this.EndDrag)
      window.addEventListener('touchmove', this.OnDrag, { passive: false })
      window.addEventListener('touchend', this.EndDrag, { passive: false })
      event.preventDefault()
    },
    EndDrag () {
      this.isLeftDragging = false
      this.SetCursor('auto')
      window.removeEventListener('mousemove', this.OnDrag)
      window.removeEventListener('mouseup', this.EndDrag)
      window.removeEventListener('touchmove', this.OnDrag)
      window.removeEventListener('touchend', this.EndDrag)
    },
    OnDrag (event) {
      let page = document.getElementById('page')
      let mousePosX = event.clientX || (event.touches && event.touches[0] ? event.touches[0].clientX : 0)
      if (this.isLeftDragging && mousePosX < (page.clientWidth / 2) && mousePosX > 114) {
        let gap = parseFloat(window.getComputedStyle(page).gap)
        let padding = parseFloat(window.getComputedStyle(page).paddingRight)

        let leftColWidth = mousePosX - gap / 2 - gap - padding

        this.columnSizes = [
          Math.max(leftColWidth, 0),
          gap,
          Math.max(page.clientWidth - mousePosX - gap / 2 - gap - padding, 0)
        ]

        page.style.gridTemplateColumns = this.columnSizes.map(c => c + 'px').join(' ')

        event.preventDefault()
      }
    },
    startSearch (data) {
      console.log('Searching for:', data)
      if (data[1] === 'book') {
        this.currentTab = PageEnum.BOOK
        this.searchResults = [
          {
            title: 'Search',
            list:
              {
                type: 'book',
                data: data[0]
              }
          }
        ]
      } else if (data[1] === 'user') {
        this.currentTab = PageEnum.PROFILE
        this.searchResults = [
          {
            title: 'Search',
            list:
              {
                type: 'user',
                data: data[0]
              }
          }
        ]
      }
    },
    startHome () {
      this.currentTab = PageEnum.HOME
      this.initializeSearchResults()
    },
    async initializeSearchResults () {
      this.loading = true
      const newSearchResults = [
        {
          title: 'Popular Books',
          list: []
        },
        {
          title: 'Recently Read',
          list: []
        },
        {
          title: 'Followed Users',
          list: []
        }
      ]
      BookService.readBooks().then(response => {
        const books = response.data.data
        newSearchResults[0].list = books.map(book => ({
          type: 'book',
          data: {
            title: book.title,
            genres: book.genres || [],
            image: book.image,
            authors: book.authors || 'Unknown Author',
            synopsis: book.synopsis || 'No synopsis available',
            rating: book.rating || 0.0,
            id: book.id_book
          }
        }))
        this.loading = false
      })
        .catch(error => {
          console.error('Error loading books:', error)
          this.loading = false
        })
      if (this.searchResults !== newSearchResults) {
        this.searchResults = newSearchResults
      }

      this.readMyBooks()
    },
    startCategory (data) {
      if (this.currentTab !== PageEnum.CATEGORY) {
        if (this.searchResults.length === 1) {
          this.initializeSearchResults()
        }
        this.currentTab = PageEnum.CATEGORY
        const newSearch = this.searchResults.find(column => column.title === data[0])
        if (newSearch) {
          this.searchResults = [newSearch]
        }
      }
    },
    startInfo () {
      this.currentTab = PageEnum.INFO
    },
    setSize () {
      let page = document.getElementById('page')
      let leftCol = document.getElementById('leftcol')
      if (!page || !leftCol) return

      if (leftCol.clientWidth > 103) {
        this.columnSizes = ['6rem', 'var(--dragbar-width)', 'auto']
      } else {
        this.columnSizes = ['20rem', 'var(--dragbar-width)', 'auto']
      }
      page.style.gridTemplateColumns = this.columnSizes.join(' ')
    },
    setMyBooks (data) {
      this.myBooksList = data
    },
    async readMyBooks () {
      if (this.token) {
        const myBooksNew = [
          {
            list: []
          }
        ]

        BookService.readMyBooks(VueJwtDecode.decode(this.token).sub).then(response => {
          const books = response.data.data
          myBooksNew[0].list = books.map(book => ({
            type: 'book',
            data: {
              title: book.title,
              genres: book.genres || [],
              image: book.image,
              authors: book.authors || 'Unknown Author',
              synopsis: book.synopsis || 'No synopsis available',
              rating: book.rating || 0.0,
              id: book.id_book
            }
          }))
          this.loadingMyBooks = false
          this.myBooksList = myBooksNew[0].list
        })
          .catch(error => {
            this.myBooksList = []
            console.error('Error loading books:', error)
            this.loadingMyBooks = false
          })
      } else {
        this.loadingMyBooks = false
      }
    }
  },
  computed: {
    token () {
      return this.$store.getters.token
    }
  },
  mounted () {
    window.addEventListener('resize', this.ResetColumnSizes)
  },
  beforeUnmount () {
    window.removeEventListener('resize', this.ResetColumnSizes)
  }
}
</script>

<style scoped>
.grid-layout {
  display: grid;
  gap: var(--panel-gap);
  grid-template-areas: 'global-nav global-nav global-nav'
                       'left-slider leftdragbar tabs';
  grid-template-rows: auto 1fr;
  grid-template-columns: 6rem var(--dragbar-width) auto;
  padding: var(--panel-gap);
  padding-top: 0;
  background-color: var(--main-background);
}

.leftdragbar {
  grid-area: leftdragbar;
  cursor: ew-resize;
  transition: transform 0.3s ease-in-out;
}

.leftdragbar:hover{
  background: var(--hover-dragbar-color);
}

.tabs {
  background: var(--box-background-color);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: calc(var(--border-radius) * 2);
  overflow: auto;
  overscroll-behavior-y: contain;
  grid-area: tabs;
  margin-left: calc(-1 * var(--panel-gap));
  display: grid;
  gap: var(--panel-gap);
  grid-template-areas: 'filter-option'
                       'main-page'
                       'footer';
  grid-template-rows: auto 1fr auto;
  max-height: 100vh;
  color: var(--text-color);
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
  transform: translateX(10px);
}

@media(max-width: 42.375rem){
  .grid-layout{
    grid-template-areas: 'global-nav global-nav global-nav'
                         'left-slider left-slider left-slider'
                         'leftdragbar leftdragbar leftdragbar'
                         'tabs tabs tabs';
    grid-template-rows: 5rem 15rem 0rem auto;
    grid-template-columns: auto;
  }

  .tabs{
    margin: var(--panel-gap);
  }
}
</style>
