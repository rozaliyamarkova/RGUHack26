<script setup>
import { ref, onMounted, computed } from 'vue'
import { getRequest, postRequest, putRequest, deleteRequest } from '../helpers/api_helper'

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
const selectedCourseAssignments = ref([])
const selectedAssignment = ref(null)

const bustimes = ref([])

const favourite_bus = ref('')

const newAssignmentName = ref('')
const newAssignmentDueDate = ref('')
const newAssignmentTimeNeeded = ref('')
const newAssignmentWeighting = ref('')
const newAssignmentGrade = ref('')
const favourite_bus_message = ref('')


const sdr_library_occupancy = ref({})
const rgu_library_occupancy = ref({})

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

          rgu_library_occupancy.value = await getRequest('/libraries/rgu/occupancy')

        } catch (err) {
          console.error('Error fetching modules:', err)
        }
      }
    })
  }
  chrome.storage.sync.get('favourite_bus', (data) => {
    if (data.favourite_bus) {
      favourite_bus.value = data.favourite_bus;
      format_favourite_bus();
    }
  })
}
)

function logEverything() {
  console.log(modules.value)
  console.log(sdr_library_occupancy.value)
  console.log(rgu_library_occupancy.value)
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

function saveFavourite(bus) {
  if (typeof chrome !== 'undefined' && chrome.storage) {
    chrome.storage.sync.set({ favourite_bus: bus.value }, () => {
      console.log('Favourite bus saved:', bus.value)
    })
  }
}


async function openCourse(course) {
  selectedCourse.value = course
  screen.value = 'course'
  const assignments = await getRequest(`/courses/${course.id}/assignments`)
  selectedCourseAssignments.value = assignments
}



const courseStats = computed(() => {
  const assignments = selectedCourseAssignments.value
  if (!assignments.length) return null

  const graded = assignments.filter(a => a.grade !== null && a.weighting)
  const totalWeighting = assignments.reduce((sum, a) => sum + (a.weighting || 0), 0)
  const gradedWeighting = graded.reduce((sum, a) => sum + a.weighting, 0)
  const weightedGrade = graded.reduce((sum, a) => sum + (a.grade * a.weighting), 0)

  const totalHours = assignments.reduce((sum, a) => sum + (a.time_needed || 0), 0)
  const upcoming = assignments.filter(a => a.grade === null)

  return {
    weightedAverage: gradedWeighting > 0 ? (weightedGrade / gradedWeighting * 100).toFixed(1) : null,
    overallTotal: gradedWeighting > 0 ? (weightedGrade * 100).toFixed(1) : null,
    gradedPercent: (gradedWeighting * 100).toFixed(0),
    totalPercent: (totalWeighting * 100).toFixed(0),
    totalHours,
    remaining: upcoming.length,
  }
})

const procrastination = computed(() => {
  const assignments = selectedCourseAssignments.value
  if (!assignments.length) return null

  const upcoming = assignments.filter(a => a.grade === null && a.due_date)
  if (!upcoming.length) return { message: "Nothing due... procrastinate forever!", hours: null }
  const sorted = [...upcoming].sort((a, b) => new Date(a.due_date) - new Date(b.due_date))

  let freeHours = Infinity

  for (const assignment of sorted) {
    const hoursUntilDue = (new Date(assignment.due_date) - Date.now()) / (1000 * 60 * 60)
    const buffer = hoursUntilDue - assignment.time_needed
    if (buffer < freeHours) freeHours = buffer
  }

  if (freeHours <= 0) {
    return { message: "You should be working right now!", hours: 0, danger: true }
  } else if (freeHours < 24) {
    return { message: `Only ${freeHours.toFixed(1)}h left to procrastinate`, hours: freeHours, danger: true }
  } else {
    const days = Math.floor(freeHours / 24)
    const remainingHours = (freeHours % 24).toFixed(0)
    return { message: `${days}d ${remainingHours}h of dilly dallying`, hours: freeHours, danger: false }
  }
})

async function openAssignment(assignment) {
  selectedAssignment.value = {
    ...assignment,
    due_date: assignment.due_date ? assignment.due_date.split('T')[0] : '',
  }
  screen.value = 'assignment'
}

async function updateAssignment() {
  try {
    const data = await putRequest(`/assignments/${selectedAssignment.value.id}`, {
      title: selectedAssignment.value.title,
      due_date: selectedAssignment.value.due_date,
      time_needed: selectedAssignment.value.time_needed,
      weighting: selectedAssignment.value.weighting || null,
      grade: selectedAssignment.value.grade || null,
    })
    selectedAssignment.value = data
    // Update it in the list too
    const idx = selectedCourseAssignments.value.findIndex(a => a.id === data.id)
    if (idx !== -1) selectedCourseAssignments.value[idx] = data
  } catch (err) {
    console.error('Error updating assignment:', err)
  }
}

async function addAssignment() {
  try {
    /*
  title: str
    due_date: str
    time_needed:int
    weighting: float|None = None
    grade: float|None = No
    */
    const data = await postRequest(`/courses/${selectedCourse.value.id}/assignments`, {
      title: newAssignmentName.value,
      due_date: newAssignmentDueDate.value,
      time_needed: newAssignmentTimeNeeded.value,
      weighting: newAssignmentWeighting.value || null,
      grade: newAssignmentGrade.value || null,
    })
    console.log('Assignment added:', data)
    newAssignmentName.value = ''
    newAssignmentDueDate.value = ''
    newAssignmentTimeNeeded.value = ''
    newAssignmentWeighting.value = ''
    newAssignmentGrade.value = ''
    selectedCourseAssignments.value.push(data)
  } catch (err) {
    console.error('Error adding assignment:', err)
  }
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

async function change_favourite(bus) {
  try {
    favourite_bus.value = bus;
    console.log(`${bus.line} | ${formatTime(bus.departure_time)} ★ `);
    saveFavourite(favourite_bus);
    return (`${bus.line} | ${formatTime(bus.departure_time)} ★ `)
  } catch (err) {
    console.error('Something went front with changing favourite bus', err);
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

const formatBus = (bus) => {
  if (bus == favourite_bus.value) {
    return (`${bus.line} | ${formatTime(bus.departure_time)} ★ `)
  } else {
    return (`${bus.line} | ${formatTime(bus.departure_time)} ☆ `)
  }
}


const format_favourite_bus = () => {
  if (favourite_bus) {
    console.log(favourite_bus.value);
    console.log(favourite_bus.value.departure_time);
    let bus_departure_date = new Date(favourite_bus.value.departure_time);
    let js_bullshit = new Date;
    let current_time = js_bullshit.getTime();

    let difference = bus_departure_date - current_time;
    difference = (Math.round(difference / 60000));

    favourite_bus_message.value = `Your bus will be at your stop in ${difference} minutes :)`;
  } else {
    return ``
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
      <div> {{ favourite_bus_message }} </div>
      <div class="divider"></div>
      <div class="input-group">
        <button @click="screen = 'modules'" class="btn">Modules</button>
        <button @click="screen = 'bus-timetable'" class="btn">Bus Timetable</button>
        <button @click="screen = 'lib'" class="btn">Library</button>
      </div>
    </div>

    <!-- Library Choice -->
    <div v-else-if="screen === 'lib'" class="card fade-in">
      <h1 class="name">Choose your fighter!</h1>
      <div class="divider"></div>
      <div class="input-group">
        <button @click="screen = 'uoalib'" class="btn">UOA Library</button>
        <button @click="screen = 'rgulib'" class="btn">RGU Library</button>
        <button @click="screen = 'choice1'" class="btn">Back</button>
      </div>
    </div>

    <!-- RGU Library Occupancy -->
    <div v-else-if="screen === 'rgulib'" class="card fade-in">
      <h1 class="name">RGU Library Occupancy</h1>
      <div class="divider"></div>
      <div v-for="floor in rgu_library_occupancy.floors" :key="floor.name" class="library-level">
        <p class="label">{{ floor.name }}</p>
        <p class="subtitle">
          {{ floor.current_usage }}/{{ floor.capacity }} people ({{ floor.occupancy_percentage }}%) —
          <span
            :class="floor.status === 'Not Busy' ? 'status-not-busy' : floor.status === 'Busy' ? 'status-busy' : 'status-very-busy'">
            {{ floor.status }}
          </span>
        </p>
      </div>
      <button @click="screen = 'lib'" class="btn">Back</button>
    </div>

    <!-- UOA Library Occupancy -->
    <div v-else-if="screen === 'uoalib'" class="card fade-in">
      <h1 class="name">UOA Library Occupancy</h1>
      <div class="divider"></div>
      <div class="library-level">
        <p class="subtitle">
          {{ sdr_library_occupancy.occupancy_percentage }}% —
          <span
            :class="sdr_library_occupancy.occupancy_percentage < 50 ? 'status-not-busy' : sdr_library_occupancy.occupancy_percentage < 80 ? 'status-busy' : 'status-very-busy'">
            {{ sdr_library_occupancy.occupancy_percentage < 50 ? 'Not Busy' : sdr_library_occupancy.occupancy_percentage
              < 80 ? 'Busy' : 'Very Busy' }} </span>
        </p>
      </div>
      <button @click="screen = 'lib'" class="btn">Back</button>
    </div>

    <!-- Modules screen -->
    <div v-else-if="screen === 'modules'" class="card fade-in">
      <div class="input-group">
        <button @click="screen = 'choice1'; format_favourite_bus();" class="btn">Back</button>
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
        <div v-if="courseStats">

          <p v-if="courseStats.weightedAverage">Average: {{ courseStats.weightedAverage }}%</p>
          <p v-else>No grades yet</p>
          <p>{{ courseStats.gradedPercent }}% / {{ courseStats.totalPercent }}% graded</p>
          <p v-if="courseStats.overallTotal">Running total: {{ courseStats.overallTotal }}%</p>
          <br />
          <p>{{ courseStats.totalHours }}h total work, {{ courseStats.remaining }} assignments remaining</p>
        </div>
        <div v-if="procrastination">
          <strong>Procrastination Timer</strong><br />
          <p>
            {{ procrastination.message }}
          </p>
        </div>
        <hr />
        <input v-model="newAssignmentName" type="text" placeholder="Assignment name..." class="input" />
        <input v-model="newAssignmentDueDate" type="date" class="input" />
        <input v-model="newAssignmentTimeNeeded" type="number" placeholder="Time needed (hours)..." class="input" />
        <input v-model="newAssignmentWeighting" type="number" step="0.01" placeholder="Weighting (0-1)..."
          class="input" />
        <input v-model="newAssignmentGrade" type="number" step="0.01" placeholder="Grade (0-1)..." class="input" />
        <button class="btn" @click="addAssignment">Add Assignment</button>

        <div v-for="assignment in selectedCourseAssignments" :key="assignment.id" @click="openAssignment(assignment)">
          <strong>{{ assignment.title }}</strong>
          <span v-if="assignment.weighting"> : {{ (assignment.weighting * 100).toFixed(0) }}%</span>
          <br />
          <div>
            Due: {{ new Date(assignment.due_date).toLocaleDateString() }}
            · {{ assignment.time_needed }}h
            <span v-if="assignment.grade !== null"> · Grade: {{ assignment.grade }}</span>
            <span v-else> · Not graded</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="screen === 'assignment'" class="card fade-in">
      <div class="input-group">
        <h1 class="name">{{ selectedAssignment.title }}</h1>
        <button @click="screen = 'course'" class="btn">Back</button>
        <hr />
        <input v-model="selectedAssignment.title" type="text" placeholder="Title" class="input" />
        <input v-model="selectedAssignment.due_date" type="date" class="input" />
        <input v-model="selectedAssignment.time_needed" type="number" placeholder="Time needed (hours)" class="input" />
        <input v-model="selectedAssignment.weighting" type="number" step="0.01" placeholder="Weighting (0-1)"
          class="input" />
        <input v-model="selectedAssignment.grade" type="number" step="0.01" placeholder="Grade (0-1)" class="input" />
        <button class="btn" @click="updateAssignment">Save</button>
      </div>
    </div>

    <!-- Bus Timetable screen -->
    <div v-else-if="screen === 'bus-timetable'" class="card fade-in">
      <div class="input-group">
        <ul class="busstop-list">
          <li v-for="stop in busstops" :key="stop.id" class="stop-item">
            <!--<button @click="screen = 'stop-timetable'; getUpcoming(stop.id)" class="btn">{{ stop.common_name }}</button>-->
            <button @click="screen = 'stop-timetable'; getUpcoming(stop.ATCOCode);" class="btn">{{ stop.common_name }},
              {{ stop.indicator }}</button>
          </li>
        </ul>
      </div>
      <button @click="screen = 'choice1'; format_favourite_bus();" class="btn">Back</button>
    </div>

    <!-- Bus Stop screen -->
    <div v-else-if="screen === 'stop-timetable'" class="card fade-in">
      <div class="input-group">
        <ul class="busstop-busses">
          <li v-for="bus in bustimes" :key="bus.id" class="bus-item">
            <!-- <button class="btn">{{ bus.line }} | {{ formatTime(bus.departure_time) }} ☆ </button> -->


            <button @click="change_favourite(bus);" class="btn">{{ formatBus(bus) }} </button>
            <!-- ★ -->
          </li>
        </ul>
      </div>
      <button @click="screen = 'bus-timetable'" class="btn">Back</button>
    </div>

  </div>
</template>