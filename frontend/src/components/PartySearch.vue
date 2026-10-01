<script setup>
import { ref, computed } from 'vue'
const emit = defineEmits(['found'])
const inn = ref(''), loading = ref(false), error = ref('')
const valid = computed(() => /^\d{10}(\d{2})?$/.test(inn.value))
async function submit() { if (!valid.value) { error.value='Введите ИНН из 10 или 12 цифр'; return }; loading.value=true; error.value=''; try { const { partyApi } = await import('../services/api'); emit('found', await partyApi.check(inn.value)) } catch (e) { error.value=e.message } finally { loading.value=false } }
</script>
<template><section class="shell py-12 md:py-20"><p class="eyebrow">Проверка контрагента</p><div class="mt-5 max-w-[760px]"><h1 class="text-4xl font-bold leading-tight md:text-6xl">Проверяем бизнес.<br><span class="text-acid">Защищаем сделки.</span></h1><p class="mt-6 max-w-[540px] text-base leading-7 text-muted">Введите ИНН компании — Smart Retail соберёт реквизиты и оценит факторы риска до начала сделки.</p><form class="mt-10 flex flex-col gap-3 sm:flex-row" @submit.prevent="submit"><input v-model="inn" inputmode="numeric" maxlength="12" class="field flex-1" placeholder="ИНН контрагента"><button class="action sm:w-48" :disabled="loading">{{ loading ? 'Проверяем...' : 'Проверить' }} <span class="ml-2">→</span></button></form><p v-if="error" class="mt-3 text-sm text-red-400">{{ error }}</p><p class="mt-5 text-xs text-[#777]">Данные получаютcя из официальных и открытых источников</p></div></section></template>
