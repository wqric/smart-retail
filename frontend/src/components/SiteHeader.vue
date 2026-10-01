<script setup>
defineProps({ active: String })
const emit = defineEmits(['navigate'])
const links = [['home', 'Smart Retail'], ['search', 'Проверка'], ['escrow', 'Гарант'], ['tariffs', 'Тарифы']]
</script>
<template>
  <header class="border-b border-[#202020] bg-[#050505]"><div class="flex h-[91px] items-center px-[42px]">
    <button class="text-[19px] font-medium text-white" @click="emit('navigate','home')">Smart Retail</button>
    <nav class="absolute left-1/2 flex -translate-x-1/2 gap-8 text-[17px] text-[#7e7e82]"><button v-for="[key,label] in links.slice(1)" :key="key" class="transition hover:text-white" :class="active===key && 'text-white'" @click="emit('navigate', key)">{{ label }}</button></nav>
    <button class="ml-auto rounded-full border border-[#323236] px-5 py-2 text-[17px] text-white">Войти</button>
  </div></header>
</template>
