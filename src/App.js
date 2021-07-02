/* Core/Library Imports */
import React, { useState, useEffect } from 'react';
import { useSpring } from 'react-spring';
import './App.css';

/* Component Imports */
import MainMessage from  './components/MainMessage';
import Background from './components/Background';
import InputSection from './components/InputSection';
import ResultPage from './components/ResultPage';
/* Context Imports */
import {globalContext} from './context/globalContext';
import {messageContext} from './context/messageContext';
import {transitionContext} from './context/transitionContext';

function App() {
  const [currentTime, setCurrentTime] = useState(0)

  /* Variable section that contains all the states that need to be tracked */
  const [globalState, setglobalState] = useState(0);

  /* This is a very roundabout way of deleting a button, not efficient at all */
  const [buttonMessage1,setButtonMessage1] = useState("Let's begin");

  const [bgColor,setbgColor] = useState("");

  const [Color, setColor] = useState("");

  const [TitleMessage, setMainMessage] = useState("Welcome to Topic Tracking");

  const [SubMessage, setSubMessage] = useState("A Twitter-based application");

  /* Global Spring Section*/
  const fade = useSpring({ 
    to: {opacity: (globalState == 1)? 0 : 1}, 
    from: {opacity: (globalState == 1)? 1 : 0},
    delay:globalState?0:300,
    
    config: {duration: 1000},
  });

  

  /* This section will contain all the functional data that is being pulled from the python file */
  useEffect(() => {
    fetch('/time').then(response => response.json()).then(data => {
      console.log(data.time);
    });
  }, []);

  /* This section is for all the custom functions that need to be defined */
  const secondPage = () => {
    setbgColor("#6B7378");
    setColor("#fff");
    setMainMessage("Enter your date range");
    setSubMessage("Sort Method:");
    setglobalState(1);
    setButtonMessage1("YYYY-MM-DD")

  } 

  
  /* The render section */
  return (
    <div className= "App" style={{backgroundColor: bgColor, color: Color}}>
      <globalContext.Provider value = {{globalState, setglobalState, secondPage, buttonMessage1, setButtonMessage1}}>
        <messageContext.Provider value = {{TitleMessage, SubMessage,setSubMessage, setMainMessage}}>
        {/*Pure background elements*/}

        <Background />

        <transitionContext.Provider value = {{fade}}>
            {/*text related elements */}
            
                <MainMessage />
      
            {/*functional component*/}

            {(globalState !=2) && <InputSection />}
            {(globalState == 2 ) && <ResultPage />}
        </transitionContext.Provider>
        </messageContext.Provider>
      </globalContext.Provider>
    </div>
  );
}

export default App;
