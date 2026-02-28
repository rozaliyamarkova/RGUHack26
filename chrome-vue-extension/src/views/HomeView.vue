<script setup>
import { ref, onMounted } from 'vue'

const nameInput = ref('')
const userName = ref('')
const error = ref('')
const screen = ref('name')
const latitude_ref = ref('')
const longitude_ref = ref('')

const header = document.getElementById("tester")
onMounted(() => {
  if (typeof chrome !== 'undefined' && chrome.storage) {
    chrome.storage.sync.get('userName', (data) => {
      if (data.userName) {
        userName.value = data.userName
        screen.value = 'choice1'
      }
    })
  }
})

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

const generateDMS = (coords, isLat) => {
  const absCoords = Math.abs(coords);
  const deg = Math.floor(absCoords);
  const min = Math.floor((absCoords - deg) * 60);
  const sec = ((absCoords - deg - min / 60) * 3600).toFixed(1);
  const direction = coords >= 0 ? (isLat ? 'N' : 'E') : isLat ? 'S' : 'W';
  console.log('hello');
  return `${deg}°${min}'${sec}"${direction}`;
};

navigator.geolocation.getCurrentPosition(
  (loc) => {
    const { coords } = loc;
    console.log(loc);
    let {latitude, longitude} = coords;
    latitude_ref.value = latitude;
    longitude_ref.value = longitude;


    console.log(`position: ${latitude_ref.value}, ${longitude_ref.value}`);
  }
);
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
      </div>
    </div>

    <!-- Modules screen -->
    <div v-else-if="screen === 'modules'" class="card fade-in">
      <div class="input-group">
        <button @click="screen = 'assignments'" class="btn">Assignments</button>
        <button @click="screen = 'notes'" class="btn">Notes</button>
        <button @click="screen = 'choice1'" class="btn">Back</button>
      </div>
    </div>

    <!-- Bus Timetable screen -->
    <div v-else-if="screen === 'bus-timetable'" class="card fade-in">
      <div class="input-group">
        <div id="tester"> {{latitude_ref}} </div>

      </div>
    </div>
  </div>
</template>