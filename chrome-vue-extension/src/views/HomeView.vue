<script setup>
import { ref, onMounted } from 'vue'
import { getRequest, postRequest } from '../helpers/api_helper'

const newModuleName = ref('')
const nameInput = ref('')
const userName = ref('')
const error = ref('')
const screen = ref('name')
const modules = ref([])

const busstops = ref([])
const latitude_ref = ref('')
const longitude_ref = ref('')
const selectedCourse = ref(null)

const bustimes = ref([])

const sdr_library_occupancy = ref({})


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
          sdr_library_occupancy.value = await getRequest('/libraries/sdr/occupancy')
  
        } catch (err) {
          console.error('Error fetching modules:', err)
        }
      }
    })
  }
})

function logEverything() {
  console.log(modules.value)
  console.log(sdr_library_occupancy.value)
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

function openCourse(course) {
  selectedCourse.value = course
  screen.value = 'course'
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

async function getBusStops() {
  try {
    const data = await getRequest(`/closest_busses?longitude=${longitude_ref.value}&latitude=${latitude_ref.value}`)
    console.log(data);
    busstops.value = data;
  } catch (err) {
    console.error('Error getting busstops. idk what went wrong twin:', err)
  }
}

async function getUpcoming(busStopID) {
  try {
    console.log(busStopID);
    const data = await getRequest(`/bus/${busStopID}`)
    console.log("hello");
    console.log(data);
    bustimes.value = data;
  } catch (err) {
    console.error('Error getting upcoming. idk what went wrong twin:', err)
  }
}



const generateDMS = (coords, isLat) => {
  const absCoords = Math.abs(coords);
  const deg = Math.floor(absCoords);
  const min = Math.floor((absCoords - deg) * 60);
  const sec = ((absCoords - deg - min / 60) * 3600).toFixed(1);
  const direction = coords >= 0 ? (isLat ? 'N' : 'E') : isLat ? 'S' : 'W';;
  return `${deg}°${min}'${sec}"${direction}`;
};

navigator.geolocation.getCurrentPosition(
  (loc) => {
    const { coords } = loc;
    console.log(loc);
    let { latitude, longitude } = coords;
    latitude_ref.value = latitude;
    longitude_ref.value = longitude;


    console.log(`position: ${latitude_ref.value}, ${longitude_ref.value}`);
    getBusStops();
  }
);
const formatTime = (isoString) => {
  return new Date(isoString).toLocaleTimeString();
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
        <button @click="screen = 'uoalib'" class="btn">UOA Library</button>
        <button @click="screen = 'rgulib'" class="btn">RGU Library</button>
      </div>
    </div>

    <!-- RGU Library Occupancy -->
    <div v-else-if="screen === 'rgulib'" class="card fade-in">
      <h1 class="name">RGU Library Occupancy</h1>
      <div class="divider"></div>
    </div>

    <!-- ABND Library Occupancy -->
    <div v-else-if="screen === 'uoalib'" class="card fade-in">
      <h1 class="name">UOA Library Occupancy</h1>
      <div class="divider"></div>
      <div>
        <p>Current occupancy: {{ sdr_library_occupancy.occupancy_percentage }}%</p>
        <button @click="logEverything" class="btn">Log Occupancy Data</button>
      </div>
    </div>

    <!-- Modules screen -->
    <div v-else-if="screen === 'modules'" class="card fade-in">
      <div class="input-group">
        <button @click="screen = 'choice1'" class="btn">Back</button>
        <input v-model="newModuleName" type="text" placeholder="Enter module name..." class="input" />
        <button class="btn" @click="addModule">Add Module</button>
        <button v-for="course in modules" :key="course.id" class="btn" @click="openCourse(course)">
          {{ course.name }}
        </button>
      </div>
    </div>

    <!-- Specific module screen -->
    <div v-else-if="screen === 'course'" class="card fade-in">
      <div class="input-group">
        <h1 class="name">{{ selectedCourse.name }}</h1>
        <button @click="screen = 'modules'" class="btn">Back</button>
      </div>
    </div>

    <!-- Bus Timetable screen -->
    <div v-else-if="screen === 'bus-timetable'" class="card fade-in">
      <div class="input-group">
        <ul class="busstop-list">
          <li v-for="stop in busstops" :key="stop.id" class="stop-item">
            <!--<button @click="screen = 'stop-timetable'; getUpcoming(stop.id)" class="btn">{{ stop.common_name }}</button>-->
            <button @click="screen = 'stop-timetable'; getUpcoming(stop.ATCOCode);" class="btn">{{ stop.common_name }}, {{ stop.indicator}}</button>
          </li>
        </ul>
      </div>
      <button @click="screen = 'choice1'" class="btn">Back</button>
    </div>

    <!-- Bus Stop screen -->
     <div v-else-if="screen === 'stop-timetable'" class="card fade-in">
      <div class="input-group">
        <ul class="busstop-busses">
          <li v-for="bus in bustimes" :key="bus.id" class="bus-item">
            <button class="btn">{{ bus.line }} | {{ formatTime(bus.departure_time) }}</button>
          </li>
        </ul>
      </div>
      <button @click="screen = 'bus-timetable'" class="btn">Back</button>
    </div>
    
  </div>
</template>