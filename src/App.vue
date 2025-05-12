<template>
  <div id="app">
    <Header />
    <main>
      <Hero />
      <Features />
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Hero from './components/Hero.vue';
import Features from './components/Features.vue';
import Footer from './components/Footer.vue';

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Features,
    Footer
  }
}
</script>

<style>
@import url('./assets/styles/global.css');
</style>