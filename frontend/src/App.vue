<script>
export default {
  name: 'App'
}
</script>

<template>
  <div id="app" class="min-vh-100 min-vw-100">
    <router-view/>
  </div>
</template>

<style>
html, body {
  min-width: 31.25rem;
  min-height: 31.25rem;
  background-color: var(--main-background);
}

:root{
  /* Space */
  --panel-gap: 0.5rem;
  --dragbar-width: 0.5rem;
  --border-radius: 5px;
  --min-column-width: 5.625rem;
  --font-size-xs: 0.9rem;
  --font-size-medium: 1.5rem;
  --font-size-title: 2rem;

  /* Colors */
  --purple-background: #6f86d6;
  --blue-background: #48c6ef;
  --blue-link: #5777F5FF;

  /* Black theme */
  --text-color: white;
  --second-text-color: #d1cff8;
  --reverse-text-color:#1e1e1e;
  --text-color-secundary: #b1b1b1;

  --main-background: #121212;
  --reverse-background: white;

  --hover-dragbar-color: white;
  --dropdown-backgroudn-color: #393939;
  --box-background-color: #282828;
  --box-border-color: rgba(255, 255, 255, 0.2);
  --title-header-library: #535151;
  --button-background: #3f3f3f;
  --search-color-shadow: rgba(255, 255, 255, 0);
  --half-transparent-main-background: rgba(0, 0, 0, 0.5);
  --half-transparent-opposite-background: rgba(255, 255, 255, 0.5);

  --gray-background: #535151;
  --black-background: #1e1e1e;
  --half-transparent-background-purple: rgba(111, 134, 214, 0.5);
  --half-transparent-background: rgba(255, 255, 255, 0.1);

}

.tooltip-container {
  position: relative;
  display: inline-block;
}

.tooltip-text {
  visibility: hidden;
  background-color: var(--gray-background);
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  white-space: nowrap;
  z-index: 1;
  top: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.gradient-custom {
  background: linear-gradient(135deg, var(--purple-background), var(--blue-background)) no-repeat;
}

.gradient-custom-header{
  background: linear-gradient(0deg, var(--box-background-color), var(--purple-background)) no-repeat;
}

#app {
  font-family: Helvetica, 'Avenir', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}
</style>
