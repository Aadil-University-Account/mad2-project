<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '../api'

const items = ref([])
const open = ref(false)
let timer = null

const unread = computed(() => items.value.filter((n) => !n.is_read).length)

async function load() {
  try {
    const res = await api.get('/notifications')
    items.value = res.data
  } catch (e) {
    /* ignore */
  }
}

async function toggle() {
  open.value = !open.value
  if (open.value && unread.value) {
    await api.put('/notifications/read')
    setTimeout(load, 1500) // keep the "new" highlight for a moment
  }
}

onMounted(() => {
  load()
  timer = setInterval(load, 15000) // check for new notifications every 15 seconds
})
onUnmounted(() => clearInterval(timer))
</script>

<template>
  <div class="bell-wrap">
    <button class="btn btn-sm btn-outline-secondary position-relative" @click="toggle" title="Notifications">
      &#128276;
      <span v-if="unread" class="bell-count">{{ unread }}</span>
    </button>
    <div v-if="open" class="bell-panel">
      <div class="fw-bold mb-2">Notifications</div>
      <div v-if="!items.length" class="text-muted small">Nothing yet.</div>
      <div v-for="n in items" :key="n.id" class="bell-item" :class="{ new: !n.is_read }">
        {{ n.message }}<div class="trek-meta">{{ n.created_at }}</div>
      </div>
    </div>
  </div>
</template>
