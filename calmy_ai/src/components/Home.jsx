import React from 'react';
import Hero from './Hero';

const Home = () => {
  return (
    <main>
      <nav style={styles.navbar}>
        <ul style={styles.navList}>
          <li style={styles.navItem}><a href="/" style={styles.navLink}>Home</a></li>
          <li style={styles.navItem}><a href="/tester" style={styles.navLink}>Tester</a></li>
          <li style={styles.navItem}><a href="/login" style={styles.navLink}>Logout</a></li>
        </ul>
      </nav>
      <Hero />
    </main>
  );
};

const styles = {
  navbar: {
    display: 'flex',
    justifyContent: 'center',
    background: 'linear-gradient(90deg,rgb(15, 48, 92),rgb(92, 174, 250))',
    padding: '15px 20px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  navList: {
    listStyle: 'none',
    display: 'flex',
    margin: 0,
    padding: 0,
  },
  navItem: {
    margin: '0 20px',
  },
  navLink: {
    color: '#fff',
    textDecoration: 'none',
    fontSize: '18px',
    fontWeight: 'bold',
    transition: 'color 0.3s ease, transform 0.3s ease',
  },
  navLinkHover: {
    color: '#E8F5E9',
    transform: 'scale(1.1)',
  },
};

export default Home;
