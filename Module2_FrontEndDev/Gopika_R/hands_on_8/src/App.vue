<template>
  <div class="app-wrapper">
    <Header />
    <main class="main-content">
      <RouterView />
    </main>
    <footer class="site-footer">
      <p>© 2026 Student Portal | All Rights Reserved</p>
    </footer>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>
