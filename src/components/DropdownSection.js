import React,{ useContext, useState}  from 'react';
import {useSpring, animated} from 'react-spring';
import {globalContext} from '../context/globalContext';
import './DropdownSection.css';
function DropdownSection(props) {

    const {globalState} = useContext(globalContext);
    const [open, setOpen] = useState(false);
    const dropdowntransition = useSpring({
        to:{opacity:globalState?0.7: 0,marginTop:globalState?200: 0, backgroundColor: "#D5D5D5"},
        from:{opacity:0,},
    })
    function Dropdown() {

        function DropdownItem(props) {
            return (
                <a href="#" className="menu-item">
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
    return (
        <>
         
            <animated.a style={dropdowntransition} className="dropdownbutton" onClick = {() => setOpen(!open)}>
                     List {open? <i class="fas fa-caret-up"></i> : <i class="fas fa-caret-down"></i>}
            </animated.a>

            {open && <Dropdown />}
        </>
    )
}

export default DropdownSection
