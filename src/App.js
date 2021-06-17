import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';

import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0)

  const fade = useSpring({ 
    to: {opacity: 1 }, 
    from: {opacity: 0},
    delay:300,
    
    config: {duration: 1000},
  });

  const fadehalf = useSpring({ 
    to: {opacity: 0.5 }, 
    from: {opacity: 0},
    delay:300,
    
    config: {duration: 1000},
  });

  const translate = useSpring({ 
    to: {opacity: 1 ,marginTop:0}, 
    from: {opacity: 0, marginTop:-200},
    
    
    config: {mass: 1, frequency: 1, damping: 1},
  });

  const rotation = useSpring({
    to:{rotateZ:0}, 
    from:{rotateZ:360},
    loop: true,

    config: {duration:10000},
  });
  useEffect(() => {
    fetch('/time').then(response => response.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className= "App">

      <animated.h1 style = {translate}> Welcome to Topic Tracking </animated.h1>
      <animated.a style = {fade} className="button"> Let's begin </animated.a>
      <animated.div style={fadehalf} className="circle"></animated.div>
      <animated.div style={fadehalf} className="larger-circle"></animated.div>
      <animated.div style={rotation} className="triangle"></animated.div>
    </div>
  );
}

export default App;
