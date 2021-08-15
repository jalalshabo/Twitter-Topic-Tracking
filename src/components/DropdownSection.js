import React,{ useContext, useEffect,  useState}  from 'react';
import {useSpring, animated} from 'react-spring';

import {globalContext} from '../context/globalContext';
import {inputContext} from '../context/inputContext';


import './DropdownSection.css';
function DropdownSection(props) {

    const {globalState} = useContext(globalContext);
    const {chosenOption,setChosenOption} = useContext(inputContext);
    const {inputFieldValue,setInputFieldValue} = useContext(inputContext);
    const dropdowntransition = useSpring({
        to:{opacity:(globalState === 1)?0.7: 0,marginTop:(globalState === 1)?200: 0, backgroundColor: "#D5D5D5"},
        from:{opacity:0,},
    })
    
    const [open, setOpen] = useState(false);
    const [InputField, setInputField] = useState(false);
 
    function changeDropdownTarget(option) {
     
        setChosenOption(option);
        setOpen(false);
    }

    function Dropdown() {

        function DropdownItem(props) {
            return (
                <a className="menu-item" onClick = {() =>  changeDropdownTarget(props.children)}>
                    {props.children}
                </a>
            );
        }

        return (
            <div className="dropdown">
                <DropdownItem >Overall</DropdownItem>
                <DropdownItem >Location</DropdownItem>
                <DropdownItem >User</DropdownItem>
            </div>
        );
    }

    useEffect(() => {
        if (chosenOption === "User" || chosenOption ===  "Location") {
            setInputField(true);
        }
        else {
            setInputField(false);
        }
    })

    return (
        <>
         
            <animated.div style={dropdowntransition} className="dropdownbutton" onClick = {() => setOpen(!open)}>
                     {chosenOption} {open? <i class="fas fa-caret-up"></i> : <i class="fas fa-caret-down"></i>}
            </animated.div>

            {(InputField && !open) && 
            
            <>
            <input className = "inputfield" onChange = {event => setInputFieldValue(event.target.value)} /> 
            <p>{(chosenOption === "Location")? "e.g. Windsor, ON" : ""}</p>
            </>
            }
            {open && <Dropdown />}
        </>
    )
}

export default DropdownSection
