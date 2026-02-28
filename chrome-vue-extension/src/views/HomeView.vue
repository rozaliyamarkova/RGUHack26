<script setup>
import { ref, onMounted } from 'vue'

const nameInput = ref('')
const userName = ref('')
const error = ref('')

onMounted(() => {
  chrome.storage.sync.get('userName', (data) => {
    if (data.userName) {
      userName.value = data.userName
    }
  })
})

function saveStudent(data) {  
  chrome.storage.sync.set({ userName: data.name, user_id: data.user_id}, () => {
    userName.value = data.name
    error.value = ''
  })
}

function getUserIdToken() {
  return new Promise((resolve) => {
    chrome.storage.sync.get('user_id', (data) => {
      resolve(data.user_id)
    })
  })
}

async function registerStudent() {
  if (!nameInput.value.trim()) {
    error.value = 'Please enter your name to continue.'
    return
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: nameInput.value })
    })

    const data = await response.json()

    saveStudent(data)
  } catch (err) {
    console.error(err)
    error.value = 'Please use letters only (A-Z).'
  }
}
</script>

<template>
  <div class="container">

    <!-- Screen that takes the name of the user -->
    <div v-if="!userName" class="card fade-in">
      <h1 class="title">Hello {{ nameInput }}!</h1>
      <div class="input-group">
        <input
          v-model="nameInput"
          type="text"
          placeholder="Your name"
          class="input"
        />
        <button @click="registerStudent" class="btn">Condtinue →</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- Greeting Screen -->
    <div v-else class="card fade-in">
      <p class="label">Good to see you,</p>
      <h1 class="name">{{ userName }}</h1>
      <p class="subtitle">Ready to get things done today?</p>
      <div class="divider"></div>
      <p class="tip">Your workspace is ready.</p>
    </div>

  </div>
</template>