import React, {useState, useContext, useEffect, useRef} from 'react'
import { globalContext } from '../context/globalContext';
import { inputContext} from '../context/inputContext';
import { messageContext } from '../context/messageContext';
import {useSpring, animated} from 'react-spring';
import Calendar from 'react-calendar';
import DropdownSection from './DropdownSection';

import './InputSection.css';

function InputSection() {

    const {ResultDiv} = useContext(globalContext);
    const {ResultScript} = useContext(globalContext);
    const {ResultLink} = useContext(globalContext);
    const {setResultDiv} = useContext(globalContext);
    const {setResultScript} = useContext(globalContext);
    const {setResultLink} = useContext(globalContext);

    const {globalState} = useContext(globalContext);
    const {secondPage} = useContext(globalContext);
    const {buttonMessage1} = useContext(globalContext);
    const {setButtonMessage1} = useContext(globalContext);
    const {setMainMessage} = useContext(messageContext);
    const {setSubMessage} = useContext(messageContext);
    const {setglobalState} = useContext(globalContext);

    const [SelectDate1, setSelectDate1] = useState(false);
    const [SelectDate2, setSelectDate2] = useState(false);
    const [Submit, setSubmit] = useState(false);
    const [InputFieldValue, setInputFieldValue] = useState('');
    const today = new Date();
    const [Date1Selected,setDate1Selected] = useState(false);
    const [Date2Selected,setDate2Selected] = useState(false);

    const [buttonMessage2, setButtonMessage2] = useState("YYYY-MM-DD");
    const [chosenOption, setChosenOption] = useState("Overall");

    const [date] = useState (new Date());
    const [date1, setDate1] = useState (new Date());

    const [date2, setDate2] = useState (new Date());
    const isInitialMount = useRef(true);

    var button1;
    var button2;
    
    const fadebutton = useSpring({ 
        to: {marginRight:(globalState === 1)?400:0, backgroundColor:(globalState === 1)? "#D5D5D5" : "#88AAE5" ,opacity:0.5}, 
        from: {opacity: 0},
        delay:(globalState === 1)?0:300,
       
        config: {duration: 1000},
      });

    const secondbutton = useSpring({
        to:{opacity:(globalState === 1)?0.5: 0,marginLeft:(globalState === 1)?400: 0, backgroundColor: "#D5D5D5"},  
        from:{opacity:0,},
    });
    const enterDate1 = () => {
        setSelectDate1(true);
        button2 = document.getElementById("button2");
        button2.style.display="none";
    }  

    const enterDate2 = () => {
        setSelectDate2(true);
        button1 = document.getElementById("button1");
        button1.style.display="none";
    }  
 
    const onChange1 = date => { 

        if (date.setHours(0,0,0,0) <= today.setHours(0,0,0,0) && date.setHours(0,0,0,0) <= date2.setHours(0,0,0,0)) {
            setDate1(date);

            setSelectDate1(false);
            setButtonMessage1(date.toISOString().substring(0, 10));
            var button2 = document.getElementById("button2");
            button2.style.display="block";
            setDate1Selected(true);
        }
        else {
            alert ("Choose a valid date!");
        }
    } 

    const onChange2 = date => { 
        if (date.setHours(0,0,0,0) <= today.setHours(0,0,0,0)) {
            if (Date1Selected && date1.setHours(0,0,0,0) <= date.setHours(0,0,0,0)) {
                setDate2(date);

                setSelectDate2(false);
                setButtonMessage2(date.toISOString().substring(0, 10));
                button1 = document.getElementById("button1");
                button1.style.display="block";
                setDate2Selected(true);
            }  
            else if (!Date1Selected) {
                setDate2(date);

                setSelectDate2(false);
                setButtonMessage2(date.toISOString().substring(0, 10));
                button1 = document.getElementById("button1");
                button1.style.display="block";
                setDate2Selected(true);
            }
            else {
                alert ("Choose a valid date!");
            }
        }
        else {
            alert ("Choose a valid date!");
        }
    } 
    
    useEffect(() => {
            if (isInitialMount.current) { 
                isInitialMount.current = false;
            }
            else {
                fetch('/api/tweets/date_range?start_date=' + buttonMessage1 + '&end_date=' + buttonMessage2).then(response => response.json()).then( data => {
                    console.log(data);
                    if (Submit) { 
                        setResultDiv(data.divElement);
                        setResultLink(data.linkElement);
                        setResultScript(data.scriptElement);
                        console.log(ResultDiv);
                        console.log(ResultLink);
                        console.log(ResultScript);
                        setSubMessage('');
                        setMainMessage("Topic Tracking Results: ");
                        setglobalState(2);
                    }
                    
                });
            }
    },[Submit]);

    return (
        <>
            {SelectDate1? <Calendar onChange={onChange1} value = {date} className="front-calendar"/> : <animated.button style = {fadebutton} className="button" id="button1" onClick={(globalState === 1)? enterDate1: secondPage}>{buttonMessage1}</animated.button>}
            
            {SelectDate2? <Calendar onChange={onChange2} value = {date} className="front-calendar" /> : <animated.button style = {secondbutton} className="button" id="button2" onClick={(globalState === 1)?enterDate2: ''}>{buttonMessage2}</animated.button>}
            <inputContext.Provider value = {{chosenOption,setChosenOption, setInputFieldValue}}>
                { (globalState === 1) && <DropdownSection />} 
     
            </inputContext.Provider>
           
            <animated.button style = {useSpring({to:{opacity:(globalState === 1)?0.5: 0,marginTop:(globalState === 1)?700: 0, backgroundColor: "#555555", color:"#fff"}, from:{opacity:0,},})} className="button" id="submitbutton" 
                    onClick = { async () => {
                    if (Date1Selected && Date2Selected) {
                        const inputdata = {buttonMessage1, buttonMessage2, chosenOption, InputFieldValue};
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
                    }
                    else {
                        alert ("You must enter a date range first!");
                    }
                    
            }}>Submit</animated.button>
            
        </>
    )
}

export default InputSection
