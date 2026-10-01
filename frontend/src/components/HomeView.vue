<script setup>
import { onMounted, ref } from 'vue'
import { partyApi } from '../services/api'

const emit = defineEmits(['search'])
const query = ref('')
const history = ref([])
const loadingHistory = ref(true)
const statusLabel = status => status === 'ACTIVE' ? 'Действует' : status === 'LIQUIDATING' ? 'Ликвидируется' : status === 'BANKRUPT' ? 'Банкротство' : status || 'Не указан'
const statusTone = status => status === 'ACTIVE' ? 'text-[#89d4ae]' : status === 'LIQUIDATING' ? 'text-[#e4c46b]' : 'text-[#dc9298]'
const checkedAt = value => value ? new Intl.DateTimeFormat('ru-RU', { dateStyle:'short', timeStyle:'short' }).format(new Date(value)) : ''
async function loadHistory() { try { history.value = await partyApi.history() } finally { loadingHistory.value = false } }
function submit() { emit('search', query.value) }
onMounted(loadHistory)
</script>

<template>
  <section class="mx-auto max-w-[1404px] px-5 pb-[85px] pt-[112px]">
    <div class="text-center"><h1 class="text-[58px] font-medium tracking-[-.04em]">Начнём новую проверку?</h1><p class="mt-4 text-[21px] text-[#8b8b8f]">Досье, риски и гарант сделки в одном поиске.</p><form class="mx-auto mt-5 flex h-[61px] max-w-[936px] rounded-full border border-[#3b3b3d] bg-[#131313] p-1" @submit.prevent="submit"><input v-model="query" class="min-w-0 flex-1 bg-transparent px-6 text-[19px] text-white outline-none placeholder:text-[#777]" placeholder="ИНН, название, руководитель или адрес"><button class="rounded-full bg-white px-7 text-[16px] font-medium text-black">Найти</button></form></div>
    <div class="mt-[57px] grid overflow-hidden rounded-[20px] border border-[#262626] md:grid-cols-4"><article v-for="(item,i) in [['Проверка','Статус, руководитель, адрес и дата регистрации'],['Гарант','Деньги у сервиса, пока поставка не подтверждена'],['Суды','Арбитраж: число дел, суммы и стадия'],['Финансы','Выручка, прибыль и численность за последний год'],['Связи','Учредители, директор и связанные компании'],['Санкции','Совпадения по спискам и иноагенты'],['Долги','ФССП, налоги и заблокированные счета'],['Досье','Реквизиты, ОКВЭД и выписка в одном экране']]" :key="item[0]" class="min-h-[145px] border-b border-r border-[#262626] p-6"><p class="font-mono text-sm text-[#656568]">0{{i+1}}</p><h2 class="mt-2 text-[20px] font-medium">{{item[0]}}</h2><p class="mt-1 max-w-[260px] text-[16px] leading-5 text-[#858589]">{{item[1]}}</p></article></div>
    <div class="mt-9 flex items-center justify-between"><h2 class="text-[18px] font-medium">Недавние проверки</h2><span class="text-[#77777b]">реальные запросы</span></div>
    <div class="mt-6 overflow-auto"><table class="w-full min-w-[850px] text-left"><thead class="border-b border-[#242424] text-sm text-[#77777b]"><tr><th class="pb-3 font-normal">Компания</th><th class="pb-3 font-normal">ИНН</th><th class="pb-3 font-normal">Город</th><th class="pb-3 font-normal">Статус</th><th class="pb-3 font-normal">Проверено</th></tr></thead><tbody><tr v-if="loadingHistory"><td class="py-8 text-[#777]" colspan="5">Загружаем историю…</td></tr><tr v-else-if="!history.length"><td class="py-8 text-[#777]" colspan="5">История пока пуста. Проверьте первую компанию — она появится здесь.</td></tr><tr v-for="item in history" :key="item.inn" class="cursor-pointer border-b border-[#242424] text-[17px] hover:bg-white/[.03]" @click="emit('search', item.inn)"><td class="py-5 font-medium">{{item.name}}</td><td class="py-5 text-[#aaa]">{{item.inn}}</td><td class="py-5 text-[#aaa]">{{item.city || '—'}}</td><td class="py-5" :class="statusTone(item.status)">●&nbsp; {{statusLabel(item.status)}}</td><td class="py-5 text-[#bbb]">{{checkedAt(item.checked_at)}}</td></tr></tbody></table></div>
  </section>
</template>
