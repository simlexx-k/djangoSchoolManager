<template>
  <div class="error-page">
    <div class="error-content">
      <h1 class="error-title">404</h1>
      <div class="error-message">
        <h2>Oops! Page not found</h2>
        <p>The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>
      </div>
      <div class="educational-fact">
        <h3>Did you know?</h3>
        <p>{{ randomFact }}</p>
      </div>
      <router-link to="/" class="home-link">
        <span>Return to Homepage</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </router-link>
    </div>
    <div class="error-background"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const facts = [
  "The word 'education' comes from the Latin 'educare' meaning 'to bring up or train'.",
  "The first known university in the world was the University of Bologna, founded in 1088.",
  "The longest word in the English language is 189,819 letters long and would take about 3.5 hours to pronounce.",
  "The human brain is more active during sleep than during the day.",
  "A group of flamingos is called a 'flamboyance'.",
  "The Great Wall of China is not visible from space with the naked eye.",
  "The first computer programmer was a woman named Ada Lovelace.",
  "The shortest war in history lasted only 38 minutes between Britain and Zanzibar in 1896.",
  "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
  "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion of the iron."
];

const randomFact = ref('');

onMounted(() => {
  randomFact.value = facts[Math.floor(Math.random() * facts.length)];
});
</script>

<style scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
  position: relative;
}

.error-content {
  text-align: center;
  z-index: 1;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  max-width: 600px;
}

.error-title {
  font-size: 8rem;
  font-weight: bold;
  color: #3498db;
  margin: 0;
  line-height: 1;
  animation: pulse 2s infinite;
}

.error-message h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.error-message p {
  color: #34495e;
  margin-bottom: 2rem;
}

.home-link {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.home-link:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
}

.home-link svg {
  margin-left: 0.5rem;
  transition: transform 0.3s ease;
}

.home-link:hover svg {
  transform: translateX(4px);
}

.error-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"%3E%3Cpath fill="%230099ff" fill-opacity="0.1" d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"%3E%3C/path%3E%3C/svg%3E') no-repeat bottom;
  background-size: cover;
  z-index: 0;
}

.educational-fact {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.educational-fact:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.educational-fact::before {
  content: '💡';
  position: absolute;
  top: -10px;
  left: -10px;
  font-size: 3rem;
  opacity: 0.1;
  transform: rotate(-15deg);
}

.educational-fact h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  position: relative;
  display: inline-block;
}

.educational-fact h3::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #3498db;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.educational-fact:hover h3::after {
  transform: scaleX(1);
}

.educational-fact p {
  color: #34495e;
  font-style: italic;
  margin-top: 0.5rem;
  line-height: 1.6;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .error-title {
    font-size: 6rem;
  }
  .error-message h2 {
    font-size: 1.5rem;
  }
}
</style>
