<script>
import LayoutStart from "./components/LayoutStart.vue";
import LayoutForm from "./components/LayoutForm.vue";


const version = import.meta.env.VITE_APP_VERSION;
console.log('Version:', version);
const copyright_year = new Date().getFullYear();

export default {
  components: {LayoutForm, LayoutStart},
  data() {
    return {
      started: true, // set to false for introduction text
      version: version,
      copyright_year: copyright_year
    }
  }
};
</script>

<template>
  <div class="container">

    <section class="section pt-0">
      <div class="tags mt-2 mb-1">
        <a href="https://github.com/magenbrot/Feuerwehr-Beitrag-Generator" title="Quellcode ansehen" target="_blank" rel="me external" class="tag is-info is-rounded">Quellcode (github.com)</a>
        Version {{version}}
      </div>

      <h1 class="title is-2">Feuerwehr Beitrag Generator</h1>
      <h2 class="subtitle is-5">Für Social Media Posts</h2>

      <div v-if="started === false">
        <LayoutStart/>
        <button class="button is-success" @click="started = true">Post erstellen</button>
      </div>
      <div v-else>
        <hr>
        <LayoutForm/>
      </div>

      <footer>
        <hr>
        <small>Copyright {{copyright_year}} // Hosted by <a href="https://ovtec.it/" rel="noopener me external" target="_blank" title="Oliver Völker">@magenbrot</a>. Original work by <a href="https://hemk.es/" rel="noopener me external" target="_blank" title="Nico Hemkes">@turbopixel</a></small>
      </footer>
    </section>
  </div>
</template>

<style>
html, body{
  background: #fdfdfd;
}
</style>
