import React from 'react';
import { motion } from 'framer-motion';
import banner from '../assets/banner.jpg';

const Hero = () => {
  return (
    <div className="pt-8 bg-gradient-to-b from-blue-100 to-blue-300 min-h-screen">
      <motion.h1
        className="text-4xl my-4 font-bold text-center text-blue-900"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        CALMY AI
      </motion.h1>
      <motion.img
        src={banner}
        alt="Banner"
        className="mx-auto my-9 w-1/4 rounded-lg shadow-lg"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
      />
      <motion.div
        className="w-1/3 mx-auto my-8"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 1 }}
      >
        <h2 className="text-center font-medium italic text-lg text-blue-800">
          "Your Personalized Stress & Fatigue Management Companion"
        </h2>
      </motion.div>
    </div>
  );
};

export default Hero;
