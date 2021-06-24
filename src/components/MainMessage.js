import React, { useContext } from 'react';
import { globalContext } from '../context/globalContext';
import { messageContext } from '../context/messageContext';
import { transitionContext } from '../context/transitionContext';
import {useSpring, animated} from 'react-spring';

import './MainMessage.css';

function MainMessage() {
 
    
    const {globalState} = useContext(globalContext);
    const {fade} = useContext(transitionContext);  

    const {TitleMessage} = useContext(messageContext);
    const {SubMessage} = useContext(messageContext);

    const translate = useSpring({ 
        to: {opacity: 1 ,marginTop:globalState?-100:-200}, 
        from: {opacity: 0, marginTop: -500},
        
        
        config: {mass: 1, frequency: 1, damping: 1},
    });
   
    const translate2 = useSpring({ 
        to: {opacity: 1 ,translateY:190}, 
        from: {opacity: 0, translateY:0 },
        delay: 500,
        
        config: {mass: 1, frequency: 1, damping: 1},
    });
    return (
        <>
          <animated.h1 style = {translate}> {TitleMessage} </animated.h1>
          <animated.p style = {globalState? translate2 :fade} className="typewriter"> {SubMessage}</animated.p>
        </>
    )
}

export default MainMessage
