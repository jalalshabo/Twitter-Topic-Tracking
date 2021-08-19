import React, {useContext, useState} from 'react';
import { Bar } from 'react-chartjs-2';
import './ResultPage.css';
import { globalContext } from '../context/globalContext';
function ResultPage() {
    //const rand = () => Math.round(Math.random() * 20 - 10); 

    const {Result} = useContext(globalContext);
 
    const [GraphNumber, setGraphNumber] = useState(0);
    const testlabels = Object.keys(Result[GraphNumber]);
    const testvalues = Object.values(Result[GraphNumber]);

    const data = {
      labels: testlabels,
      datasets: [
        {
          label: 'Overall Term Frequency',
          data: testvalues,
          backgroundColor: [
            'rgba(54, 162, 235, 0.2)',
          ],
          borderColor: [
            'rgba(54, 162, 235, 1)',
          ],
          borderWidth: 1,
        },
      ],
    };

    const options = {
      indexAxis: 'y',
      // Elements options apply to all of the options unless overridden in a dataset
      // In this case, we are setting the border of each horizontal bar to be 2px wide
      elements: {
        bar: {
          borderWidth: 2,
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: 'right',
        },
        title: {
          display: true,
          text: 'Top 10 Relevant Terms for Topic ' + (GraphNumber + 1),
        },
      },
    };

    const changeGraph = (num) => {
      setGraphNumber(num);
    }

    return (
      <>
        <div className='result-wrapper'>

          <div className="topic-selection">
            <button onClick= {() => changeGraph(0)}> Topic 1</button>
            <button onClick= {() => changeGraph(1)}> Topic 2</button>
            <button onClick= {() => changeGraph(2)}> Topic 3</button>
            <button onClick= {() => changeGraph(3)}> Topic 4</button>
            <button onClick= {() => changeGraph(4)}> Topic 5</button>
            <button onClick= {() => changeGraph(5)}> Topic 6</button>
            <button onClick= {() => changeGraph(6)}> Topic 7</button>
            <button onClick= {() => changeGraph(7)}> Topic 8</button>
            <button onClick= {() => changeGraph(8)}> Topic 9</button>
            <button onClick= {() => changeGraph(9)}> Topic 10 </button>
          </div>
            <div className='result-graph'>
              <Bar data={data} options={options}/>
            </div>
          </div>
          
        
      </>
    );

 

}

export default ResultPage
