<script setup lang="ts">
import Navbar from '@/components/navbar/Navbar.vue'
import Profile from '../profile/Profile.vue'
import AppLogo from './AppLogo.vue'

const appName = 'CRUD 2.0'
</script>

<template>
  <header class="app-header">
    <nav class="app-header__nav">
      <AppLogo :name="appName" />

      <Navbar />

      <Profile />
    </nav>
  </header>
</template>
