<script setup>
import { ref } from 'vue'
import SiteHeader from './components/SiteHeader.vue'
import HomeView from './components/HomeView.vue'
import SearchView from './components/SearchView.vue'
import DossierView from './components/DossierView.vue'
import EscrowView from './components/EscrowView.vue'
import StatusModal from './components/StatusModal.vue'
const page=ref('home'), party=ref(null), escrow=ref(null), searchQuery=ref('')
async function search(value) { searchQuery.value=value || ''; page.value='search' }
function found(data) { party.value=data; page.value='dossier' }
function navigate(next) { page.value=next }
</script>
<template><SiteHeader :active="page" @navigate="navigate"/><main><HomeView v-if="page==='home'" @search="search"/><SearchView v-else-if="page==='search'" :initial="searchQuery" @found="found"/><DossierView v-else-if="page==='dossier'" :party="party" @navigate="navigate"/><EscrowView v-else-if="page==='escrow'" :party="party" @created="escrow=$event"/><section v-else class="mx-auto max-w-[1080px] px-5 py-24"><h1 class="text-4xl font-semibold">Тарифы</h1><p class="mt-4 text-[#999]">Единая комиссия за гарант-сделку — 1,2% от суммы. Проверка контрагента доступна в составе сервиса.</p><button class="mt-8 rounded-full bg-white px-6 py-3 text-black" @click="page='escrow'">Открыть гарант-сделку</button></section></main><footer v-if="page==='home'" class="border-t border-[#242424] py-5"><div class="flex justify-between px-[42px] text-[16px] text-[#777]"><span>Smart Retail · проверка и гарант сделок</span><span>Оферта · Политика конфиденциальности</span></div></footer><StatusModal :result="escrow" @close="escrow=null"/></template>
