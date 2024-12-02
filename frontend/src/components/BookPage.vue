<template>
  <div id="main-page" class="main-page">
    <div v-if="type === 'book'">
      Book page info for {{ textInput }}
    </div>
    <div v-else>
      Users page info for {{ textInput }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookPage',
  data () {
    return {
      textInput: '',
      type: ''
    }
  },
  props: {
    searchResults: Array
  },
  watch: {
    '$route.query': {
      handler () {
        let textInput = this.$route.query.search || ''
        let type = this.$route.query.type || ''
        if (textInput !== '' && type !== '') {
          this.textInput = textInput
          this.type = type
        }
      },
      immediate: true
    }
  },
  mounted () {
    const token = this.$store.getters.token

    if (!token) {
      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
.book-page-wrap{
  grid-area: main-page;
  padding-inline: calc(var(--panel-gap)*2 + var(--panel-gap)/2);
}
</style>
