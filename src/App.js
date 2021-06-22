<<<<<<< Updated upstream
/* Core/Library Imports */
import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import './App.css';
/* Component Imports */
import MainMessage from  './components/MainMessage';
import Background from './components/Background';

/* Context Imports */
import {globalContext} from './context/globalContext';
import {messageContext} from './context/messageContext';
import {transitionContext} from './context/transitionContext';

function App() {
  const [currentTime, setCurrentTime] = useState(0)

  /* Variable section that contains all the states that need to be tracked */
  const [globalState, setglobalState] = useState(false);

  /* This is a very roundabout way of deleting a button, not efficient at all */
  const [buttonMessage,setButtonMessage] = useState("Let's begin");
  const [chosenFunction, setChosenFunction] = useState(true);

  const [bgColor,setbgColor] = useState("");

  const [Color, setColor] = useState("");

  const [TitleMessage, setMainMessage] = useState("Welcome to Topic Tracking");

  const [SubMessage, setSubMessage] = useState("A Twitter-based application");

  /* Global Spring Section*/
  const fade = useSpring({ 
    to: {opacity: globalState? 0 : 1}, 
    from: {opacity: globalState? 1 : 0},
    delay:globalState?0:300,
    
    config: {duration: 1000},
  });

  const fadebutton = useSpring({ 
    to: {marginRight:globalState?400:0, backgroundColor:globalState? "#D5D5D5" : "#88AAE5" ,opacity:0.5}, 
    from: {opacity: 0},
    delay:globalState?0:300,
   
    config: {duration: 1000},
  });

  /* This section will contain all the functional data that is being pulled from the python file */
  useEffect(() => {
    fetch('/time').then(response => response.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  /* This section is for all the custom functions that need to be defined */
  const secondPage = () => {
    setbgColor("#6B7378");
    setColor("#fff");
    setMainMessage("Enter your date range");
    setSubMessage("");
    setglobalState(true);
    setButtonMessage("YYYY-MM-DD")
    setChosenFunction(false);
  } 

  const enterDate = () => {
    alert("Enter Date");
  }
  /* The render section */
  return (
    <div className= "App" style={{backgroundColor: bgColor, color: Color}}>
      <globalContext.Provider value = {{globalState, setglobalState}}>
        {/*Pure background elements*/}
        <Background />
        <transitionContext.Provider value = {{fade}}>
            {/*text related elements */}
            <messageContext.Provider value = {{TitleMessage, SubMessage}}>
                <MainMessage />
            </messageContext.Provider>
            
            {/*functional component*/}
            <animated.button style = {fadebutton} className="button" id="button1" onClick={chosenFunction? secondPage: enterDate}>{buttonMessage}</animated.button>
            <animated.button style = {useSpring({to:{opacity:globalState?1: 0,marginLeft:globalState?400: 0, backgroundColor: "#D5D5D5"}, from:{opacity:0,},})} className="button" id="button2" onClick={enterDate}>{buttonMessage}</animated.button>
            
            <animated.button style = {useSpring({to:{opacity:globalState?1: 0,marginTop:globalState?400: 0, backgroundColor: "#D5D5D5"}, from:{opacity:0,},})} className="dropdownbutton" id="button2">Overall <p className="triangle">s</p></animated.button>
            
            <animated.button style = {useSpring({to:{opacity:globalState?1: 0,marginTop:globalState?700: 0, backgroundColor: "#555555", color:"#fff"}, from:{opacity:0,},})} className="button" id="button2" >Submit</animated.button>
            
            
        </transitionContext.Provider>
      </globalContext.Provider>
    </div>
  );
}

export default App;
=======
/* Core/Library Imports */
import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import './App.css';
/* Component Imports */
import MainMessage from  './components/MainMessage';
import Background from './components/Background';
import InputSection from './components/InputSection';
/* Context Imports */
import {globalContext} from './context/globalContext';
import {messageContext} from './context/messageContext';
import {transitionContext} from './context/transitionContext';

function App() {
  const [currentTime, setCurrentTime] = useState(0)

  /* Variable section that contains all the states that need to be tracked */
  const [globalState, setglobalState] = useState(false);

  /* This is a very roundabout way of deleting a button, not efficient at all */
  const [buttonMessage1,setButtonMessage1] = useState("Let's begin");

  const [bgColor,setbgColor] = useState("");

  const [Color, setColor] = useState("");

  const [TitleMessage, setMainMessage] = useState("Welcome to Topic Tracking");

  const [SubMessage, setSubMessage] = useState("A Twitter-based application");

  /* Global Spring Section*/
  const fade = useSpring({ 
    to: {opacity: globalState? 0 : 1}, 
    from: {opacity: globalState? 1 : 0},
    delay:globalState?0:300,
    
    config: {duration: 1000},
  });

  

  /* This section will contain all the functional data that is being pulled from the python file */
  useEffect(() => {
    fetch('/time').then(response => response.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  /* This section is for all the custom functions that need to be defined */
  const secondPage = () => {
    setbgColor("#6B7378");
    setColor("#fff");
    setMainMessage("Enter your date range");
    setSubMessage("");
    setglobalState(true);
    setButtonMessage1("YYYY-MM-DD")

  } 

  
  /* The render section */
  return (
    <div className= "App" style={{backgroundColor: bgColor, color: Color}}>
      <globalContext.Provider value = {{globalState, setglobalState, secondPage, buttonMessage1, setButtonMessage1}}>
        {/*Pure background elements*/}
        <Background />
        <transitionContext.Provider value = {{fade}}>
            {/*text related elements */}
            <messageContext.Provider value = {{TitleMessage, SubMessage}}>
                <MainMessage />
            </messageContext.Provider>
            
            {/*functional component*/}
            <InputSection />
             
        </transitionContext.Provider>
      </globalContext.Provider>
    </div>
  );
}

export default App;
>>>>>>> Stashed changes
