<template>
  <div class="options-content">
        <router-link v-for="(item, index) in column" :key="index" v-if="item.data" class="btn" :to="startSearch(item)">
          <div class="card-book">
            <img loading="lazy" :src="item.data.image" class="image" alt="Cover Book">
            <div class="text-wrap">
              <h5 class="text-card">
                {{ item.data.title }}
              </h5>
            </div>
          </div>
        </router-link>
  </div>
</template>

<script>
import { encode } from '../../utils/encoding.js'

export default {
  name: 'GridLibrary',
  props: {
    column: Array
  },
  methods: {
    startSearch (item) {
      const newQuery = {
        search: item.data.title,
        type: item.type,
        id: item.data.id
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
.options-content{
  display: grid;
  grid-template-columns: repeat(auto-fit, 5rem);
  gap: 1rem;
  align-items: center;
  padding-block: var(--panel-gap);
  padding-left: calc(var(--panel-gap)/2);
}

.btn{
  padding: var(--panel-gap);
  border: 0;
  border-radius: var(--border-radius);
}

.btn:hover{
  background: var(--half-transparent-background);
}

.card-book{
  color: var(--text-color);
  display: flex;
  flex-direction: column;
  gap: var(--panel-gap);
}

.card-book.list{
  flex-direction: row;
}

.image{
  height: 8rem;
  border-radius: var(--border-radius);
  box-shadow: 0 0 0.5rem var(--half-transparent-main-background);
}

.text-wrap{
  justify-content: center;
  display: flex;
}

.text-card{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: var(--font-size-xs);
}

</style>
