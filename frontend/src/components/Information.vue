<template>
  <div id="main-page" class="main-page">
    <div class="about-us-container">
      <h1 class="page-title">About Us</h1>

      <section class="about-section">
        <h2>Our Story</h2>
        <p>We are  a group of students passionate about books and technology. We came together with a clear idea: to create a space where readers from all corners can discover, share, and enjoy the magic of reading.</p>
      </section>

      <section class="about-section">
        <h2>Our Mission</h2>
        <p>Our website is more than just a book catalog; it’s a community that connects stories with people. We believe that every book has the power to inspire, teach, and transform, and our goal is to bring that power closer to those who seek it.
          As students, we know how important it is to have access to good resources, and with this project, we want to do our part to foster a love for reading. Thank you for being part of this adventure with us!</p>
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
      <!--
      <section class="about-section">
        <h2>Contact Us</h2>
        <p>Have any questions? We'd love to hear from you!</p>
        <button class="contact-button">Get in Touch</button>
      </section>
      -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'information',
  data () {
    return {
      teamMembers: [
        { name: 'Adria Alfonso', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Albert Meliksetyan', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Eloi Busquets', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Hlieb Sydorenko', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Marta Bernadas', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' },
        { name: 'Nacho Rivera', role: 'Developer', avatar: '/placeholder.svg?height=150&width=150' }
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
  width: 40%;
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
