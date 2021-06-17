import React, { useState, useEffect } from 'react';

import { useSpring, useTrail, animated } from 'react-spring';

import './App.css';

function App() {
<<<<<<< HEAD
  const [currentTime, setCurrentTime] = useState(0)
=======

  {/* Variable section that contains all the states that need to be tracked */}
  const [flag, setFlag] = useState(false);

  {/* This is a very roundabout way of deleting a button, not efficient at all */}
  const [begin, setBegin] = useState("button");
  const [chosenFunction, setChosenFunction] = useState(true);

  const [bgColor,setbgColor] = useState("");

  const [Color, setColor] = useState("");

  const [MainMessage, setMainMessage] = useState("Welcome to Topic Tracking");

  const [SubMessage, setSubMessage] = useState("A Twitter-based application");

  const [currentTime, setCurrentTime] = useState(0);
>>>>>>> 42522d6e438d0f048e67891fa50512eb353d50e6

  {/* This section is the animation section, where all the animations and transitions are done via the react-spring library*/}
  const fade = useSpring({ 
    to: {opacity: flag? 0 : 1}, 
    from: {opacity: flag? 0 : 1},
    delay:flag?0:300,
    
    config: {duration: 1000},
  });

  const fadehalf = useSpring({ 
    to: {opacity: flag? 1 : 0.5, marginBottom: flag? 800: 0}, 
    from: {opacity: flag? 0.5:0, marginBottom:0},
    delay:flag?0:500,
    
    config: {mass: 1, frequency: 1, damping: 1},
  });

  const translate = useSpring({ 
    to: {opacity: 1 ,marginTop:flag? -100:0}, 
    from: {opacity: 0, marginTop:-200},
    
    
    config: {mass: 1, frequency: 1, damping: 1},
  });

  const rotation = useSpring({
    to:{rotateZ:0}, 
    from:{rotateZ:360},
    loop: true,

    config: {duration:10000},
  });

  const transcorner = useSpring({ 
    to: {opacity: 0.3 ,marginBottom:flag? 1000:0, marginRight:0, borderRight:flag? "1px solid #fff" :"1px solid #000"}, 
    from: {opacity: 0, marginBottom:-400, marginRight:-400},
    delay:flag?0:500,
    
    
    config: {mass: 1, frequency: 1, damping: 1},
  });

  {/* This section will contain all the functional data that is being pulled from the python file */}
  useEffect(() => {
    fetch('/time').then(response => response.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  {/* This section is for all the custom functions that need to be defined */}
  const secondPage = () => {
    setbgColor("#6B7378");
    setColor("#fff");
    setMainMessage("Enter your date range");
    setSubMessage("");
    setFlag(true);
    setBegin("");
    setChosenFunction(false);
  }

  {/* The render section */}
  return (
    <div className= "App" style={{backgroundColor: bgColor, color: Color}}>

      <animated.h1 style = {translate}> {MainMessage} </animated.h1>
      <animated.p style = {fade} className="typewriter"> {SubMessage}</animated.p>
      
      <animated.p style = {transcorner} className="line"></animated.p>
      <animated.p style = {transcorner} className="line2"></animated.p>
      <animated.p style = {transcorner} className="line3"></animated.p>

      <animated.button style = {fade} className={begin} onClick={chosenFunction? secondPage: ''}> Let's begin </animated.button>
      <animated.div style={fadehalf} className="circle"></animated.div>
      <animated.div style={fadehalf} className="larger-circle"></animated.div>
      <animated.div style={rotation} className="triangle"></animated.div>
    </div>
  );
}

export default App;
