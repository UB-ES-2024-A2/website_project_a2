<template>
  <div id="main-page" class="main-page">
    <div class="about-us-container">
      <h1 class="page-title">About Us</h1>

      <section class="about-section">
        <h2>Our Story</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor.</p>
      </section>

      <section class="about-section">
        <h2>Our Mission</h2>
        <p>Ut in nulla enim. Phasellus molestie magna non est bibendum non venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus. Mauris iaculis porttitor posuere.</p>
      </section>

      <section class="about-section">
        <h2>Our Team</h2>
        <div class="team-grid">
          <div class="team-member" v-for="member in teamMembers" :key="member.name">
            <!-- <img :src="member.avatar" :alt="member.name" class="member-avatar"> -->
            <h3>{{ member.name }}</h3>
            <p>{{ member.role }}</p>
          </div>
        </div>
      </section>

      <section class="about-section">
        <h2>Contact Us</h2>
        <p>Have any questions? We'd love to hear from you!</p>
        <button class="contact-button">Get in Touch</button>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'information',
  data () {
    return {
      teamMembers: [
        { name: 'Jane Doe', role: 'Founder & CEO', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'John Smith', role: 'CTO', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Alice Johnson', role: 'Lead Designer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Bob Brown', role: 'Lead Developer', avatar: '/placeholder.svg?height=150&width=150' }
      ]
    }
  }
}
</script>

<style scoped>
.main-page {
  grid-area: main-page;
  padding: calc(var(--panel-gap) * 2);
  background-color: var(--box-background-color);
  color: var(--text-color);
  border-radius: calc(var(--border-radius) * 2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.about-us-container {
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.page-title {
  font-size: var(--font-size-title);
  color: var(--purple-background);
  margin-bottom: calc(var(--panel-gap) * 2);
  text-align: center;
}

.about-section {
  margin-bottom: calc(var(--panel-gap) * 4);
}

h2 {
  font-size: var(--font-size-medium);
  color: var(--purple-background);
  margin-bottom: var(--panel-gap);
}

p {
  font-size: var(--font-size-xs);
  line-height: 1.6;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: calc(var(--panel-gap) * 2);
  margin-top: calc(var(--panel-gap) * 2);
}

.team-member {
  text-align: center;
  background-color: var(--half-transparent-background);
  padding: calc(var(--panel-gap) * 2);
  border-radius: var(--border-radius);
  transition: transform 0.3s ease;
}

.team-member:hover {
  transform: translateY(-5px);
}

.member-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: var(--panel-gap);
}

.contact-button {
  background-color: var(--purple-background);
  color: var(--text-color);
  padding: var(--panel-gap) calc(var(--panel-gap) * 2);
  border-radius: calc(var(--border-radius) * 2);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin-top: var(--panel-gap);
}

.contact-button:hover {
  background-color: var(--blue-background);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}

</style>
