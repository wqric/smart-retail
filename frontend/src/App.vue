<script setup>
import { ref } from 'vue'
import PartySearch from './components/PartySearch.vue'
import PartyCard from './components/PartyCard.vue'
import EscrowForm from './components/EscrowForm.vue'
import StatusModal from './components/StatusModal.vue'
const party=ref(null), escrow=ref(null)
</script>
<template><header class="border-b border-line"><div class="shell flex h-20 items-center justify-between"><a class="text-lg font-bold tracking-tight">smart<span class="text-acid">retail</span></a><span class="rounded-full border border-line px-3 py-1.5 text-xs text-muted">Безопасные B2B-сделки</span></div></header><main><PartySearch @found="party=$event"/><PartyCard v-if="party" :party="party"/><EscrowForm v-if="party" :party="party" @created="escrow=$event"/></main><footer class="border-t border-line py-7"><div class="shell flex justify-between text-xs text-muted"><span>© Smart Retail, 2026</span><span>Проверка · Эскроу · Контроль</span></div></footer><StatusModal :result="escrow" @close="escrow=null"/></template>
