import React, { useState, useEffect }  from 'react'
import { useSpring, useTrail, animated } from 'react-spring';

import './Background.css';
function Background(flag) {
    
    const transcorner = useSpring({ 
        to: {opacity: 0.3 ,marginBottom:flag? 1000:0, marginRight:0, borderRight:flag? "1px solid #fff" :"1px solid #000"}, 
        from: {opacity: 0, marginBottom:-400, marginRight:-400},
        delay:flag?0:500,
        
        
        config: {mass: 1, frequency: 1, damping: 1},
      });

      const datetransition = useSpring({
        to: {opacity:flag? 1: 0, width:flag?"10%": "0%"},
    
    
        config: {mass: 1, frequency: 1, damping: 2},
      });

      const fadehalf = useSpring({ 
        to: {opacity: flag? 1 : 0.5, marginBottom: flag? 800: 0}, 
        from: {opacity: flag? 0.5:0, marginBottom:0},
        delay:flag?0:500,
        
        config: {mass: 1, frequency: 1, damping: 1},
      });

      const rotation = useSpring({
        to:{rotateZ:0}, 
        from:{rotateZ:360},
        loop: true,
    
        config: {duration:10000},
      });
    return (
        <>
            <animated.p style = {transcorner} className="line"></animated.p>
            <animated.p style = {transcorner} className="line2"></animated.p> 
            <animated.p style = {transcorner} className="line3"></animated.p>

            <animated.hr style = {datetransition} className="dateline"/>
            <animated.div style={fadehalf} className="circle"></animated.div>
            <animated.div style={fadehalf} className="larger-circle"></animated.div>
            <animated.div style={rotation} className="triangle"></animated.div>
      </>
    )
}

export default Background
