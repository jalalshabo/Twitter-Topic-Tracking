import React, {useContext} from 'react'

import './ResultPage.css';
import { globalContext } from '../context/globalContext';
function ResultPage() {
    //const rand = () => Math.round(Math.random() * 20 - 10); 

    const {ResultDiv} = useContext(globalContext);
    const {ResultScript} = useContext(globalContext);
    const {ResultLink} = useContext(globalContext);
  
    var template = document.createElement('template');
    template.innerHTML = ResultDiv + ResultLink + ResultScript;
    console.log(template);

    function Template({ children, ...attrs }) {
      return (
        <template
          {...attrs}
          dangerouslySetInnerHTML={{ __html: children }}
        />
      );
    }
    return (
      <>
        <Template className="result-graph">
          {ResultDiv}
          {ResultScript}
          {ResultLink}
        </Template>
      </>
    );

 

}

export default ResultPage
