<script setup>
import { ref, onMounted } from 'vue'
import { getRequest, postRequest } from '../helpers/api_helper'

const newModuleName = ref('')
const nameInput = ref('')
const userName = ref('')
const error = ref('')
const screen = ref('name')

const modules = ref([])

onMounted(() => {
  if (typeof chrome !== 'undefined' && chrome.storage) {
    chrome.storage.sync.get('userName', (data) => {
      if (data.userName) {
        userName.value = data.userName
        screen.value = 'choice1'

      }
    })
    chrome.storage.sync.get("user_id", async (data) => {
      if (data.user_id) {
        try {

          modules.value = await getRequest('/courses')
  
        } catch (err) {
          console.error('Error fetching modules:', err)
        }
      }
    })
  }
})

function logEverything() {
  console.log(modules.value)
}

function saveStudent(data) {  
  if (typeof chrome !== 'undefined' && chrome.storage) {
    chrome.storage.sync.set({ userName: data.name, user_id: data.user_id }, () => {
      userName.value = data.name
      screen.value = 'choice1'
      error.value = ''
    })
  } else {
    userName.value = data.name
    screen.value = 'choice1'
  }
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

async function addModule() {
  try {
    const data = await postRequest('/courses', { name: newModuleName.value })
    console.log('Module added:', data)
    newModuleName.value = ''
    modules.value.push(data)
  } catch (err) {
    console.error('Error adding module:', err)
  }
}



</script>

<template>
  <div class="container">
    <!-- Screen that takes the name of the user -->
    <div v-if="screen === 'name'" class="card fade-in">
      <h1 class="title">Hello {{ nameInput }}!</h1>
      <div class="input-group">
        <input v-model="nameInput" type="text" placeholder="Don Diablo" class="input" />
        <button @click="registerStudent" class="btn">Continue</button>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- Modules / Bus Timetables-->
    <div v-else-if="screen === 'choice1'" class="card fade-in">
      <h1 class="name">Hello {{ userName }}!</h1>
      <div class="divider"></div>
      <div class="input-group">
        <button @click="screen = 'modules'" class="btn">Modules</button>
        <button @click="screen = 'bus-timetable'" class="btn">Bus Timetable</button>
        <button @click="screen = 'lib'" class="btn">Library</button>
      </div>
    </div>

    <!-- Library Choice -->
    <div v-else-if="screen === 'lib'" class="card fade-in">
      <h1 class="name">Select a library to check occupancy</h1>
      <div class="divider"></div>
      <div class="input-group">
        <button @click="screen = 'abdnlib'" class="btn">ABDN Library</button>
        <button @click="screen = 'rgulib'" class="btn">RGU Library</button>
      </div>
    </div>

    <!-- RGU Library Occupancy -->
    <div v-else-if="screen === 'rgulib'" class="card fade-in">
      <h1 class="name">RGU Library Occupancy</h1>
      <div class="divider"></div>
    </div>

    <!-- ABND Library Occupancy -->
    <div v-else-if="screen === 'abdnlib'" class="card fade-in">
      <h1 class="name">ABDN Library Occupancy</h1>
      <div class="divider"></div>
    </div>

    <!-- Modules screen -->
    <div v-else-if="screen === 'modules'" class="card fade-in">
      <div class="input-group">
        <button @click="screen = 'assignments'" class="btn">Assignments</button>
        <button @click="screen = 'notes'" class="btn">Notes</button>
        <button @click="screen = 'choice1'" class="btn">Back</button>
        <hr />
        <input v-model="newModuleName" type="text" placeholder="Enter name..." class="input" />
        <button class="btn" @click="addModule">Add Module</button>
        <button v-for="course in modules" :key="course.id"class="btn is-light">{{ course.name }}</button>
      </div>
    </div>

    <
  </div>
</template>