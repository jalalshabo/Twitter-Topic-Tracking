import React, {useState, useContext, useEffect} from 'react'
import { globalContext } from '../context/globalContext';
import { inputContext} from '../context/inputContext';
import {useSpring, animated} from 'react-spring';
import Calendar from 'react-calendar';
import DropdownSection from './DropdownSection';
import { Async } from 'react-async';

import './InputSection.css';

function InputSection() {

    const {globalState} = useContext(globalContext);
    const {secondPage} = useContext(globalContext);
    const {buttonMessage1} = useContext(globalContext);
    const {setButtonMessage1} = useContext(globalContext);

    const [SelectDate1, setSelectDate1] = useState(false);
    const [SelectDate2, setSelectDate2] = useState(false);
    const [Submit, setSubmit] = useState(false);

    const [buttonMessage2, setButtonMessage2] = useState("YYYY-MM-DD");
    const [chosenOption, setChosenOption] = useState("List");

    const [date, setDate] = useState (new Date());
    const fadebutton = useSpring({ 
        to: {marginRight:globalState?400:0, backgroundColor:globalState? "#D5D5D5" : "#88AAE5" ,opacity:0.5}, 
        from: {opacity: 0},
        delay:globalState?0:300,
       
        config: {duration: 1000},
      });

    const secondbutton = useSpring({
        to:{opacity:globalState?0.5: 0,marginLeft:globalState?400: 0, backgroundColor: "#D5D5D5"},  
        from:{opacity:0,},
    });
    const enterDate1 = () => {
        setSelectDate1(true);
        var button2 = document.getElementById("button2");
        button2.style.display="none";
    }  

    const enterDate2 = () => {
        setSelectDate2(true);
        var button1 = document.getElementById("button1");
        button1.style.display="none";
    }  
 
    const onChange1 = date => { 
        setDate(date);

        setSelectDate1(false);
        setButtonMessage1(date.toISOString().substring(0, 10));
        var button2 = document.getElementById("button2");
        button2.style.display="block";
    } 

    const onChange2 = date => { 
        setDate(date);

        setSelectDate2(false);
        setButtonMessage2(date.toISOString().substring(0, 10));
        var button1 = document.getElementById("button1");
        button1.style.display="block";
    } 
    
    useEffect(() => {
        if (Submit){
            fetch('/sqlstatement').then(response => response.json()).then( data => {
                console.log(data.sqlstatement);
            });
        }
       
    });
    return (
        <>
            {SelectDate1? <Calendar onChange={onChange1} value = {date} className="front"/> : <animated.button style = {fadebutton} className="button" id="button1" onClick={globalState? enterDate1: secondPage}>{buttonMessage1}</animated.button>}
            
            {SelectDate2? <Calendar onChange={onChange2} value = {date} className="front" /> : <animated.button style = {secondbutton} className="button" id="button2" onClick={enterDate2}>{buttonMessage2}</animated.button>}
            <inputContext.Provider value = {{chosenOption,setChosenOption}}>
                <DropdownSection> 
          
                </DropdownSection>
            </inputContext.Provider>
           
            <animated.button style = {useSpring({to:{opacity:globalState?0.5: 0,marginTop:globalState?700: 0, backgroundColor: "#555555", color:"#fff"}, from:{opacity:0,},})} className="button" id="submitbutton" 
                    onClick = { async () => {
                    const inputdata = {buttonMessage1, buttonMessage2};
                    const response = await fetch('./add_sqlstatement', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(inputdata)
                    })
                    
                    if (response.ok) {
                        console.log("Request was successful");
                        setSubmit(true);
                    }
                    
                   
                    console.log(Submit);
            }}>Submit</animated.button>
            
        </>
    )
}

export default InputSection
